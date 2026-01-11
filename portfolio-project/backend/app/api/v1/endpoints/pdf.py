from typing import Optional
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import logging
import io
from PIL import Image
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)
router = APIRouter()

from typing import List

def _resize_image_for_pdf(data: bytes, max_width: int = 1024) -> tuple[bytes, str]:
    """Resize image to a maximum width to prevent Playwright crashes due to huge data-URIs."""
    try:
        img = Image.open(io.BytesIO(data))
        # Determine MIME
        fmt = img.format or "PNG"
        mime = f"image/{fmt.lower()}".replace("jpg", "jpeg")
        
        if img.width > max_width:
            aspect_ratio = img.height / float(img.width)
            new_height = int(max_width * aspect_ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            out_bio = io.BytesIO()
            # Preserve format if possible, otherwise webp or jpeg
            save_fmt = fmt if fmt in ["JPEG", "PNG", "WEBP"] else "JPEG"
            img.save(out_bio, format=save_fmt, quality=85)
            return out_bio.getvalue(), f"image/{save_fmt.lower()}".replace("jpg", "jpeg")
        
        return data, mime
    except Exception as e:
        logger.warning("Resize failed, using original: %s", e)
        return data, "image/png"

class GeneratePdfRequest(BaseModel):
    html: Optional[str] = None
    url: Optional[str] = None
    landscape: Optional[bool] = False
    failed_images: Optional[List[str]] = None
    skipped_images: Optional[List[str]] = None

# Reject unreasonably large payloads early to avoid memory issues (5 MB)
MAX_HTML_SIZE_BYTES = 5 * 1024 * 1024

@router.post("/generate")
async def generate_pdf(payload: GeneratePdfRequest):
    """Render provided HTML or URL to a PDF using Playwright and return as application/pdf"""
    if not payload.html and not payload.url:
        raise HTTPException(status_code=400, detail="Either 'html' or 'url' must be provided")

    if payload.html and len(payload.html.encode('utf-8')) > MAX_HTML_SIZE_BYTES:
        logger.warning("PDF request rejected: html payload too large (%d bytes)", len(payload.html.encode('utf-8')))
        raise HTTPException(status_code=413, detail="HTML payload too large")

    try:
        # Log failed images reported by frontend (helps debug inlining failures)
        if getattr(payload, 'failed_images', None):
            logger.warning("Frontend reported failed images: %s", payload.failed_images)

        # Attempt to fetch and inline remote images skipped by the client (skipped_images)
        if getattr(payload, 'skipped_images', None):
            try:
                import re, base64, requests
                from pathlib import Path
                for url in payload.skipped_images:
                    try:
                        if not re.match(r'^https?://', url):
                            logger.warning('Skipping non-http url for remote fetch: %s', url)
                            continue
                        resp = requests.get(url, stream=True, timeout=10)
                        resp.raise_for_status()
                        data = resp.content if hasattr(resp, 'content') else b''.join(resp.iter_content(8192))
                        # Resize to prevent crash
                        data, mime = _resize_image_for_pdf(data)
                        b64 = base64.b64encode(data).decode('ascii')
                        payload.html = re.sub(re.escape(f'src="{url}"'), f'src="data:{mime};base64,{b64}"', payload.html)
                        logger.warning('Inlined remote image %s (%d bytes)', url, len(data))
                    except Exception as e:
                        logger.warning('Failed to fetch remote image %s: %s', url, e)
            except Exception:
                logger.exception('Error while attempting to inline remote skipped images')

        # Server-side inline for local static images (e.g., src="/static/images/...")
        if payload.html:
            try:
                import re, base64
                from pathlib import Path
                # Find all src="/static/..." or src='/static/...'
                def _inline_local_static(match):
                    src = match.group(1)
                    parsed = urlparse(src)
                    normalized_path = parsed.path or src
                    if not normalized_path.startswith('/static/'):
                        return match.group(0)
                    # Map to app/static path
                    local_path = Path(__file__).resolve().parents[3] / 'static' / normalized_path.replace('/static/', '')
                    try:
                        data = local_path.read_bytes()
                        # Resize local images too
                        data, mime = _resize_image_for_pdf(data)
                        b64 = base64.b64encode(data).decode('ascii')
                        return f'src="data:{mime};base64,{b64}"'
                    except Exception:
                        logger.warning("Could not inline local static image: %s", local_path)
                        return match.group(0)

                payload_html = payload.html
                payload_html = re.sub(r'src=["\']([^"\']+)["\']', _inline_local_static, payload_html)
            except Exception:
                logger.exception("Error while attempting to inline local static images")
                payload_html = payload.html
        else:
            payload_html = None

        async with async_playwright() as p:
            browser = await p.chromium.launch(args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ])
            page = await browser.new_page()

            if payload.url:
                # navigate to URL
                await page.goto(payload.url, wait_until='networkidle')
            else:
                # directly set HTML content (useful to avoid network dependency)
                await page.set_content(payload_html or payload.html, wait_until='networkidle')

            try:
                pdf_bytes = await page.pdf(
                    format='A4',
                    print_background=True,
                    display_header_footer=False,
                    margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                    prefer_css_page_size=True
                )
            except Exception as primary_err:
                # Diagnostic logging: gather basic metrics about content and images
                try:
                    import re, time, base64
                    from pathlib import Path
                    html_content = payload_html or payload.html or ''
                    img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
                    total_b64_len = sum(len(m) for m in img_matches if m.startswith('data:'))
                    logger.warning("Initial page.pdf failed; img_count=%d total_b64_len=%d html_len=%d",
                                   len(img_matches), total_b64_len, len(html_content))

                    # Try to capture a screenshot for debugging
                    try:
                        screenshot_bytes = await page.screenshot(full_page=True)
                        screenshot_path = Path('/tmp') / f'pdf_error_screenshot_{int(time.time())}.png'
                        screenshot_path.write_bytes(screenshot_bytes)
                        logger.warning("Wrote PDF debug screenshot to %s", screenshot_path)
                    except Exception:
                        logger.exception("Failed to take screenshot for diagnostics")
                except Exception:
                    logger.exception("Failed to gather diagnostics after page.pdf failure")

                # Retry with fallback scales
                last_exc = primary_err
                for scale in (0.9, 0.8, 0.7):
                    try:
                        logger.warning("Retrying page.pdf with scale=%s", scale)
                        pdf_bytes = await page.pdf(
                            format='A4',
                            print_background=True,
                            display_header_footer=False,
                            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                            scale=scale
                        )
                        logger.warning("PDF generation succeeded with scale=%s", scale)
                        break
                    except Exception as retry_err:
                        logger.exception("Retry with scale=%s failed", scale)
                        last_exc = retry_err
                else:
                    # All retries failed
                    await browser.close()
                    logger.exception("All PDF retries failed: %s", last_exc)
                    raise last_exc

            await browser.close()

            return Response(content=pdf_bytes, media_type="application/pdf",
                            headers={"Content-Disposition": "attachment; filename=portfolio.pdf"})

    except Exception as exc:
        # Log full stacktrace for debugging
        logger.exception("Failed to generate PDF: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error while generating PDF")

import api from '@/services/api';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

// -----------------------------------------------------------
// 1. DOMPurify & Markdown 설정 (기존 유지)
// -----------------------------------------------------------
const DOMPURIFY_CONFIG = {
  ALLOWED_TAGS: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'a', 'img',
    'strong', 'em', 'b', 'i', 'u', 's', 'del', 'ins',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
  ],
  ALLOWED_ATTR: [
    'href', 'src', 'alt', 'title', 'class', 'id',
    'width', 'height', 'style'
  ],
  FORBID_TAGS: [
    'script', 'style', 'iframe', 'object', 'embed', 'form', 
    'nav', 'header', 'footer', 'button', 'input', 'textarea', 'select'
  ],
  FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover'],
};

function isMarkdown(content) {
  if (!content) return false;
  const htmlTagPattern = /<\/?[a-z][\s\S]*>/i;
  const markdownPatterns = [
    /^#{1,6}\s/m, /\*\*[^*]+\*\*/, /\*[^*]+\*/, /!\[.*?\]\(.*?\)/,
    /\[.*?\]\(.*?\)/, /^[-*+]\s/m, /^\d+\.\s/m, /^\u003e\s/m,
    /```[\s\S]*?```/, /`[^`]+`/
  ];
  return !htmlTagPattern.test(content) && markdownPatterns.some(p => p.test(content));
}

function markdownToHtml(markdown) {
  marked.setOptions({ breaks: true, gfm: true, headerIds: false, mangle: false });
  return DOMPurify.sanitize(marked(markdown), DOMPURIFY_CONFIG);
}

function normalizeContent(content) {
  if (!content) return '<p>내용 없음</p>';
  return isMarkdown(content) ? markdownToHtml(content) : DOMPurify.sanitize(content, DOMPURIFY_CONFIG);
}

// -----------------------------------------------------------
// 2. 인쇄용 HTML 생성 및 window.print() 실행
// -----------------------------------------------------------

/**
 * 포트폴리오 데이터를 인쇄 가능한 HTML 문서로 변환하여 새 창에 띄우고 인쇄 대화상자를 호출합니다.
 * 이 방식은 텍스트가 Selectable하며, 벡터 품질을 유지하고, 용량이 매우 작습니다.
 */
export async function generatePortfolioPDF() {
  try {
    // 1. 데이터 가져오기
    const [aboutRes, postsRes] = await Promise.all([
      api.get('/api/v1/board/slug/about').catch(() => ({ data: {} })),
      api.get('/api/v1/board/')
    ]);

    const aboutData = aboutRes.data;
    const posts = postsRes.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    // 2. HTML 문자열 조립 (인쇄용 스태틱 HTML, 스크립트 없음)
    const style = `
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        @page { size: A4; margin: 15mm; }
        body { font-family: 'Noto Sans KR', sans-serif; line-height: 1.6; color: #333; background: #fff; margin: 0; padding: 0; }
        a { text-decoration: none; color: inherit; }
        .page-break { page-break-after: always; break-after: page; }
        .no-break { page-break-inside: avoid; break-inside: avoid; }
        .cover-page { height: 90vh; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; }
        .cover-title{ font-size:48px; font-weight:bold; margin-bottom:20px; }
        .cover-subtitle{ font-size:24px; color:#555; margin-bottom:10px; }
        .cover-date{ font-size:18px; color:#888; }
        .section-title{ font-size:32px; font-weight:bold; border-bottom:2px solid #333; padding-bottom:10px; margin-bottom:30px; margin-top:0; }
        .post-container{ margin-bottom:50px; }
        .post-header{ margin-bottom:20px; padding-bottom:10px; border-bottom:1px solid #eee; }
        .post-title{ font-size:24px; font-weight:bold; margin:0 0 10px 0; }
        .post-meta{ font-size:14px; color:#666; display:block; }
        .post-meta span:first-child { display:block; margin-bottom:5px; }
        .post-tag{ color:#2563eb; display:block; margin-top:5px; }
        .markdown-body{ font-size:14px; }
        .markdown-body h1, .markdown-body h2, .markdown-body h3{ margin-top:20px; margin-bottom:10px; font-weight:bold; page-break-after:avoid; }
        .markdown-body p{ margin-bottom:10px; text-align:justify; }
        .markdown-body img{ max-width:100%; height:auto; display:block; margin:15px auto; border-radius:4px; page-break-inside:avoid; }
        .markdown-body pre{ background:#f8f9fa; padding:15px; border-radius:5px; overflow-x:auto; font-family:monospace; font-size:12px; page-break-inside:avoid; border:1px solid #e9ecef; white-space:pre-wrap; }
        .markdown-body blockquote{ border-left:4px solid #dfe2e5; padding-left:15px; color:#6a737d; margin:15px 0; page-break-inside:avoid; }
        @media print { body { -webkit-print-color-adjust: exact; } }
      </style>
    `;

    const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

    const coverHtml = `
      <div class="cover-page page-break">
        <div class="cover-title">PORTFOLIO</div>
        <div class="cover-subtitle">Sung Yeun Woo</div>
      </div>
    `;

    let aboutHtml = '';
    if (aboutData && aboutData.content) {
      aboutHtml = `
        <div class="page-break">
          <h1 class="section-title">${aboutData.title || 'About Me'}</h1>
          <div class="markdown-body">${normalizeContent(aboutData.content)}</div>
        </div>
      `;
    }

    let postsHtml = '';
    if (posts.length > 0) {
      postsHtml += `<h1 class="section-title">Projects</h1>`;

      posts.forEach((post, index) => {
        const dateStr = new Date(post.created_at).toLocaleDateString('en-US');
        const tags = post.tags ? `<span class="post-tag">${post.tags.replaceAll(',', ' · ')}</span>` : '';
        postsHtml += `
          <div class="post-container page-break">
            <div class="post-header">
              <h2 class="post-title">${index + 1}. ${post.title}</h2>
              <div class="post-meta">
                ${tags}
              </div>
            </div>
            <div class="markdown-body">${normalizeContent(post.content)}</div>
          </div>
        `;
      });
    }

    const fullHtml = `
      <!DOCTYPE html>
      <html lang="ko">
      <head><meta charset="UTF-8"><title></title>${style}</head>
      <body>${coverHtml}${aboutHtml}${postsHtml}</body>
      </html>
    `;

    // 3. 이미지들을 Data URL로 인라인화하여 Playwright가 외부 리소스 없이 렌더링할 수 있게 함
    const INLINE_MAX_BYTES = 300 * 1024; // 300 KB per image limit
    const inlineImagesInHtml = async (html) => {
      const failed = [];
      const skipped = []; // images skipped because they are too large to inline in browser
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const imgs = Array.from(doc.querySelectorAll('img'));

        await Promise.all(imgs.map(async (img) => {
          try {
            let src = img.getAttribute('src') || '';
            if (!src) return;

            let fullUrl = src;
            if (src.startsWith('//')) fullUrl = window.location.protocol + src;
            else if (src.startsWith('/')) fullUrl = window.location.origin + src;
            else if (!/^https?:\/\//i.test(src)) fullUrl = window.location.origin + '/' + src;

            // Check content-length first to avoid downloading very large images
            let headResp;
            try {
              headResp = await fetch(fullUrl, { method: 'HEAD', credentials: 'include' });
            } catch (e) {
              headResp = null;
            }

            const contentLen = headResp?.headers?.get('content-length');
            if (contentLen && parseInt(contentLen, 10) > INLINE_MAX_BYTES) {
              skipped.push(fullUrl);
              return;
            }

            const resp = await fetch(fullUrl, { credentials: 'include' });
            if (!resp.ok) { failed.push(fullUrl); return; }
            const blob = await resp.blob();

            if (blob.size > INLINE_MAX_BYTES) {
              // too big to include from browser side; ask server to inline instead
              skipped.push(fullUrl);
              return;
            }

            const arrayBuf = await blob.arrayBuffer();
            // convert to base64
            let binary = '';
            const bytes = new Uint8Array(arrayBuf);
            const chunkSize = 0x8000;
            for (let i = 0; i < bytes.length; i += chunkSize) {
              binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
            }
            const base64 = btoa(binary);
            const dataUrl = `${blob.type ? 'data:' + blob.type + ';base64,' : 'data:image/png;base64,'}${base64}`;
            img.setAttribute('src', dataUrl);
          } catch (e) {
            // 실패해도 전체 흐름 중단하지 않음
            console.warn('Failed to inline image', e);
            try { failed.push(img.getAttribute('src') || ''); } catch (_e) { console.warn('Could not record failed image src'); }
          }
        }));

        return { html: doc.documentElement.outerHTML, failed, skipped };
      } catch (e) {
        console.warn('inlineImagesInHtml error', e);
        return { html, failed, skipped };
      }
    }

    const { html: inlinedHtml, failed: failedImages, skipped: skippedImages } = await inlineImagesInHtml(fullHtml);

    // 4. 서버에 HTML을 보내 PDF로 변환하여 다운로드 받기
    const response = await api.post('/api/v1/pdf/generate', { html: inlinedHtml, failed_images: failedImages, skipped_images: skippedImages }, { responseType: 'blob' });

    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    const fileName = `portfolio_${new Date().toISOString().split('T')[0]}.pdf`;
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    return { success: true };

  } catch (error) {
    console.error('PDF generation failed:', error);
    throw new Error('서버에서 PDF를 생성하지 못했습니다.');
  }
}

// 기존 htmlToImage 등 불필요한 함수 제거됨




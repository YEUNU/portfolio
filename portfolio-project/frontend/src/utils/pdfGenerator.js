import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import api from '@/services/api';

// DOMPurify 설정: PDF 생성에 필요한 안전한 HTML 태그만 허용
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
    'width', 'height',
  ],
  FORBID_TAGS: ['script', 'style', 'iframe', 'object', 'embed', 'form'],
  FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover'],
};

/**
 * 콘텐츠가 Markdown인지 HTML인지 감지
 */
function isMarkdown(content) {
  if (!content) return false;
  
  // HTML 태그가 있으면 HTML로 판단
  const htmlTagPattern = /<\/?[a-z][\s\S]*>/i;
  
  // Markdown 특유의 패턴들
  const markdownPatterns = [
    /^#{1,6}\s/m,           // 헤딩: # ## ###
    /\*\*[^*]+\*\*/,        // 볼드: **text**
    /\*[^*]+\*/,            // 이탤릭: *text*
    /!\[.*?\]\(.*?\)/,      // 이미지: ![alt](url)
    /\[.*?\]\(.*?\)/,       // 링크: [text](url)
    // eslint-disable-next-line no-useless-escape
    /^[\*\-\+]\s/m,         // 리스트: * - +
    /^\d+\.\s/m,            // 번호 리스트: 1. 2.
    /^>\s/m,                // 인용: >
    /```[\s\S]*?```/,       // 코드 블록: ```
    /`[^`]+`/               // 인라인 코드: `code`
  ];
  
  const hasHtmlTags = htmlTagPattern.test(content);
  const hasMarkdownPatterns = markdownPatterns.some(pattern => pattern.test(content));
  
  // HTML 태그가 없고 Markdown 패턴이 있으면 Markdown
  return !hasHtmlTags && hasMarkdownPatterns;
}

/**
 * Markdown을 HTML로 변환 (DOMPurify로 XSS 방지)
 */
function markdownToHtml(markdown) {
  // marked 설정
  marked.setOptions({
    breaks: true,        // 줄바꿈을 <br>로 변환
    gfm: true,          // GitHub Flavored Markdown
    headerIds: false,   // 헤더에 ID 추가 안함
    mangle: false       // 이메일 주소 난독화 안함
  });
  
  const rawHtml = marked(markdown);
  // DOMPurify로 sanitize하여 XSS 방지
  return DOMPurify.sanitize(rawHtml, DOMPURIFY_CONFIG);
}

/**
 * 콘텐츠를 HTML로 정규화 (Markdown이면 변환, HTML이면 sanitize)
 */
function normalizeContent(content) {
  if (!content) return '<p>내용 없음</p>';
  
  if (isMarkdown(content)) {
    return markdownToHtml(content);
  }
  
  // HTML 콘텐츠도 sanitize
  return DOMPurify.sanitize(content, DOMPURIFY_CONFIG);
}

/**
 * HTML 콘텐츠를 Canvas로 렌더링하여 이미지로 변환
 */
async function htmlToImage(htmlContent, width = 800) {
  const tempContainer = document.createElement('div');
  tempContainer.style.position = 'absolute';
  tempContainer.style.left = '-9999px';
  tempContainer.style.top = '0';
  tempContainer.style.width = `${width}px`;
  tempContainer.style.padding = '40px';
  tempContainer.style.backgroundColor = 'white';
  tempContainer.style.fontFamily = "'Noto Sans KR', 'Malgun Gothic', Arial, sans-serif";
  tempContainer.style.fontSize = '16px';
  tempContainer.style.lineHeight = '1.8';
  tempContainer.style.color = '#000';
  tempContainer.style.wordBreak = 'break-word';
  
  // 이미지 스타일 추가
  tempContainer.innerHTML = `
    <style>
      img { max-width: 100%; height: auto; margin: 10px 0; }
      h1, h2, h3, h4, h5, h6 { margin: 20px 0 10px 0; font-weight: bold; }
      h1 { font-size: 28px; }
      h2 { font-size: 24px; }
      h3 { font-size: 20px; }
      p { margin: 10px 0; }
      pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
      code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
      table { border-collapse: collapse; width: 100%; margin: 15px 0; }
      th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
      th { background-color: #f5f5f5; font-weight: bold; }
      ul, ol { margin: 10px 0; padding-left: 30px; }
      li { margin: 5px 0; }
    </style>
    ${htmlContent}
  `;
  
  document.body.appendChild(tempContainer);

  try {
    const canvas = await html2canvas(tempContainer, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      logging: false,
      backgroundColor: '#ffffff',
      imageTimeout: 15000
    });

    const imgData = canvas.toDataURL('image/png');
    return {
      data: imgData,
      width: canvas.width,
      height: canvas.height
    };
  } finally {
    document.body.removeChild(tempContainer);
  }
}

/**
 * 이미지를 PDF에 추가하고 여러 페이지로 분할
 * 컨텐츠가 잘리거나 중복되지 않도록 정확하게 분할
 */
async function addImageToPDF(pdf, imgData, imgWidth, imgHeight, startY = 10) {
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const margin = 10;
  const maxWidth = pageWidth - (margin * 2);
  const bottomMargin = 15; // 하단 여백 (페이지 번호 공간)
  
  // 이미지 크기를 페이지 너비에 맞게 조정
  const ratio = maxWidth / imgWidth;
  const scaledWidth = maxWidth;
  const scaledHeight = imgHeight * ratio;
  
  // 첫 페이지에서 사용 가능한 높이
  const firstPageAvailableHeight = pageHeight - startY - bottomMargin;
  
  if (scaledHeight <= firstPageAvailableHeight) {
    // 한 페이지에 다 들어가는 경우
    pdf.addImage(imgData, 'PNG', margin, startY, scaledWidth, scaledHeight);
    return 1;
  }
  
  // 이미지 로드 (비동기)
  const img = new Image();
  await new Promise((resolve, reject) => {
    img.onload = resolve;
    img.onerror = reject;
    img.src = imgData;
  });
  
  // 여러 페이지에 걸쳐 있는 경우
  let remainingHeight = scaledHeight;
  let sourceY = 0; // 원본 이미지에서 자를 Y 위치 (스케일된 좌표)
  let pageCount = 0;
  let isFirstPage = true;
  
  while (remainingHeight > 0) {
    if (!isFirstPage) {
      pdf.addPage();
    }
    pageCount++;
    
    const availableHeight = isFirstPage 
      ? firstPageAvailableHeight 
      : pageHeight - margin - bottomMargin;
    
    const heightToDraw = Math.min(availableHeight, remainingHeight);
    const yPosition = isFirstPage ? startY : margin;
    
    // Canvas를 사용하여 이미지의 특정 부분만 잘라내기
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 원본 이미지 비율로 canvas 크기 설정
    const sourceHeight = heightToDraw / ratio;
    const sourceYInOriginal = sourceY / ratio;
    
    canvas.width = imgWidth;
    canvas.height = sourceHeight;
    
    // 이미지의 일부분을 canvas에 그리기
    ctx.drawImage(
      img,
      0, sourceYInOriginal,        // 소스 x, y (원본 이미지 좌표)
      imgWidth, sourceHeight,      // 소스 width, height
      0, 0,                        // 대상 x, y (canvas 좌표)
      imgWidth, sourceHeight       // 대상 width, height
    );
    
    const slicedImgData = canvas.toDataURL('image/png');
    pdf.addImage(slicedImgData, 'PNG', margin, yPosition, scaledWidth, heightToDraw);
    
    sourceY += heightToDraw;
    remainingHeight -= heightToDraw;
    isFirstPage = false;
  }

  return pageCount;
}

/**
 * About 페이지와 모든 게시글을 PDF로 생성
 */
export async function generatePortfolioPDF() {
  try {
    // 1. About 페이지 데이터 가져오기
    const aboutResponse = await api.get('/api/v1/board/slug/about');
    const aboutData = aboutResponse.data;

    // 2. 모든 게시글 가져오기
    const postsResponse = await api.get('/api/v1/board/');
    const posts = postsResponse.data.sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );

    // PDF 문서 생성
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
      compress: true
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    // 표지 추가
    pdf.setFontSize(32);
    pdf.setFont(undefined, 'bold');
    pdf.text('Portfolio', pageWidth / 2, 80, { align: 'center' });
    
    pdf.setFontSize(16);
    pdf.setFont(undefined, 'normal');
    const today = new Date().toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    pdf.text(today, pageWidth / 2, 100, { align: 'center' });

    // About 섹션 추가
    if (aboutData.content) {
      pdf.addPage();
      
      // 섹션 제목
      pdf.setFontSize(24);
      pdf.setFont(undefined, 'bold');
      pdf.text('About', 15, 20);
      
      // 콘텐츠를 HTML로 정규화 (Markdown이면 변환)
      const normalizedContent = normalizeContent(aboutData.content);
      
      // HTML 콘텐츠를 이미지로 변환하여 추가
      const aboutHtml = `
        <h2 style="margin-top: 0;">${aboutData.title || ''}</h2>
        ${normalizedContent}
      `;
      
      const aboutImage = await htmlToImage(aboutHtml, 750);
      await addImageToPDF(pdf, aboutImage.data, aboutImage.width, aboutImage.height, 35);
    }

    // 게시글 섹션 추가
    if (posts.length > 0) {
      pdf.addPage();
      
      // 섹션 제목
      pdf.setFontSize(24);
      pdf.setFont(undefined, 'bold');
      pdf.text('All Posts', 15, 20);
      
      let isFirstPost = true;
      
      for (let i = 0; i < posts.length; i++) {
        const post = posts[i];
        
        if (!isFirstPost) {
          pdf.addPage();
        }
        isFirstPost = false;
        
        // 게시글 제목과 메타데이터
        const createdDate = new Date(post.created_at).toLocaleDateString('ko-KR', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
        
        const tags = Array.isArray(post.tags) 
          ? post.tags.join(', ') 
          : post.tags || '';
        
        const postHeader = `
          <div style="margin-bottom: 30px;">
            <h2 style="margin: 0 0 10px 0; color: #1a1a1a;">${i + 1}. ${post.title}</h2>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">작성일: ${createdDate}</p>
            ${tags ? `<p style="margin: 5px 0; color: #3b82f6; font-size: 14px;">태그: ${tags}</p>` : ''}
          </div>
        `;
        
        // 콘텐츠를 HTML로 정규화 (Markdown이면 변환)
        const normalizedPostContent = normalizeContent(post.content);
        
        // 게시글 HTML 콘텐츠를 이미지로 변환하여 추가
        const postHtml = postHeader + normalizedPostContent;
        const postImage = await htmlToImage(postHtml, 750);
        await addImageToPDF(pdf, postImage.data, postImage.width, postImage.height, 35);
      }
    }

    // 페이지 번호 추가
    const totalPages = pdf.internal.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      pdf.setFontSize(10);
      pdf.setTextColor(150);
      pdf.text(
        `${i} / ${totalPages}`,
        pageWidth / 2,
        pageHeight - 10,
        { align: 'center' }
      );
    }

    // PDF 저장
    const fileName = `portfolio_${new Date().toISOString().split('T')[0]}.pdf`;
    pdf.save(fileName);

    return { success: true, fileName };
  } catch (error) {
    console.error('PDF 생성 실패:', error);
    throw new Error('PDF 생성에 실패했습니다.');
  }
}



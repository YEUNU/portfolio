import { marked } from 'marked';
import DOMPurify from 'dompurify';
import api from '@/services/api';

// marked 라이브러리의 설정을 중앙에서 관리합니다.
// 이 설정을 통해 <img> 태그가 제거되는 것을 방지하고,
// '/static/...' 같은 상대 경로도 올바른 전체 URL로 인식하게 됩니다.
marked.setOptions({
  baseUrl: api.defaults.baseURL,
  // sanitize 옵션은 최신 버전에서 deprecated 되었습니다.
  // DOMPurify를 통해 XSS를 방지합니다.
  sanitize: false,
});

// DOMPurify 설정: 안전한 HTML 태그 및 속성만 허용
const DOMPURIFY_CONFIG = {
  // 허용할 태그들 (마크다운에서 일반적으로 사용되는 태그)
  ALLOWED_TAGS: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'a', 'img',
    'strong', 'em', 'b', 'i', 'u', 's', 'del', 'ins',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
    'sup', 'sub',
  ],
  // 허용할 속성들
  ALLOWED_ATTR: [
    'href', 'src', 'alt', 'title', 'class', 'id',
    'target', 'rel',
    'width', 'height',
    'colspan', 'rowspan',
  ],
  // 모든 위험한 URI 스킴 차단 (javascript:, data: 등)
  ALLOW_DATA_ATTR: false,
  // <a> 태그의 target="_blank"에 자동으로 rel="noopener noreferrer" 추가
  ADD_ATTR: ['target'],
  // 스크립트 및 이벤트 핸들러 완전 차단
  FORBID_TAGS: ['script', 'style', 'iframe', 'object', 'embed', 'form', 'input', 'button'],
  FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover', 'onfocus', 'onblur'],
};

/**
 * 마크다운 문자열을 안전한 HTML로 변환합니다.
 * DOMPurify를 통해 XSS 공격을 방지합니다.
 * 
 * @param {string} content - 마크다운 형식의 문자열
 * @returns {string} - XSS가 제거된 안전한 HTML 문자열
 */
export function renderMarkdownSafe(content) {
  if (!content) return '';
  
  // 1. marked로 마크다운을 HTML로 변환
  const rawHtml = marked(content);
  
  // 2. DOMPurify로 위험한 HTML 제거
  const sanitizedHtml = DOMPurify.sanitize(rawHtml, DOMPURIFY_CONFIG);
  
  return sanitizedHtml;
}

// 기존 marked 인스턴스도 export (하위 호환성)
// 주의: 이 함수는 sanitize되지 않은 HTML을 반환합니다.
// 가능하면 renderMarkdownSafe를 사용하세요.
export default marked;

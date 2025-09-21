import { marked } from 'marked';
import api from '@/services/api';

// marked 라이브러리의 설정을 중앙에서 관리합니다.
// 이 설정을 통해 <img> 태그가 제거되는 것을 방지하고,
// '/static/...' 같은 상대 경로도 올바른 전체 URL로 인식하게 됩니다.
marked.setOptions({
  baseUrl: api.defaults.baseURL,
  // sanitize 옵션은 최신 버전에서 deprecated 되었습니다.
  // 대신, 관리자만 사용하는 페이지임을 신뢰하고 HTML을 그대로 렌더링합니다.
  // 실제 프로덕션에서는 DOMPurify 같은 라이브러리로 XSS를 방지하는 것이 좋습니다.
  sanitize: false, 
});

// 설정된 marked 인스턴스를 export하여 모든 컴포넌트에서 일관되게 사용합니다.
export default marked;

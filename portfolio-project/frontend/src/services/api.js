import axios from 'axios';

// Axios 인스턴스 생성
const api = axios.create({
  // API 기본 URL을 현재 창의 주소로 동적으로 설정합니다.
  // 이렇게 하면 localhost, 192.168.x.x 등 어떤 주소로 접속하든
  // API 요청이 올바르게 전달됩니다.
  baseURL: window.location.origin,
});

// 응답 인터셉터: 401 에러 시 자동 로그아웃 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 토큰이 만료되었거나 유효하지 않을 때
      const { useAuthStore } = require('@/store/auth');
      const authStore = useAuthStore();
      authStore.logout();

      // 로그인 페이지로 리다이렉트 (현재 페이지 정보 저장)
      if (window.location.pathname !== '/login') {
        window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`;
      }
    }
    return Promise.reject(error);
  }
);

export default api;

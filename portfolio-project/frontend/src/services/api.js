import axios from 'axios';

// Axios 인스턴스 생성
const api = axios.create({
  // API 기본 URL을 현재 창의 주소로 동적으로 설정합니다.
  // 이렇게 하면 localhost, 192.168.x.x 등 어떤 주소로 접속하든
  // API 요청이 올바르게 전달됩니다.
  baseURL: window.location.origin, 
});

export default api;


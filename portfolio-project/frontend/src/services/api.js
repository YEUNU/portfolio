import axios from 'axios';

// Axios 인스턴스 생성
const api = axios.create({
  // 백엔드 API의 기본 URL을 설정합니다.
  // Docker Compose 환경에서는 Nginx의 포트(8080)를 통해 백엔드(/api)로 프록시됩니다.
  baseURL: 'http://localhost:8080', 
});

export default api;
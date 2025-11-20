import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { useAuthStore } from './store/auth';
import './assets/styles/common.css';

const app = createApp(App);

// 1. Pinia(상태 저장소)를 먼저 앱에 등록합니다.
app.use(createPinia());

// 2. Pinia 스토어를 생성합니다.
const authStore = useAuthStore();

// 3. 앱을 최종적으로 화면에 보여주기 전에,
//    반드시 먼저 실행되어야 할 비동기 초기화 함수를 만듭니다.
async function initializeApp() {
  // localStorage에 토큰이 있다면,
  // API 통신 헤더를 설정하고 사용자 정보를 가져와서 로그인 상태를 완벽하게 복원합니다.
  await authStore.checkAuth();

  // 4. 로그인 상태 복원이 완료된 후에 라우터를 등록하고 앱을 마운트합니다.
  app.use(router);
  app.mount('#app');
}

// 초기화 함수를 실행합니다.
initializeApp();

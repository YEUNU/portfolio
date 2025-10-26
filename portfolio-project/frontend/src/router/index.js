import { createRouter, createWebHistory } from 'vue-router';
import BoardView from '../views/BoardView.vue';
import WriteView from '../views/WriteView.vue';
import LoginView from '../views/LoginView.vue';
import PostDetailView from '../views/PostDetailView.vue';
import AboutView from '../views/AboutView.vue';
import ContactView from '../views/ContactView.vue';
import { useAuthStore } from '@/store/auth';

const routes = [
  {
    path: '/',
    name: 'Board',
    component: BoardView,
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetailView,
  },
  // --- [수정] About, Contact 경로를 명시적으로 추가 ---
  // 이렇게 하면 어떤 URL이 어떤 컴포넌트와 연결되는지 명확하게 알 수 있습니다.
  {
    path: '/about',
    name: 'About',
    component: AboutView,
  },
  {
    path: '/contact',
    name: 'Contact',
    component: ContactView,
  },
  // --- 글쓰기 및 수정 경로 ---
  {
    path: '/write',
    name: 'Write',
    component: WriteView,
    meta: { requiresAdmin: true }, // 관리자만 접근 가능하도록 메타 정보 추가
  },
  {
    // 일반 게시글 수정(id)과 고정 페이지 수정(slug)을 모두 이 경로가 처리합니다.
    path: '/write/:id',
    name: 'Edit',
    component: WriteView,
    meta: { requiresAdmin: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// --- [개선] Navigation Guard: 페이지 이동 전 인증/권한 확인 ---
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // 페이지 새로고침 시 토큰은 있지만 사용자 정보가 없는 경우, 사용자 정보를 다시 가져옵니다.
  if (!authStore.isLoggedIn && authStore.token) {
    try {
      await authStore.checkAuth();
    } catch (error) {
      // 토큰이 유효하지 않으면 자동으로 로그아웃 처리합니다.
      authStore.logout();
      console.error('Authentication check failed:', error);
    }
  }

  // 이동하려는 페이지가 관리자 권한을 요구하는지 확인합니다.
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);

  // 관리자 페이지에 권한 없이 접근하려는 경우
  if (requiresAdmin && !authStore.isAdmin) {
    // 로그인 페이지로 보내고, 로그인 후 돌아올 페이지 주소를 쿼리로 남깁니다. (UX 개선)
    next({
      name: 'Login',
      query: { redirect: to.fullPath },
    });
  } else {
    // 그 외의 모든 경우는 정상적으로 페이지 이동을 허용합니다.
    next();
  }
});

export default router;

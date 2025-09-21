import { createRouter, createWebHistory } from 'vue-router';
import BoardView from '../views/BoardView.vue';
import WriteView from '../views/WriteView.vue';
import LoginView from '../views/LoginView.vue';
import PostDetailView from '../views/PostDetailView.vue';
import PageView from '../views/PageView.vue'; // ✅ PageView 컴포넌트 import
import PageEditView from '../views/PageEditView.vue'; // ✅ PageEditView 컴포넌트 import
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
  // ✅ 추가된 경로: About, Contact 등 정적 페이지를 위한 동적 라우트
  {
    path: '/:slug', 
    name: 'PageView',
    component: PageView,
  },
  {
    path: '/write',
    name: 'Write',
    component: WriteView,
    meta: { requiresAdmin: true },
  },
  {
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
  // ✅ 추가된 경로: 관리자 전용 페이지 수정 라우트
  {
    path: '/pages/edit/:slug',
    name: 'PageEdit',
    component: PageEditView,
    meta: { requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  if (!authStore.user && authStore.token) {
    await authStore.checkAuth();
  }

  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);

  if (requiresAdmin && !authStore.isAdmin) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;


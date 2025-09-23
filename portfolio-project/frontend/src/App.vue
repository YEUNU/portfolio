<template>
  <div class="app-container">
    <!-- 왼쪽 사이드바: 메인 네비게이션 -->
    <aside class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-header">
        <router-link to="/" class="site-title" @click="closeSidebar">S.Y. Portfolio</router-link>
        <!-- 모바일용 닫기 버튼 -->
        <button @click="closeSidebar" class="btn-close-sidebar">&times;</button>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <span class="nav-category" :class="{ 'category-active': isPortfolioActive }">Portfolio</span>
            <ul class="tag-list">
              <li @click="filterByTag(null)" :class="{ active: isPortfolioActive && !$route.query.tag }" class="tag-item">
                All Posts
              </li>
              <li v-for="tag in allTags" :key="tag" @click="filterByTag(tag)" :class="{ active: isPortfolioActive && $route.query.tag === tag }" class="tag-item">
                {{ tag }}
              </li>
            </ul>
          </li>
          <li>
            <router-link to="/about" class="nav-link" @click="closeSidebar">About</router-link>
          </li>
          <li>
            <router-link to="/contact" class="nav-link" @click="closeSidebar">Contact</router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 오른쪽 메인 콘텐츠 영역 -->
    <div class="main-wrapper">
      <header class="main-header">
        <!-- 모바일용 햄버거 메뉴 버튼 -->
        <button @click="toggleSidebar" class="btn-hamburger">&#9776;</button>
        <div class="header-actions">
          <div v-if="authStore.isLoggedIn && authStore.isAdmin">
            <router-link to="/write" class="btn btn-primary">글쓰기</router-link>
            <button @click="handleLogout" class="btn btn-secondary">로그아웃</button>
          </div>
          <div v-else>
            <router-link to="/login" class="btn btn-secondary">로그인</router-link>
          </div>
        </div>
      </header>
      <main class="content-area">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const allTags = ref([]);
const isSidebarOpen = ref(false);

const isPortfolioActive = computed(() => {
  return route.name === 'Board' || route.name === 'PostDetail';
});

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
const closeSidebar = () => {
  isSidebarOpen.value = false;
};

const fetchAllTags = async () => {
  try {
    const response = await api.get('/api/v1/board/tags');
    allTags.value = response.data;
  } catch (err) {
    console.error('Failed to fetch tags:', err);
  }
};

const filterByTag = (tag) => {
  router.push({ path: '/', query: tag ? { tag } : {} });
  closeSidebar();
};

const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Login' });
};

onMounted(fetchAllTags);
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: #121212;
  color: #e0e0e0;
}

.sidebar {
  width: 280px;
  background-color: #181818;
  padding: 40px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.sidebar-header {
  margin-bottom: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
}

.main-nav ul { list-style: none; padding: 0; }
.main-nav li { margin-bottom: 25px; }
.nav-category { font-size: 1.2rem; font-weight: 600; color: #a0a0a0; display: block; margin-bottom: 15px; transition: color 0.2s; }
.nav-category.category-active { color: #fff; }
.nav-link { font-size: 1.2rem; font-weight: 600; color: #a0a0a0; text-decoration: none; transition: color 0.2s; }
.nav-link.router-link-exact-active { color: #fff; }
.tag-list { list-style: none; padding-left: 15px; margin-top: 15px; }
.tag-item { color: #a0a0a0; cursor: pointer; padding: 6px 0; transition: color 0.2s; }
.tag-item:hover, .tag-item.active { color: #3d8bfd; }

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.main-header {
  display: flex;
  /* ✅ 수정: 버튼들을 오른쪽으로 정렬합니다. */
  justify-content: flex-end; 
  align-items: center;
  padding: 30px 50px;
  border-bottom: 1px solid #2a2a2a;
}
.header-actions { display: flex; align-items: center; }

.btn { padding: 10px 20px; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 500; text-decoration: none; cursor: pointer; transition: background-color 0.2s, color 0.2s; margin-left: 15px; }
.btn-primary { background-color: #3d8bfd; color: #fff; }
.btn-primary:hover { background-color: #2a79e8; }
.btn-secondary { background-color: #2a2a2a; color: #e0e0e0; }
.btn-secondary:hover { background-color: #333; }

.content-area {
  flex: 1;
  padding: 50px;
  overflow-y: auto;
}

.btn-hamburger, .btn-close-sidebar {
  display: none;
  background: none;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    transform: translateX(-100%);
    z-index: 1000;
    box-shadow: 2px 0 10px rgba(0,0,0,0.5);
  }
  .sidebar.is-open {
    transform: translateX(0);
  }
  .btn-hamburger, .btn-close-sidebar {
    display: block;
  }
  /* ✅ 수정: 모바일에서는 양쪽 정렬을 유지합니다. */
  .main-header {
    justify-content: space-between;
    padding: 20px;
  }
  .content-area {
    padding: 20px;
  }
}
</style>


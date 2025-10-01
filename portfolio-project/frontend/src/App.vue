<template>
  <div class="app-container">
    <!-- 왼쪽 사이드바: 메인 네비게이션 -->
    <aside class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-header">
        <router-link to="/" class="site-title" @click="closeSidebar">성연우의 \n포트폴리오</router-link>
        <!-- 모바일용 닫기 버튼 -->
        <button @click="closeSidebar" class="btn-close-sidebar">&times;</button>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <span class="nav-category" :class="{ 'category-active': isPortfolioActive }">Portfolio</span>
            <ul class="tag-list">
              <!-- [수정] li > router-link 구조로 변경 -->
              <li>
                <router-link :to="{ path: '/', query: {} }" class="tag-item" :class="{ active: isPortfolioActive && !$route.query.tag }" @click="closeSidebar">
                  All Posts
                </router-link>
              </li>
              <li v-for="tag in allTags" :key="tag">
                <router-link :to="{ path: '/', query: { tag: tag } }" class="tag-item" :class="{ active: isPortfolioActive && $route.query.tag === tag }" @click="filterByTag(tag)">
                  {{ tag }}
                </router-link>
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

// [수정] router.push 대신 router-link를 사용하므로, 이 함수는 이제 사이드바를 닫는 역할만 합니다.
const filterByTag = (tag) => {
  // router.push({ path: '/', query: tag ? { tag } : {} });
  closeSidebar();
};

const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Login' });
};

onMounted(fetchAllTags);
</script>

<style scoped>
/* CSS는 변경할 필요가 없습니다. */
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

/* [수정] router-link는 기본적으로 a 태그이므로, 스타일이 약간 달라질 수 있습니다. */
/* a 태그의 기본 스타일을 초기화하고 기존 스타일을 적용합니다. */
.tag-item { 
  display: block; /* a 태그를 블록 요소로 만들어 클릭 영역을 넓힙니다. */
  color: #a0a0a0; 
  cursor: pointer; 
  padding: 6px 0; 
  transition: color 0.2s;
  text-decoration: none; /* 밑줄 제거 */
}
.tag-item:hover, .tag-item.active { color: #3d8bfd; }

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.main-header {
  display: flex;
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
  .main-header {
    justify-content: space-between;
    padding: 20px;
  }
  .content-area {
    padding: 20px;
  }
}
</style>

<template>
  <div class="app-container">
    <!-- 왼쪽 사이드바: 메인 네비게이션 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link to="/" class="site-title">S.Y. Portfolio</router-link>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <span class="nav-category" :class="{ 'category-active': isPortfolioActive }">Portfolio</span>
            <!-- 태그(카테고리) 목록 -->
            <ul class="tag-list">
              <li
                @click="filterByTag(null)"
                :class="{ active: isPortfolioActive && !$route.query.tag }"
                class="tag-item"
              >
                All Posts
              </li>
              <li
                v-for="tag in allTags"
                :key="tag"
                @click="filterByTag(tag)"
                :class="{ active: isPortfolioActive && $route.query.tag === tag }"
                class="tag-item"
              >
                {{ tag }}
              </li>
            </ul>
          </li>
          <li>
            <router-link to="/about" class="nav-link">About</router-link>
          </li>
          <li>
            <router-link to="/contact" class="nav-link">Contact</router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 오른쪽 메인 콘텐츠 영역 -->
    <div class="main-wrapper">
      <header class="main-header">
        <!-- 로그인 상태에 따라 다른 버튼들을 표시 -->
        <div v-if="authStore.isLoggedIn && authStore.isAdmin">
          <router-link to="/write" class="btn btn-primary">글쓰기</router-link>
          <button @click="handleLogout" class="btn btn-secondary">로그아웃</button>
        </div>
        <div v-else>
          <router-link to="/login" class="btn btn-secondary">로그인</router-link>
        </div>
      </header>
      <main class="content-area">
        <!-- 현재 URL에 맞는 페이지 컴포넌트가 이 자리에 렌더링됨 -->
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

// 현재 경로가 포트폴리오 관련 페이지인지 확인하는 computed 속성
const isPortfolioActive = computed(() => {
  // 라우터의 이름이 'Board' 또는 'PostDetail'일 때만 true를 반환
  return route.name === 'Board' || route.name === 'PostDetail';
});


// 백엔드로부터 모든 태그 목록을 가져오는 함수
const fetchAllTags = async () => {
  try {
    const response = await api.get('/api/v1/board/tags');
    allTags.value = response.data;
  } catch (err) {
    console.error('Failed to fetch tags:', err);
  }
};

// 태그를 클릭했을 때 URL을 변경하여 필터링을 실행하는 함수
const filterByTag = (tag) => {
  router.push({ path: '/', query: tag ? { tag } : {} });
};

// 로그아웃 처리 함수
const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Login' });
};

// 컴포넌트가 처음 마운트될 때 태그 목록을 불러옴
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
}

.sidebar-header {
  margin-bottom: 50px;
}

.site-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
}

.main-nav ul {
  list-style: none;
  padding: 0;
}

.main-nav li {
  /* ✅ 수정: 메인 메뉴 그룹 간의 간격을 조정 */
  margin-bottom: 25px; 
}

.nav-category {
  font-size: 1.2rem;
  font-weight: 600;
  color: #a0a0a0;
  display: block;
  margin-bottom: 15px;
  transition: color 0.2s;
}

.nav-category.category-active {
  color: #fff;
}

.nav-link {
  font-size: 1.2rem;
  font-weight: 600;
  color: #a0a0a0;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link.router-link-exact-active {
    color: #fff;
}

.tag-list {
  list-style: none;
  padding-left: 15px;
  margin-top: 15px;
}

.tag-item {
  color: #a0a0a0;
  cursor: pointer;
  /* ✅ 수정: 태그들 사이의 간격을 미세 조정 */
  padding: 6px 0; 
  transition: color 0.2s;
}

.tag-item:hover, .tag-item.active {
  color: #3d8bfd;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 30px 50px;
  border-bottom: 1px solid #2a2a2a;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
  margin-left: 15px;
}

.btn-primary {
  background-color: #3d8bfd;
  color: #fff;
}

.btn-primary:hover {
    background-color: #2a79e8;
}

.btn-secondary {
  background-color: #2a2a2a;
  color: #e0e0e0;
}
.btn-secondary:hover {
    background-color: #333;
}

.content-area {
  flex: 1;
  padding: 50px;
  overflow-y: auto;
}
</style>


<template>
  <div class="app-container">
    <PreloadLinks />

    <aside class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-header">
        <router-link to="/" class="site-title" @click="closeSidebar">
          성연우의<br />포트폴리오
        </router-link>
        <button @click="closeSidebar" class="btn-close-sidebar" aria-label="메뉴 닫기">&times;</button>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <span class="nav-category" :class="{ 'category-active': isPortfolioActive }">Portfolio</span>
            <ul class="tag-list">
              <li>
                <router-link
                  :to="{ path: '/', query: {} }"
                  class="tag-item"
                  :class="{ active: isPortfolioActive && !$route.query.tag }"
                  @click="closeSidebar"
                >
                  <span class="tag-name">All Posts</span>
                  <span class="tag-count">{{ totalPosts }}</span> </router-link>
              </li>
              <li v-for="tag in sortedTagsWithCount" :key="tag.name">
                <router-link
                  :to="{ path: '/', query: { tag: tag.name } }"
                  class="tag-item"
                  :class="{ active: isPortfolioActive && $route.query.tag === tag.name }"
                  @click="filterByTag(tag.name)"
                >
                  <span class="tag-name">{{ tag.name }}</span>
                  <span class="tag-count">{{ tag.count }}</span> </router-link>
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

    <div v-if="isSidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>

    <div class="main-wrapper">
      <header class="main-header">
        <button @click="toggleSidebar" class="btn-hamburger" aria-label="메뉴 열기">&#9776;</button>
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
// 스크립트 부분은 변경사항 없습니다.
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import PreloadLinks from '@/components/common/PreloadLinks.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const allTags = ref([]);
const tagCounts = ref({});
const totalPosts = ref(0);
const isSidebarOpen = ref(false);

const isPortfolioActive = computed(() => {
  return route.name === 'Board' || route.name === 'PostDetail';
});

const sortedTagsWithCount = computed(() => {
  return allTags.value
    .map((tag) => ({
      name: tag,
      count: tagCounts.value[tag] || 0,
    }))
    .sort((a, b) => b.count - a.count);
});

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
const closeSidebar = () => {
  isSidebarOpen.value = false;
};

const fetchAllTags = async () => {
  try {
    const countResponse = await api.get('/api/v1/board/tags/count');
    tagCounts.value = countResponse.data;

    const tagsResponse = await api.get('/api/v1/board/tags');
    allTags.value = tagsResponse.data;

    const allPostsResponse = await api.get('/api/v1/board/');
    totalPosts.value = allPostsResponse.data.length;
  } catch (err) {
    console.error('Failed to fetch tags:', err);
  }
};

const filterByTag = (tag) => {
  closeSidebar();
};

const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Login' });
};

onUnmounted(() => {
  authStore.clearTimer();
});

onMounted(fetchAllTags);
</script>

<style scoped>
/* [개선] 전체적인 스타일 수정 */
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: #121212;
  color: #e0e0e0;
}

.sidebar {
  width: 280px;
  background-color: #181818;
  padding: 40px; /* 기존과 동일 */
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  border-right: 1px solid #2a2a2a; /* [개선] 우측에 구분선 추가 */
}

.sidebar-header {
  margin-bottom: 60px; /* [개선] 하단 여백 증가 */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.site-title {
  font-size: 2rem; /* [개선] 폰트 크기 증가 */
  font-weight: 700; /* [개선] 폰트 굵기 증가 */
  color: #ffffff;
  text-decoration: none;
  line-height: 1.3; /* [개선] 줄 간격 조정 */
}

.main-nav ul {
  list-style: none;
  padding: 0;
}
.main-nav > ul > li {
  margin-bottom: 35px; /* [개선] 메뉴 그룹 간 여백 증가 */
}
.nav-category {
  font-size: 1rem; /* [개선] 폰트 크기 조정 */
  font-weight: 600; /* [개선] 폰트 굵기 조정 */
  color: #757575; /* [개선] 기본 색상을 더 어둡게 */
  text-transform: uppercase; /* [개선] 대문자로 변경 */
  letter-spacing: 0.05em; /* [개선] 자간 추가 */
  display: block;
  margin-bottom: 20px; /* [개선] 하위 메뉴와의 여백 증가 */
  transition: color 0.3s ease;
}
.nav-category.category-active {
  color: #ffffff; /* [개선] 활성화 시 흰색으로 강조 */
}

/* [개선] About, Contact 링크 스타일 통일 */
.nav-link {
  font-size: 1.1rem; /* [개선] 폰트 크기 조정 */
  font-weight: 500;
  color: #a0a0a0;
  text-decoration: none;
  transition: color 0.3s ease;
  padding: 8px 0; /* [개선] 클릭 영역 확보 */
  display: block;
}
.nav-link:hover,
.nav-link.router-link-exact-active {
  color: #ffffff; /* [개선] 호버/활성화 시 흰색으로 변경 */
}

.tag-list {
  list-style: none;
  padding-left: 0; /* [개선] 들여쓰기 제거, 계층 구조 단순화 */
  margin-top: 15px;
  max-height: 280px; /* [개선] 최대 높이 증가 */
  overflow-y: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.tag-list::-webkit-scrollbar {
  display: none;
}

.tag-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  font-weight: 400;
  color: #a0a0a0; /* [개선] 기본 텍스트 색상 */
  cursor: pointer;
  padding: 10px 15px; /* [개선] 좌우 패딩 추가 */
  border-radius: 8px; /* [개선] 모서리 둥글게 */
  transition: color 0.3s ease, background-color 0.3s ease; /* [개선] 부드러운 전환 효과 */
  text-decoration: none;
  margin-bottom: 4px; /* [개선] 아이템 간 여백 추가 */
}

.tag-item:hover {
  color: #ffffff;
  background-color: #2a2a2a; /* [개선] 호버 시 배경색 변경 */
}

.tag-item.active {
  color: #ffffff;
  font-weight: 600; /* [개선] 활성화 시 폰트 굵게 */
  background-color: #3d8bfd; /* [개선] 활성화 시 배경색으로 강조 */
}

.tag-name {
  flex: 1;
}

.tag-count {
  font-size: 0.9em;
  background-color: #333; /* [개선] 카운트 배경색 추가 */
  color: #a0a0a0;
  padding: 2px 8px; /* [개선] 패딩 추가 */
  border-radius: 10px; /* [개선] 캡슐 형태 */
  transition: all 0.3s ease; /* [개선] 부드러운 전환 효과 */
}

.tag-item:hover .tag-count,
.tag-item.active .tag-count {
  background-color: rgba(255, 255, 255, 0.2); /* [개선] 호버/활성화 시 배경색 변경 */
  color: #ffffff;
}


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
.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
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
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.content-area::-webkit-scrollbar {
  display: none;
}

.btn-hamburger,
.btn-close-sidebar {
  display: none;
  background: none;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* [개선] 배경 어둡게 */
    z-index: 999;
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    transform: translateX(-100%);
    z-index: 1000;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
    border-right: none;
  }
  .sidebar.is-open {
    transform: translateX(0);
  }
  .btn-hamburger,
  .btn-close-sidebar {
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
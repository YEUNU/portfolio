<template>
  <div class="app-container">
    <!-- PreloadLinks 컴포넌트 추가 -->
    <PreloadLinks />

    <!-- 왼쪽 사이드바: 메인 네비게이션 -->
    <aside class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-header">
        <router-link to="/" class="site-title" @click="closeSidebar"
          >성연우의<br />포트폴리오</router-link
        >
        <!-- 모바일용 닫기 버튼 -->
        <button @click="closeSidebar" class="btn-close-sidebar" aria-label="메뉴 닫기">&times;</button>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <span class="nav-category" :class="{ 'category-active': isPortfolioActive }"
              >Portfolio</span
            >
            <ul class="tag-list">
              <!-- [수정] li > router-link 구조로 변경 -->
              <li>
                <router-link
                  :to="{ path: '/', query: {} }"
                  class="tag-item"
                  :class="{ active: isPortfolioActive && !$route.query.tag }"
                  @click="closeSidebar"
                >
                  <span class="tag-name">All Posts</span>
                  <span class="tag-count" v-if="totalPosts > 0">({{ totalPosts }})</span>
                </router-link>
              </li>
              <li v-for="tag in sortedTagsWithCount" :key="tag.name">
                <router-link
                  :to="{ path: '/', query: { tag: tag.name } }"
                  class="tag-item"
                  :class="{ active: isPortfolioActive && $route.query.tag === tag.name }"
                  @click="filterByTag(tag.name)"
                >
                  <span class="tag-name">{{ tag.name }}</span>
                  <span class="tag-count">({{ tag.count }})</span>
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

    <!-- 사이드바 오버레이 -->
    <div v-if="isSidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>

    <!-- 오른쪽 메인 콘텐츠 영역 -->
    <div class="main-wrapper">
      <header class="main-header">
        <!-- 모바일용 햄버거 메뉴 버튼 -->
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
    .sort((a, b) => b.count - a.count); // 포스팅 개수가 많은 순으로 정렬
});

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
const closeSidebar = () => {
  isSidebarOpen.value = false;
};



const fetchAllTags = async () => {
  try {
    // 태그별 개수 정보 가져오기
    const countResponse = await api.get('/api/v1/board/tags/count');
    tagCounts.value = countResponse.data;

    // 기존 태그 목록 가져오기
    const tagsResponse = await api.get('/api/v1/board/tags');
    allTags.value = tagsResponse.data;

    // 전체 포스팅 개수를 위한 API 호출
    const allPostsResponse = await api.get('/api/v1/board/');
    totalPosts.value = allPostsResponse.data.length;
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

// 컴포넌트 언마운트 시 타이머 정리
onUnmounted(() => {
  authStore.clearTimer();
});

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

.main-nav ul {
  list-style: none;
  padding: 0;
}
.main-nav > ul > li {
  margin-bottom: 25px;
}
.nav-category {
  font-size: 1.3rem;
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
  font-size: 1.3rem;
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
  padding-left: 25px; /* 들여쓰기 증가 */
  margin-top: 15px;
  max-height: 250px; /* 최대 높이 설정 */
  overflow-y: auto; /* 높이 초과 시 스크롤바 표시 */
}

/* [수정] router-link는 기본적으로 a 태그이므로, 스타일이 약간 달라질 수 있습니다. */
/* a 태그의 기본 스타일을 초기화하고 기존 스타일을 적용합니다. */
.tag-item {
  display: flex; /* flexbox로 변경하여 태그명과 개수를 양쪽 정렬 */
  justify-content: space-between; /* 태그명과 개수를 양쪽 끝에 정렬 */
  align-items: center;
  font-size: 1.1rem; /* 하위 메뉴 폰트 크기 조정 */
  font-weight: 400; /* 하위 메뉴 폰트 굵기 조정 */
  color: #a0a0a0;
  cursor: pointer;
  padding: 6px 0;
  transition: color 0.2s;
  text-decoration: none; /* 밑줄 제거 */
}
.tag-item:hover,
.tag-item.active {
  color: #3d8bfd;
}

.tag-name {
  flex: 1; /* 태그명이 남은 공간을 차지 */
}

.tag-count {
  font-size: 0.85em;
  opacity: 0.7;
  margin-left: 8px;
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
    background-color: rgba(0, 0, 0, 0.2); /* 약간 어두운 배경 */
    z-index: 999; /* 사이드바(1000) 바로 아래 */
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    transform: translateX(-100%);
    z-index: 1000;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
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

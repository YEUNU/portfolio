<template>
  <div class="page-view">
    <!-- 로딩 중일 때 표시될 스피너 -->
    <div v-if="loading" class="loading-spinner"></div>

    <!-- 에러 발생 시 메시지 표시 -->
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- 페이지 콘텐츠가 성공적으로 로드되었을 때 -->
    <div v-if="page && !loading && !error" class="page-content">
      <div class="page-header">
        <h1 class="page-title">{{ page.title }}</h1>
        <!-- 관리자일 경우에만 수정 버튼 표시 -->
        <button v-if="authStore.isAdmin" @click="goToEditPage" class="btn-edit">
          수정하기
        </button>
      </div>
      <!-- 중앙 설정된 marked를 통해 렌더링된 콘텐츠 -->
      <div class="markdown-content" v-html="compiledMarkdown"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import marked from '@/utils/markdown'; // ✅ 수정: 중앙 설정된 marked 인스턴스 import
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const page = ref(null);
const loading = ref(true);
const error = ref(null);

// 중앙 설정된 marked를 사용하여 Markdown 콘텐츠를 HTML로 변환
const compiledMarkdown = computed(() => {
  if (page.value && page.value.content) {
    return marked(page.value.content);
  }
  return '';
});

// slug를 기반으로 페이지 데이터를 가져오는 함수
const fetchPage = async (slug) => {
  try {
    loading.value = true;
    error.value = null;
    const response = await api.get(`/api/v1/pages/${slug}`);
    page.value = response.data;
  } catch (err) {
    console.error(`Failed to fetch page ${slug}:`, err);
    error.value = '페이지를 불러오는 데 실패했습니다.';
    page.value = null;
  } finally {
    loading.value = false;
  }
};

// 수정 페이지로 이동하는 함수
const goToEditPage = () => {
  if (page.value) {
    router.push({ name: 'PageEdit', params: { slug: page.value.slug } });
  }
};

// 컴포넌트가 마운트될 때 현재 라우트의 slug로 데이터를 가져옴
onMounted(() => {
  // slug 파라미터가 있는지 확인 (About/Contact 페이지의 경우)
  if (route.params.slug) {
    fetchPage(route.params.slug);
  }
});

// 라우트의 slug가 변경될 때마다 데이터를 다시 가져옴 (e.g., /about -> /contact)
watch(
  () => route.params.slug,
  (newSlug) => {
    if (newSlug) {
      fetchPage(newSlug);
    }
  }
);
</script>

<style scoped>
.page-view {
  color: #e0e0e0;
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fff;
}

.btn-edit {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  background-color: #3d8bfd;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-edit:hover {
  background-color: #2a79e8;
}

.markdown-content {
  line-height: 1.7;
}

/* Markdown 스타일링 */
.markdown-content :deep(h2) {
  font-size: 1.8rem;
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
}
.markdown-content :deep(p) {
  margin-bottom: 1rem;
}
.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 2rem 0;
  display: block;
}
.markdown-content :deep(ul) {
  padding-left: 20px;
}
.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
}
.markdown-content :deep(a) {
  color: #3d8bfd;
  text-decoration: none;
}
.markdown-content :deep(a:hover) {
  text-decoration: underline;
}
.markdown-content :deep(strong) {
  font-weight: bold;
}
</style>


<template>
  <div class="post-detail-view">
    <!-- 로딩 중일 때 표시될 스피너 -->
    <div v-if="loading" class="loading-spinner"></div>

    <!-- 에러 발생 시 메시지 표시 -->
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- 콘텐츠가 성공적으로 로드되었을 때 -->
    <div v-if="post && !loading && !error" class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      <p class="post-meta">
        <span class="tags">{{ post.tags }}</span>
        <span class="date">{{ formattedDate }}</span>
      </p>
      <!-- 중앙 설정된 marked를 통해 렌더링된 콘텐츠 -->
      <div class="markdown-content" v-html="compiledMarkdown"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import marked from '@/utils/markdown'; // ✅ 수정: 중앙 설정된 marked 인스턴스 import
import api from '@/services/api';

const route = useRoute();
const post = ref(null);
const loading = ref(true);
const error = ref(null);

// 중앙 설정된 marked를 사용하여 Markdown 콘텐츠를 HTML로 변환
const compiledMarkdown = computed(() => {
  if (post.value && post.value.content) {
    return marked(post.value.content);
  }
  return '';
});

// 날짜 형식을 'YYYY. M. D.' 형태로 변환
const formattedDate = computed(() => {
  if (post.value && post.value.created_at) {
    return new Date(post.value.created_at).toLocaleDateString('ko-KR');
  }
  return '';
});

// 컴포넌트가 마운트될 때 URL의 ID를 기반으로 게시글 데이터를 가져옴
onMounted(async () => {
  try {
    const postId = route.params.id;
    const response = await api.get(`/api/v1/board/${postId}`);
    post.value = response.data;
  } catch (err) {
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.post-detail-view {
  color: #e0e0e0;
  width: 100%;
  max-width: 800px; /* 콘텐츠 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
}

.post-title {
  font-size: 3rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.post-meta {
  color: #757575;
  margin-bottom: 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  padding-bottom: 1.5rem;
}

.markdown-content {
  line-height: 1.8;
  font-size: 1.1rem;
}

/* Markdown으로 변환된 HTML 요소들에 대한 스타일링 */
.markdown-content :deep(h2) {
  font-size: 2rem;
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.markdown-content :deep(p) {
  margin-bottom: 1.2rem;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 2rem 0;
  display: block;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  padding-left: 25px;
  margin-bottom: 1.2rem;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #3d8bfd;
  margin: 1.5rem 0;
  padding: 0.5rem 1.5rem;
  color: #a0a0a0;
  background-color: #1c1c1c;
}

.markdown-content :deep(code) {
  background-color: #2a2a2a;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}

.markdown-content :deep(pre) {
  background-color: #2a2a2a;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}

.markdown-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}
</style>


<template>
  <div class="post-detail-view">
    <div v-if="loading" class="loading-spinner"></div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="post && !loading && !error" class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      <p class="post-meta">
        <span class="tags">{{ post.tags }}</span>
        <span class="date">{{ formattedDate }}</span>
      </p>
      <div class="markdown-content" v-html="compiledMarkdown"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import marked from '@/utils/markdown';
import api from '@/services/api';

const route = useRoute();
const post = ref(null);
const loading = ref(true);
const error = ref(null);

const compiledMarkdown = computed(() => {
  if (post.value && post.value.content) {
    return marked(post.value.content);
  }
  return '';
});

const formattedDate = computed(() => {
  if (post.value && post.value.created_at) {
    return new Date(post.value.created_at).toLocaleDateString('ko-KR');
  }
  return '';
});

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
  max-width: 800px;
  margin: 0 auto;
}
.post-title {
  font-size: 3rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 1rem;
}
.post-meta {
  color: #757575;
  margin-bottom: 3rem;
  display: flex;
  justify-content: space-between;
}
.markdown-content {
  line-height: 1.8;
  font-size: 1.1rem;
}
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
}
.markdown-content :deep(ul) {
  padding-left: 20px;
}

@media (max-width: 768px) {
  .post-title {
    font-size: 2.2rem;
  }
  .markdown-content {
    font-size: 1rem;
  }
}
</style>


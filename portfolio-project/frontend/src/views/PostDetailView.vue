<template>
  <div class="post-detail-view">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="post">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span>작성일: {{ formattedDate }}</span>
        <span>작성자: {{ post.author }}</span>
      </div>
      <MarkdownPreview :content="post.content" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';

const route = useRoute();
const post = ref(null);
const loading = ref(true);
const error = ref(null);

const formattedDate = computed(() => {
  if (post.value?.created_at) {
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
    console.error(err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.post-detail-view {
  color: var(--color-text);
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.post-title {
  font-size: 3rem;
  font-weight: bold;
  color: var(--color-text);
  margin-bottom: var(--spacing-sm);
}

.post-meta {
  color: var(--color-text-dark);
  margin-bottom: var(--spacing-xl);
  display: flex;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .post-title {
    font-size: 2.2rem;
  }

  .post-detail-view {
    padding: var(--spacing-md);
  }
}
</style>
<template>
  <div class="page-container about-view">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="post">
      <!-- 수정하기 버튼 -->
      <div class="edit-button-wrapper">
        <!-- 
          [핵심 수정]
          단순히 /write로 이동하는 대신,
          'about'이라는 파라미터를 가지고 Write 페이지로 이동합니다.
          이제 WriteView는 route.params.id 값이 'about'인 것을 알 수 있습니다.
        -->
        <router-link :to="{ name: 'Write', params: { id: 'about' } }" class="edit-button">
          수정하기
        </router-link>
      </div>

      <h1 class="post-title">{{ post.title }}</h1>
      <MarkdownPreview :content="post.content" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';

const post = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    // 백엔드 API에서 고정된 페이지를 slug('about')로 조회합니다.
    const response = await api.get(`/api/v1/board/slug/about`);
    post.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = '페이지를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.about-view {
  position: relative;
  color: var(--color-text);
}

.edit-button-wrapper {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
}

.edit-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: var(--color-primary-hover);
}

.post-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: var(--spacing-xl);
}
</style>

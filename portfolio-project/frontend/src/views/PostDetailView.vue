<template>
  <div class="page-container post-detail-view">
    <div v-if="loading" class="loading">
      게시글을 불러오는 중입니다...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <article v-else-if="post">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span v-if="post.author">작성자: {{ post.author }}</span>
        <span v-if="formattedDate">작성일: {{ formattedDate }}</span>
      </div>
      <MarkdownPreview :content="post.content" />
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';
import { useMeta } from '@/composables/useMeta';

const route = useRoute();
const post = ref(null);
const loading = ref(true);
const error = ref(null);
const { updateMeta, addStructuredData } = useMeta();

// 날짜 포맷팅 computed 속성은 그대로 유지합니다.
const formattedDate = computed(() => {
  if (post.value?.created_at) {
    return new Date(post.value.created_at).toLocaleDateString('ko-KR');
  }
  return '';
});

// 데이터 로딩 로직을 별도 함수로 분리하여 재사용성을 높입니다.
const fetchPost = async (postId) => {
  loading.value = true;
  error.value = null;
  post.value = null; // 새 게시글 로딩 전 이전 데이터를 초기화합니다.
  try {
    const response = await api.get(`/api/v1/board/${postId}`);
    post.value = response.data;
    updatePostMeta(response.data);
  } catch (err) {
    console.error(`Failed to fetch post ${postId}:`, err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

const updatePostMeta = (postData) => {
  // 게시글의 첫 번째 이미지 찾기
  const getFirstImage = (content) => {
    const regex = /!\[.*?]\((.*?)\)/;
    const match = content.match(regex);
    if (match && match[1]) {
      const imageUrl = match[1];
      return imageUrl.startsWith('/') ? `${api.defaults.baseURL}${imageUrl}` : imageUrl;
    }
    return '/og-image.jpg';
  };

  // 메타 설명을 위한 텍스트 추출 (마크다운 제거)
  const getDescriptionFromContent = (content) => {
    return content
      .replace(/[#*()[\]]/g, '') // 마크다운 문법 제거
      .substring(0, 160) // 160자로 제한
      .trim();
  };

  const title = `${postData.title} - 성연우의 포트폴리오`;
  const description = getDescriptionFromContent(postData.content);
  const ogImage = getFirstImage(postData.content);

  updateMeta({
    title,
    description,
    keywords: `성연우, 포트폴리오, ${postData.title}, ${postData.tags || '개발자'}`,
    canonical: `https://your-domain.com/post/${postData.id}`,
    ogImage
  });

  // 게시글 구조화된 데이터
  addStructuredData({
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": postData.title,
    "description": description,
    "author": {
      "@type": "Person",
      "name": "성연우"
    },
    "datePublished": postData.created_at,
    "dateModified": postData.updated_at || postData.created_at,
    "url": `https://your-domain.com/post/${postData.id}`,
    "image": ogImage,
    "keywords": postData.tags
  });
};

// 컴포넌트가 처음 마운트될 때 게시글을 불러옵니다.
onMounted(() => {
  fetchPost(route.params.id);
});

// (가장 중요한 변경점)
// 다른 게시글로 이동할 때 컴포넌트가 재사용되므로, id 변경을 감지하여 데이터를 다시 불러옵니다.
watch(
  () => route.params.id,
  (newId, oldId) => {
    // newId가 존재하고 이전 id와 다를 경우에만 데이터를 새로 가져옵니다.
    if (newId && newId !== oldId) {
      fetchPost(newId);
    }
  }
);
</script>

<style scoped>
/* .page-container에서 레이아웃을 담당하므로 중복되는 스타일은 제거합니다. */
.post-detail-view {
  color: var(--color-text);
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
  /* space-between 대신 gap을 사용해 일관된 간격을 유지합니다. */
  gap: 1rem;
  flex-wrap: wrap; /* 화면이 좁아지면 줄바꿈 처리 */
}

/* 로딩 및 에러 메시지 스타일 추가 */
.loading, .error {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-text-dark);
}

@media (max-width: 768px) {
  .post-title {
    font-size: 2.2rem;
  }
}
</style>
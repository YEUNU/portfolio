<template>
  <div class="board-view">
    <h1 class="page-title">{{ pageTitle }}</h1>
    <div v-if="loading" class="loading-spinner"></div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="!loading && !error" class="posts-grid">
      <div v-for="post in posts" :key="post.id" class="post-card" @click="viewPost(post.id)">
        <div
          class="post-thumbnail"
          :style="
            getFirstImage(post.content)
              ? { backgroundImage: `url(${getFirstImage(post.content)})` }
              : {}
          "
        ></div>
        <div class="post-info">
          <h2 class="post-title">{{ post.title }}</h2>
          <p class="post-tags">{{ post.tags }}</p>
          <div v-if="authStore.isAdmin" class="admin-actions">
            <button @click.stop="editPost(post.id)" class="btn-edit">수정</button>
            <button @click.stop="deletePost(post.id)" class="btn-delete">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import { useMeta } from '@/composables/useMeta';

const posts = ref([]);
const loading = ref(true);
const error = ref(null);
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const { updateMeta, addStructuredData } = useMeta();

const pageTitle = computed(() => {
  return route.query.tag ? `# ${route.query.tag}` : 'All Posts';
});

const getFirstImage = (content) => {
  if (!content) return null;
  const regex = /!\[.*?]\((.*?)\)/;
  const match = content.match(regex);
  if (match && match[1]) {
    const imageUrl = match[1];
    if (imageUrl.startsWith('/')) {
      return `${api.defaults.baseURL}${imageUrl}`;
    }
    return imageUrl;
  }
  return null;
};

const fetchPosts = async () => {
  try {
    loading.value = true;
    let url = '/api/v1/board/';
    if (route.query.tag) {
      url += `?tags=${route.query.tag}`;
    }
    const response = await api.get(url);
    const fetchedPosts = response.data;

    fetchedPosts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    posts.value = fetchedPosts;
    error.value = null;
  } catch (err) {
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

watch(
  () => route.query.tag,
  () => {
    fetchPosts();
    updatePageMeta();
  }
);

onMounted(() => {
  fetchPosts();
  updatePageMeta();
});

const updatePageMeta = () => {
  const tag = route.query.tag;
  const title = tag ? `${tag} - 성연우의 포트폴리오` : '성연우의 포트폴리오 | 개발자 포트폴리오';
  const description = tag
    ? `${tag} 관련 프로젝트들을 확인해보세요.`
    : '성연우의 개발자 포트폴리오입니다. 다양한 웹 개발 프로젝트들을 확인해보세요.';

  updateMeta({
    title,
    description,
    keywords: tag
      ? `성연우, 포트폴리오, ${tag}, 개발자`
      : '성연우, 포트폴리오, 개발자, 웹개발, 프론트엔드, 백엔드',
    canonical: tag ? `https://your-domain.com/?tag=${tag}` : 'https://your-domain.com',
  });

  // 구조화된 데이터 추가
  if (!tag) {
    addStructuredData({
      '@context': 'https://schema.org',
      '@type': 'Portfolio',
      name: '성연우의 포트폴리오',
      description: '웹 개발자 성연우의 포트폴리오 사이트',
      author: {
        '@type': 'Person',
        name: '성연우',
      },
      url: 'https://your-domain.com',
    });
  }
};

const viewPost = (id) => {
  router.push({ name: 'PostDetail', params: { id } });
};

const editPost = (id) => {
  router.push({ name: 'Edit', params: { id } });
};

const deletePost = async (id) => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/v1/board/${id}`);
      fetchPosts();
    } catch (err) {
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};
</script>

<style scoped>
.board-view {
  width: 100%;
}
.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 30px;
}
.posts-grid {
  display: grid;
  /* 모바일에서는 1열, PC에서는 여러 열로 보이도록 변경 */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}
.post-card {
  background-color: #1e1e1e;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  cursor: pointer;
}
.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
.post-thumbnail {
  width: 100%;
  height: 200px;
  background-color: #333;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.post-info {
  padding: 20px;
}
.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 10px 0;
  color: #f0f0f0;
}
.post-tags {
  font-size: 0.9rem;
  color: #757575;
  margin-bottom: 15px;
}
.admin-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.btn-edit,
.btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}
.btn-edit {
  background-color: #3d8bfd;
  color: white;
}
.btn-delete {
  background-color: #e53935;
  color: white;
}
.loading-spinner,
.error-message {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
}
/* 모바일 화면에서 제목 크기 조정 */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
}
</style>

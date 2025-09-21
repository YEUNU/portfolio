<template>
  <div class="board-view">
    <h1 class="page-title">{{ pageTitle }}</h1>

    <div v-if="loading" class="loading-spinner"></div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && !error" class="posts-grid">
      <!-- ✅ 수정된 부분: 게시글 카드를 클릭하면 viewPost 함수 실행 -->
      <div v-for="post in posts" :key="post.id" class="post-card" @click="viewPost(post.id)">
        <div class="post-thumbnail"></div>
        <div class="post-info">
          <h2 class="post-title">{{ post.title }}</h2>
          <p class="post-tags">{{ post.tags }}</p>
          <div v-if="authStore.isAdmin" class="admin-actions">
            <!-- ✅ 수정된 부분: 버튼 클릭 시 상위 요소의 클릭 이벤트 전파 중단 -->
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

const posts = ref([]);
const loading = ref(true);
const error = ref(null);
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const pageTitle = computed(() => {
  return route.query.tag ? `# ${route.query.tag}` : 'All Posts';
});

const fetchPosts = async () => {
  try {
    loading.value = true;
    let url = '/api/v1/board/';
    if (route.query.tag) {
      url += `?tags=${route.query.tag}`;
    }
    const response = await api.get(url);
    posts.value = response.data;
    error.value = null;
  } catch (err) {
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

watch(() => route.query.tag, fetchPosts);

onMounted(fetchPosts);

// ✅ 추가된 함수: 게시글 상세 보기 페이지로 이동
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
/* 스타일은 기존과 동일하게 유지됩니다. */
.board-view {
  width: 100%;
}
.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 30px;
}
.loading-spinner, .error-message {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
}
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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
.btn-edit, .btn-delete {
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
</style>


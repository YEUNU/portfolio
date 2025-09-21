<template>
  <div class="board-view">
    <!-- ✅ 수정: 페이지 타이틀을 동적으로 표시하도록 변경 -->
    <h1 class="page-title">{{ pageTitle }}</h1>
    <div v-if="loading" class="loading-spinner"></div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="!loading && !error" class="posts-grid">
      <div v-for="post in posts" :key="post.id" class="post-card" @click="viewPost(post.id)">
        <div
          class="post-thumbnail"
          :style="getFirstImage(post.content) ? { backgroundImage: `url(${getFirstImage(post.content)})` } : {}"
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
// ✅ watch와 computed를 import하여 동적 데이터 처리를 강화합니다.
import { ref, onMounted, watch, computed } from 'vue'; 
// ✅ useRoute를 import하여 URL의 변화를 감지합니다.
import { useRouter, useRoute } from 'vue-router'; 
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

const posts = ref([]);
const loading = ref(true);
const error = ref(null);
const router = useRouter();
const route = useRoute(); // ✅ route 객체를 가져와 현재 URL 정보에 접근합니다.
const authStore = useAuthStore();

// ✅ 추가: URL 쿼리에 따라 페이지 타이틀을 동적으로 계산합니다.
const pageTitle = computed(() => {
  return route.query.tag ? `# ${route.query.tag}` : 'All Posts';
});

const getFirstImage = (content) => {
  if (!content) return null;
  const regex = /!\[.*?\]\((.*?)\)/;
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

// ✅ 수정: fetchPosts 함수가 App.vue로부터 전달된 URL 쿼리(?tag=...)를 사용하도록 변경합니다.
const fetchPosts = async () => {
  try {
    loading.value = true;
    let url = '/api/v1/board/';
    if (route.query.tag) {
      url += `?tags=${route.query.tag}`;
    }
    const response = await api.get(url);
    const fetchedPosts = response.data;
    
    // ✅ 추가: 게시글을 생성 시간(created_at) 기준으로 내림차순 정렬 (최신순)
    fetchedPosts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    posts.value = fetchedPosts;
    error.value = null;
  } catch (err) {
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

// ✅ 추가: URL의 태그 필터가 변경될 때마다 게시물 목록을 새로고침합니다.
watch(() => route.query.tag, fetchPosts);

onMounted(fetchPosts);

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
      // 태그 목록 갱신은 App.vue에서 처리해야 합니다 (추후 개선).
    } catch (err) {
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};
</script>

<style scoped>
/* ✅ 수정: 불필요한 스타일(sidebar, board-container 등)을 모두 제거하고 정리합니다. */
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
.loading-spinner, .error-message {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
}
</style>


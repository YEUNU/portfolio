<template>
  <div class="board-view">
    <h1 class="page-title">{{ pageTitle }}</h1>

    <!-- [개선] 로딩 스피너 UI 추가 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
    </div>
    
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <div v-else-if="posts.length > 0" class="posts-grid">
      <router-link
        v-for="post in posts"
        :key="post.id"
        :to="{ name: 'PostDetail', params: { id: post.id } }"
        class="post-card-link"
      >
        <article class="post-card">
          <div class="card-thumbnail">
            <!-- [개선] alt 속성도 null-safe하게 변경 -->
            <img :src="getThumbnailUrl(post)" :alt="`${post ? post.title : '게시물'} 썸네일`" />
          </div>
          <div class="card-content">
            <h2 class="card-title">{{ post.title }}</h2>
            <div class="card-tags">
              <span v-for="tag in post.processedTags" :key="tag" class="tag">{{ tag }}</span>
            </div>
            <div v-if="authStore.isAdmin" class="admin-actions">
              <button @click.prevent.stop="editPost(post.id)" class="btn-edit">수정</button>
              <!-- [개선] confirm() 대신 커스텀 모달을 열도록 변경 -->
              <button @click.prevent.stop="openDeleteModal(post.id, post.title)" class="btn-delete">삭제</button>
            </div>
          </div>
        </article>
      </router-link>
    </div>

    <div v-else class="no-posts">
      <p>게시물이 없습니다.</p>
    </div>

    <!-- [신규] 삭제 확인 커스텀 모달 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">삭제 확인</h3>
        <p class="modal-text">
          정말로 '<strong>{{ postToDelete.title }}</strong>' 게시글을 삭제하시겠습니까?<br/>
          이 작업은 되돌릴 수 없습니다.
        </p>
        <div class="modal-actions">
          <button @click="closeDeleteModal" class="btn btn-secondary">취소</button>
          <button @click="handleDeleteConfirm" class="btn btn-danger">삭제</button>
        </div>
      </div>
    </div>

    <!-- [신규] 오류 알림 커스텀 모달 -->
    <div v-if="showErrorModal" class="modal-overlay" @click="closeErrorModal">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">오류 발생</h3>
        <p class="modal-text">{{ errorMessage }}</p>
        <div class="modal-actions">
          <button @click="closeErrorModal" class="btn btn-primary">확인</button>
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

const defaultThumbnail = '/images/default-thumbnail.png';

// --- [신규] 모달 상태 관리 ---
const showDeleteModal = ref(false);
const postToDelete = ref({ id: null, title: '' });

const showErrorModal = ref(false);
const errorMessage = ref('');
// ----------------------------

const pageTitle = computed(() => {
  return route.query.tag ? `# ${route.query.tag}` : 'All Posts';
});

const getThumbnailUrl = (post) => {
  if (!post) {
    return defaultThumbnail;
  }
  if (post.thumbnail_url) {
    return post.thumbnail_url;
  }
  if (typeof post.content === 'string') {
    const regex = /!\[.*?\]\((.*?)\)/;
    const match = post.content.match(regex);
    if (match && match[1]) {
      const imageUrl = match[1];
      return imageUrl.startsWith('/') ? `${api.defaults.baseURL}${imageUrl}` : imageUrl;
    }
  }
  return defaultThumbnail;
};

const fetchPosts = async () => {
  try {
    loading.value = true;
    error.value = null;
    const tag = route.query.tag;
    const url = tag ? `/api/v1/board/?tags=${tag}` : '/api/v1/board/';
    const response = await api.get(url);

    const fetchedPosts = response.data.map(post => ({
      ...post,
      processedTags: typeof post.tags === 'string'
        ? post.tags.split(',').map(t => t.trim()).filter(t => t)
        : (post.tags || [])
    }));

    fetchedPosts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    posts.value = fetchedPosts;

  } catch (err) {
    console.error('Failed to fetch posts:', err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

const updatePageMeta = () => {
  // This function is intentionally left empty.
};

watch(() => route.query.tag, () => {
  fetchPosts();
  updatePageMeta();
}, { immediate: true });

const editPost = (id) => {
  router.push({ name: 'Edit', params: { id } });
};

// --- [신규] 모달 제어 함수 ---
const openDeleteModal = (id, title) => {
  postToDelete.value = { id, title };
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  postToDelete.value = { id: null, title: '' };
};

const openErrorModal = (message) => {
  errorMessage.value = message;
  showErrorModal.value = true;
};

const closeErrorModal = () => {
  showErrorModal.value = false;
  errorMessage.value = '';
};
// ----------------------------

// [개선] 삭제 로직을 별도 함수로 분리
const handleDeleteConfirm = async () => {
  if (!postToDelete.value.id) return;

  try {
    await api.delete(`/api/v1/board/${postToDelete.value.id}`);
    posts.value = posts.value.filter(p => p.id !== postToDelete.value.id);
    closeDeleteModal(); // 성공 시 모달 닫기
  } catch (err) {
    console.error('Failed to delete post:', err);
    closeDeleteModal(); // 삭제 모달 닫기
    // [개선] alert() 대신 에러 모달 열기
    openErrorModal('게시글 삭제에 실패했습니다. 다시 시도해주세요.');
  }
};
</script>

<style scoped>
/* --- 기존 스타일 ... --- */
.board-view {
  width: 100%;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #f0f0f0;
  margin-bottom: 40px;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 40px;
}

.post-card-link {
  text-decoration: none;
  color: inherit;
}

.post-card {
  background-color: #1c1c1c;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #2a2a2a;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 30px rgba(0, 0, 0, 0.3);
}

.card-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  background-color: #2a2a2a;
  overflow: hidden;
}

.card-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.post-card:hover .card-thumbnail img {
  transform: scale(1.05);
}

.card-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  background-color: #333;
  color: #bdbdbd;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.admin-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.btn-edit,
.btn-delete {
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-edit {
  background-color: #3d8bfd;
  color: white;
}
.btn-edit:hover { background-color: #2a79e8; }

.btn-delete {
  background-color: #4a4a4a;
  color: #e0e0e0;
}
.btn-delete:hover { background-color: #e53935; }


.error-message, .no-posts {
  text-align: center;
  padding: 80px 0;
  color: #757575;
  font-size: 1.1rem;
}

/* --- [신규] 로딩 스피너 스타일 --- */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 80px 0;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #333; /* 스피너 트랙 */
  border-top-color: #3d8bfd; /* 스피너 색상 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* --- [신규] 커스텀 모달 스타일 --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background-color: #2a2a2a;
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid #444;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #f0f0f0;
  margin: 0 0 15px 0;
}

.modal-text {
  font-size: 1rem;
  color: #bdbdbd;
  line-height: 1.6;
  margin-bottom: 30px;
}
.modal-text strong {
  color: #f0f0f0;
  font-weight: 600;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* --- [신규] 공용 버튼 스타일 --- */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.btn-primary {
  background-color: #3d8bfd;
  color: #fff;
}
.btn-primary:hover { background-color: #2a79e8; }

.btn-secondary {
  background-color: #4a4a4a;
  color: #e0e0e0;
}
.btn-secondary:hover { background-color: #5a5a5a; }

.btn-danger {
  background-color: #e53935;
  color: #fff;
}
.btn-danger:hover { background-color: #c62828; }
</style>
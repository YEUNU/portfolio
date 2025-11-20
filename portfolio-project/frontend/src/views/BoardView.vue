<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page Title -->
    <div class="mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-primary dark:text-primary-dark mb-2 animate-fade-in">
        {{ pageTitle }}
      </h1>
      <div class="h-1 w-20 bg-primary dark:bg-primary-dark rounded-md3-full"></div>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-surface-variant dark:border-surface-dark-variant border-t-primary rounded-full animate-spin"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-b-primary-300 dark:border-b-primary-700 rounded-full animate-spin" style="animation-direction: reverse; animation-duration: 1s;"></div>
      </div>
    </div>
    
    <!-- Error Message -->
    <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[400px] space-y-4">
      <svg class="w-20 h-20 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xl text-surface-on-variant dark:text-surface-dark-on">{{ error }}</p>
    </div>

    <!-- Posts Grid -->
    <div v-else-if="posts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        :showAdmin="authStore.isAdmin"
        @click="router.push({ name: 'PostDetail', params: { id: post.id } })"
        @edit="editPost(post.id)"
        @delete="openDeleteModal(post.id, post.title)"
      />
    </div>

    <!-- No Posts Message -->
    <div v-else class="flex flex-col items-center justify-center min-h-[400px] space-y-6">
      <div class="relative">
        <svg class="w-32 h-32 text-surface-on-variant dark:text-surface-dark-on" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <div class="absolute inset-0 bg-primary/10 blur-3xl"></div>
      </div>
      <div class="text-center space-y-2">
        <p class="text-2xl font-medium text-surface-on dark:text-surface-dark-on">게시물이 없습니다</p>
        <p class="text-surface-on-variant dark:text-surface-dark-on">첫 번째 게시물을 작성해보세요!</p>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div 
      v-if="showDeleteModal" 
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in"
      @click="closeDeleteModal"
    >
      <div 
        class="bg-surface dark:bg-surface-dark rounded-md3-xl p-6 max-w-md w-full shadow-md3-5 border border-outline/20 dark:border-outline-dark/20 transform transition-all duration-300 scale-100"
        @click.stop
      >
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-error-container dark:bg-error-dark-container rounded-md3-sm">
            <svg class="w-6 h-6 text-error-on-container" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-surface-on dark:text-surface-dark-on">삭제 확인</h3>
        </div>
        <p class="text-surface-on dark:text-surface-dark-on mb-6">
          정말로 '<span class="font-semibold">{{ postToDelete.title }}</span>' 게시글을 삭제하시겠습니까?<br/>
          <span class="text-sm text-error">이 작업은 되돌릴 수 없습니다.</span>
        </p>
        <div class="flex gap-3">
          <button 
            @click="closeDeleteModal" 
            class="flex-1 px-4 py-2.5 bg-surface-variant dark:bg-surface-dark-variant hover:bg-outline/20 dark:hover:bg-outline-dark/20 text-surface-on dark:text-surface-dark-on font-medium rounded-md3-full transition-all duration-200"
          >
            취소
          </button>
          <button 
            @click="handleDeleteConfirm" 
            class="flex-1 px-4 py-2.5 bg-error hover:bg-error-dark dark:bg-error-dark dark:hover:bg-error text-error-on font-medium rounded-md3-full shadow-md3-2 hover:shadow-md3-3 transition-all duration-200"
          >
            삭제
          </button>
        </div>
      </div>
    </div>

    <!-- Error Alert Modal -->
    <div 
      v-if="showErrorModal" 
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in"
      @click="closeErrorModal"
    >
      <div 
        class="bg-surface dark:bg-surface-dark rounded-md3-xl p-6 max-w-md w-full shadow-md3-5 border border-outline/20 dark:border-outline-dark/20"
        @click.stop
      >
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-error-container dark:bg-error-dark-container rounded-md3-sm">
            <svg class="w-6 h-6 text-error-on-container" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-surface-on dark:text-surface-dark-on">오류 발생</h3>
        </div>
        <p class="text-surface-on dark:text-surface-dark-on mb-6">{{ errorMessage }}</p>
        <button 
          @click="closeErrorModal" 
          class="w-full px-4 py-2.5 bg-primary hover:bg-primary-dark dark:bg-primary-dark dark:hover:bg-primary text-primary-on font-medium rounded-md3-full shadow-md3-2 hover:shadow-md3-3 transition-all duration-200"
        >
          확인
        </button>
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
import PostCard from '@/components/post/PostCard.vue';

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
    const url = tag ? `/api/v1/board/?tags=${encodeURIComponent(tag)}` : '/api/v1/board/';
    
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
/* Custom animations for smooth entrance */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}
</style>
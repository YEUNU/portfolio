<template>
  <div class="page-container contact-view">
    <!-- 관리자 로그인 시에만 수정하기 버튼을 보여줍니다. -->
    <div v-if="authStore.isAdmin" class="page-actions">
      <!-- 
        '수정하기' 버튼 클릭 시, 
        /write/contact 경로로 이동하여 WriteView 컴포넌트를 재사용합니다.
      -->
      <router-link :to="{ name: 'Edit', params: { id: 'contact' } }" class="btn btn-primary">
        수정하기
      </router-link>
    </div>
    
    <div v-if="loading" class="loading-spinner">
      Loading...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="pageContent" class="content-wrapper">
      <h1 class="page-title">{{ pageContent.title }}</h1>
      <!-- 마크다운으로 작성된 본문을 HTML로 렌더링합니다. -->
      <MarkdownPreview :content="pageContent.content" />
    </div>
    <div v-else class="info-message">
      페이지 콘텐츠가 없습니다. 관리자 계정으로 로그인하여 내용을 작성해주세요.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';

const pageContent = ref(null);
const loading = ref(true);
const error = ref(null);
const authStore = useAuthStore();

// 'contact' 페이지의 데이터를 불러오는 함수
const fetchPageContent = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 백엔드에 slug가 'contact'인 게시글(페이지)의 데이터를 요청합니다.
    const response = await api.get('/api/v1/board/slug/contact');
    pageContent.value = response.data;
  } catch (err) {
    console.error('Failed to load contact page content:', err);
    // 404 에러가 아닌 경우에만 에러 메시지를 표시합니다. (콘텐츠가 없는 것은 에러가 아님)
    if (err.response?.status !== 404) {
      error.value = '페이지를 불러오는 중 오류가 발생했습니다.';
    }
  } finally {
    loading.value = false;
  }
};

// 컴포넌트가 마운트될 때 데이터를 불러옵니다.
onMounted(fetchPageContent);
</script>

<style scoped>
/* 다른 페이지와의 일관성을 위해 .page-container 클래스를 사용합니다. */
.page-container {
  /* 스타일은 AboutView.vue나 다른 뷰 컴포넌트와 유사하게 구성할 수 있습니다. */
}
.page-actions {
  text-align: right;
  margin-bottom: 1.5rem;
}
.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333;
}
.btn {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.btn-primary {
  background-color: #3d8bfd;
  color: #fff;
}
.btn-primary:hover {
  background-color: #2a79e8;
}
.loading-spinner, .error-message, .info-message {
  text-align: center;
  margin-top: 4rem;
  color: #888;
}
</style>

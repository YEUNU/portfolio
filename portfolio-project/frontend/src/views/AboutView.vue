<template>
  <div class="page-container about-view">
    <div v-if="loading">콘텐츠를 불러오는 중입니다...</div>
    <div v-else-if="error">{{ error }}</div>
    <article v-else-if="page">
      <!-- [수정] 제목과 버튼을 감싸는 헤더 -->
      <header class="page-header">
        <h1 class="page-title">{{ page.title }}</h1>
        <!-- 관리자일 경우에만 수정/삭제 버튼을 보여줍니다 -->
        <div v-if="authStore.isAdmin" class="admin-actions">
          <router-link :to="{ name: 'Edit', params: { id: 'about' } }" class="btn btn-secondary">
            수정하기
          </router-link>
          <!-- 삭제 기능은 위험하므로, 필요 시 주석을 해제하고 deletePage 함수를 구현하세요. -->
          <!-- <button @click="deletePage" class="btn btn-danger">삭제</button> -->
        </div>
      </header>

      <hr class="divider" />

      <!-- MarkdownPreview 컴포넌트를 사용하여 콘텐츠를 표시합니다 -->
      <MarkdownPreview :content="page.content" />
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
// MarkdownPreview 컴포넌트를 사용한다고 가정합니다.
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';

const router = useRouter();
const authStore = useAuthStore();
const page = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    // slug를 기반으로 'about' 페이지 데이터를 불러옵니다.
    const response = await api.get('/api/v1/board/slug/about');
    page.value = response.data;
  } catch (err) {
    console.error('Failed to load page content:', err);
    error.value = '페이지를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});

/*
// 삭제 기능 구현 예시
const deletePage = async () => {
  if (confirm("'About' 페이지를 정말로 삭제하시겠습니까?")) {
    try {
      await api.delete('/api/v1/board/about'); // slug 'about'을 사용
      router.push('/'); // 삭제 후 홈으로 이동
    } catch (err) {
      console.error('Failed to delete page:', err);
      alert('페이지 삭제에 실패했습니다.');
    }
  }
};
*/
</script>

<style scoped>
/* --- [핵심 수정] 제목과 버튼의 레이아웃을 잡는 스타일 --- */
.page-header {
  display: flex; /* 자식 요소(제목, 버튼 그룹)를 가로로 배치 */
  justify-content: space-between; /* 양쪽 끝으로 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  margin-bottom: 1.5rem;
  flex-wrap: wrap; /* 화면이 좁아질 경우 버튼이 아래로 떨어지도록 함 */
  gap: 1rem; /* 제목과 버튼 그룹 사이의 최소 간격 */
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--color-text, #e0e0e0);
  margin: 0; /* 브라우저 기본 마진 제거 */
}

.admin-actions {
  display: flex;
  gap: 0.75rem; /* 버튼 사이의 간격 */
}
/* -------------------------------------------------------- */

/* App.vue 또는 공통 스타일시트의 버튼 스타일과 일치시키는 것이 좋습니다. */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.btn-secondary {
  background-color: #2a2a2a;
  color: #e0e0e0;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background-color: #333;
}

.btn-danger {
  background-color: #e53935;
  color: #fff;
}

.divider {
  border: none;
  height: 1px;
  background-color: #2a2a2a;
  margin-bottom: 2rem;
}
</style>


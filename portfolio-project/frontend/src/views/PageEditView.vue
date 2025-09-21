<template>
  <div class="page-edit-view">
    <h1 class="page-title">"{{ pageTitle }}" 페이지 수정</h1>
    <div class="editor-layout">
      <!-- 왼쪽: 수정 폼 -->
      <div class="editor-container">
        <form @submit.prevent="handleSubmit" class="edit-form">
          <div class="form-group">
            <label for="title">페이지 제목</label>
            <input id="title" type="text" v-model="page.title" required />
          </div>
          <div class="form-group">
            <label for="content">내용 (Markdown 지원)</label>
            <textarea id="content" v-model="page.content" rows="20" required></textarea>
          </div>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? '저장 중...' : '저장하기' }}
          </button>
          <p v-if="error" class="error-message">{{ error }}</p>
        </form>
      </div>
      <!-- 오른쪽: 실시간 미리보기 -->
      <div class="preview-container">
        <h2 class="preview-title">미리보기</h2>
        <div class="markdown-preview" v-html="compiledMarkdown"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { marked } from 'marked';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const page = ref({ title: '', content: '' });
const pageTitle = ref('');
const loading = ref(false);
const error = ref(null);

// Markdown 콘텐츠를 실시간으로 HTML로 변환
const compiledMarkdown = computed(() => {
  return marked(page.value.content || '내용을 입력하면 여기에 미리보기가 표시됩니다.');
});

// 컴포넌트가 마운트될 때 기존 페이지 데이터를 불러옴
onMounted(async () => {
  try {
    const slug = route.params.slug;
    const response = await api.get(`/api/v1/pages/${slug}`);
    page.value = response.data;
    pageTitle.value = response.data.title; // 초기 제목 설정
  } catch (err) {
    error.value = '페이지 데이터를 불러오는 데 실패했습니다.';
  }
});

// 수정된 내용을 서버에 저장하는 함수
const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  try {
    const slug = route.params.slug;
    await api.put(`/api/v1/pages/${slug}`, {
      title: page.value.title,
      content: page.value.content,
    });
    // 저장 성공 시 해당 페이지 뷰로 이동
    router.push({ name: 'PageView', params: { slug } });
  } catch (err) {
    error.value = '페이지 저장에 실패했습니다.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* WriteView.vue와 유사한 스타일을 사용하여 일관성을 유지합니다. */
.page-edit-view {
  color: #fff;
}
.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
}
.editor-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
input, textarea {
  width: 100%;
  padding: 0.8rem;
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 1rem;
  font-family: inherit;
}
textarea {
  resize: vertical;
}
.btn-submit {
  padding: 0.8rem 1.5rem;
  border: none;
  background-color: #3d8bfd;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}
.preview-container {
  border-left: 1px solid #444;
  padding-left: 2rem;
}
.preview-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.markdown-preview {
  background-color: #1e1e1e;
  padding: 1rem;
  border-radius: 8px;
  min-height: 400px;
  line-height: 1.7;
}
.error-message {
  color: #e57373;
  margin-top: 1rem;
}

/* Markdown 스타일링 */
.markdown-preview :deep(h2) {
  font-size: 1.8rem;
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
}
.markdown-preview :deep(p) {
  margin-bottom: 1rem;
}
.markdown-preview :deep(ul) {
  padding-left: 20px;
}
</style>

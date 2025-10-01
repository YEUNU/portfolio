<template>
  <div class="page-container write-view">
    <h1 class="page-title">{{ isEditing ? '게시글 수정' : '새 글 작성하기' }}</h1>
    <form @submit.prevent="handleSubmit">
      <div class="editor-layout">
        <!-- Editor Section -->
        <div class="editor-container">
          <div class="form-group">
            <label for="title">제목</label>
            <input
              type="text"
              id="title"
              v-model="post.title"
              placeholder="제목을 입력하세요"
              required
            />
          </div>

          <div class="form-group">
            <label for="content">내용</label>
            <div class="editor-toolbar">
              <button type="button" @click="triggerFileInput" class="btn-upload">이미지 업로드</button>
              <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" hidden />
            </div>
            <textarea
              id="content"
              ref="contentTextarea"
              v-model="post.content"
              rows="20"
              placeholder="내용을 입력하세요 (마크다운 지원)"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="tags">태그 (쉼표로 구분)</label>
            <input
              type="text"
              id="tags"
              v-model="post.tags"
              placeholder="예: vue, javascript, frontend"
            />
          </div>
        </div>

        <!-- Preview Section -->
        <div class="preview-container">
          <h2 class="preview-title">미리보기</h2>
          <div class="markdown-preview" v-html="compiledMarkdown"></div>
        </div>
      </div>
      
      <p v-if="error" class="error-message">{{ error }}</p>
      
      <div class="form-actions">
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '저장 중...' : (isEditing ? '수정하기' : '저장하기') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import marked from '@/utils/markdown';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();
const post = ref({
  title: '',
  content: '',
  tags: '',
});
const loading = ref(false);
const error = ref(null);
const fileInput = ref(null);
const contentTextarea = ref(null);

const isEditing = computed(() => !!route.params.id);

const compiledMarkdown = computed(() => {
  return marked(post.value.content || '내용을 입력하면 여기에 미리보기가 표시됩니다.');
});

onMounted(async () => {
  const postId = route.params.id;
  if (isEditing.value && postId) {
    loading.value = true;
    error.value = null;
    try {
      let response;
      // --- [핵심 수정] ---
      // postId가 숫자인지 (일반 게시글) 아닌지 (고정 페이지 slug) 확인합니다.
      if (isNaN(parseInt(postId))) {
        // postId가 'about', 'contact' 같은 문자열이면 slug API를 호출합니다.
        response = await api.get(`/api/v1/board/slug/${postId}`);
      } else {
        // postId가 숫자이면 기존 ID 기반 API를 호출합니다.
        response = await api.get(`/api/v1/board/${postId}`);
      }
      
      if (Array.isArray(response.data.tags)) {
        response.data.tags = response.data.tags.join(', ');
      }
      post.value = response.data;
    } catch (err) {
      console.error('Failed to load post for editing:', err);
      error.value = '게시글을 불러오는 데 실패했습니다.';
    } finally {
      loading.value = false;
    }
  }
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/api/v1/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    const relativePath = response.data.file_path;
    const markdownImage = `\n![${file.name}](${relativePath})\n`;

    const textarea = contentTextarea.value;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    post.value.content = post.value.content.substring(0, start) + markdownImage + post.value.content.substring(end);
    
    await nextTick();
    textarea.selectionStart = textarea.selectionEnd = start + markdownImage.length;
    textarea.focus();

  } catch (err) {
    alert('이미지 업로드에 실패했습니다.');
    console.error(err);
  } finally {
    event.target.value = '';
  }
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  try {
    const contentToSave = post.value.content.replace(new RegExp(api.defaults.baseURL, 'g'), '');
    const payload = { ...post.value, content: contentToSave };

    if (isEditing.value) {
      await api.put(`/api/v1/board/${route.params.id}`, payload);
    } else {
      await api.post('/api/v1/board/', payload);
    }
    router.push({ name: 'Board' });
  } catch (err) {
    error.value = '게시글 저장에 실패했습니다.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.page-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: var(--spacing-lg);
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
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  color: var(--color-text);
  font-size: 1rem;
}
textarea { 
  resize: vertical; 
  font-family: inherit;
}
.form-actions {
  margin-top: 2rem;
  text-align: right;
}
.btn-submit {
  padding: 0.8rem 1.5rem;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}
.btn-submit:hover {
  background-color: var(--color-primary-hover);
}
.btn-submit:disabled {
  background-color: var(--color-surface-secondary);
  cursor: not-allowed;
}
.preview-container {
  border-left: 1px solid var(--color-border);
  padding-left: 2rem;
}
.preview-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.markdown-preview {
  background-color: var(--color-surface);
  padding: 1rem;
  border-radius: var(--border-radius);
  min-height: 400px;
}
.error-message {
  color: var(--color-error);
  margin-top: 1rem;
}
.editor-toolbar {
  margin-bottom: 10px;
}
.btn-upload {
  padding: 6px 12px;
  background-color: var(--color-surface-secondary);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-upload:hover {
  background-color: var(--color-surface);
}

@media (max-width: 1024px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }
  .preview-container {
    border-left: none;
    border-top: 1px solid var(--color-border);
    padding-left: 0;
    padding-top: 2rem;
    margin-top: 2rem;
  }
}
</style>

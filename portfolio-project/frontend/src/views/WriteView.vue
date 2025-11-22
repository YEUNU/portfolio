<template>
  <div class="max-w-7xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl md:text-5xl font-bold text-primary dark:text-primary-dark mb-2 animate-fade-in">
        {{ isEditing ? '게시글 수정' : '새 글 작성하기' }}
      </h1>
      <div class="h-1 w-20 bg-primary dark:bg-primary-dark rounded-md3-full"></div>
    </div>
    
    <form @submit.prevent="handleSubmit">
      <!-- Title (Full Width) -->
      <div class="form-group mb-6">
        <label for="title" class="block text-sm font-medium text-surface-on dark:text-surface-dark-on mb-2">
          제목
        </label>
        <input
          type="text"
          id="title"
          v-model="post.title"
          placeholder="제목을 입력하세요"
          class="w-full px-4 py-3 bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-md3-md text-surface-on dark:text-surface-dark-on placeholder-surface-on-variant dark:placeholder-surface-dark-on focus:outline-none focus:border-primary dark:focus:border-primary-dark focus:ring-2 focus:ring-primary/20 dark:focus:ring-primary-dark/20 transition-all"
          required
        />
      </div>

      <div class="editor-layout">
        <!-- Editor Section (full width) -->
        <div class="editor-container">
          <div class="form-group">
            <label for="content" class="block text-sm font-medium text-surface-on dark:text-surface-dark-on mb-2">
              내용
            </label>
            <TiptapEditor 
              ref="tiptapEditor"
              v-model="post.content" 
              @upload-image="triggerFileInput"
            />
            <input
              type="file"
              ref="fileInput"
              @change="handleFileUpload"
              accept="image/*"
              hidden
            />
          </div>
        </div>
      </div>

      <!-- Tags (Full Width) -->
      <div class="form-group mt-6">
        <label for="tags" class="block text-sm font-medium text-surface-on dark:text-surface-dark-on mb-2">
          태그 (쉼표로 구분)
        </label>
        <input
          type="text"
          id="tags"
          v-model="post.tags"
          placeholder="예: vue, javascript, frontend"
          class="w-full px-4 py-3 bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-md3-md text-surface-on dark:text-surface-dark-on placeholder-surface-on-variant dark:placeholder-surface-dark-on focus:outline-none focus:border-primary dark:focus:border-primary-dark focus:ring-2 focus:ring-primary/20 dark:focus:ring-primary-dark/20 transition-all"
        />
      </div>

      <p v-if="error" class="text-error dark:text-error-dark mt-4 text-center">{{ error }}</p>

      <div class="flex justify-end gap-3 mt-8">
        <button 
          type="button" 
          @click="$router.back()"
          class="px-6 py-3 bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on rounded-md3-md hover:bg-outline/20 dark:hover:bg-outline-dark/20 transition-all duration-200"
        >
          취소
        </button>
        <button 
          type="submit" 
          class="px-6 py-3 bg-primary dark:bg-primary-dark text-white rounded-md3-md hover:shadow-md3-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200" 
          :disabled="loading"
        >
          {{ loading ? '저장 중...' : isEditing ? '수정하기' : '저장하기' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';
import TiptapEditor from '@/components/editor/TiptapEditor.vue';

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
const tiptapEditor = ref(null);

const isEditing = computed(() => !!route.params.id);

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
    
    // TipTap 에디터에 이미지 삽입
    if (tiptapEditor.value) {
      tiptapEditor.value.insertImage(relativePath);
    }
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
    console.error('저장 실패:', err);
    error.value = '저장에 실패했습니다.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.editor-layout {
  display: block;
  gap: 0;
  align-items: start;
  min-height: 400px;
}

.editor-container {
  min-width: 0;
}

/* preview removed: preview-container styles intentionally removed */

.form-group {
  @apply mb-6;
}

/* Enhanced Toolbar Styles */
.editor-toolbar-enhanced {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem;
  flex-wrap: wrap;
}

.toolbar-group {
  display: flex;
  gap: 0.25rem;
}

.toolbar-divider {
  width: 1px;
  @apply bg-outline/30 dark:bg-outline-dark/30;
  margin: 0 0.5rem;
}

.toolbar-btn {
  @apply px-3 py-2 rounded-md3-sm transition-all duration-200 flex items-center justify-center min-w-[2rem] border border-transparent;
  @apply text-surface-on dark:text-surface-dark-on;
  @apply hover:bg-primary/10 dark:hover:bg-primary-dark/10;
  @apply hover:text-primary dark:hover:text-primary-dark;
}

.toolbar-btn:hover {
  @apply border-primary/30 dark:border-primary-dark/30;
}

.toolbar-btn:active {
  @apply bg-primary dark:bg-primary-dark text-white scale-95;
}

/* Rendered Content Preview Styles */
.rendered-content {
  line-height: 1.7;
  word-wrap: break-word;
  overflow-wrap: break-word;
  @apply text-surface-on dark:text-surface-dark-on;
}

/* Headings */
.rendered-content :deep(h1) {
  @apply text-4xl font-bold mb-4 text-primary dark:text-primary-dark;
  border-bottom: 2px solid;
  @apply border-primary/30 dark:border-primary-dark/30;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
}

.rendered-content :deep(h2) {
  @apply text-3xl font-bold mb-3 text-primary dark:text-primary-dark;
  border-bottom: 2px solid;
  @apply border-primary/30 dark:border-primary-dark/30;
  padding-bottom: 0.5rem;
  margin-top: 1.75rem;
}

.rendered-content :deep(h3) {
  @apply text-2xl font-bold mb-2 text-primary dark:text-primary-dark;
  margin-top: 1.5rem;
}

.rendered-content :deep(h4) {
  @apply text-xl font-bold mb-2 text-surface-on dark:text-surface-dark-on;
  margin-top: 1.25rem;
}

.rendered-content :deep(h5) {
  @apply text-lg font-bold mb-2 text-surface-on dark:text-surface-dark-on;
  margin-top: 1rem;
}

.rendered-content :deep(h6) {
  @apply text-base font-bold mb-2 text-surface-on dark:text-surface-dark-on;
  margin-top: 1rem;
}

/* Paragraphs */
.rendered-content :deep(p) {
  margin-bottom: 1rem;
  @apply text-surface-on dark:text-surface-dark-on;
  line-height: 1.8;
}

/* Links */
.rendered-content :deep(a) {
  @apply text-primary dark:text-primary-dark underline hover:text-primary-600 dark:hover:text-primary-300;
  transition: color 0.2s ease;
}

/* Inline Code */
.rendered-content :deep(code) {
  @apply bg-surface-variant dark:bg-surface-dark-variant text-error dark:text-error-dark;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

/* Code Blocks */
.rendered-content :deep(pre) {
  @apply bg-surface-variant dark:bg-surface-dark-variant;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid;
  @apply border-outline/20 dark:border-outline-dark/20;
}

.rendered-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
  @apply text-surface-on dark:text-surface-dark-on;
  font-size: 0.9em;
  line-height: 1.6;
}

/* Blockquotes */
.rendered-content :deep(blockquote) {
  @apply border-l-4 border-primary dark:border-primary-dark;
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  @apply text-surface-on-variant dark:text-surface-dark-on;
  font-style: italic;
  background: rgba(0, 0, 0, 0.02);
  @apply dark:bg-white/5;
  padding: 1rem 1rem 1rem 1.5rem;
  border-radius: 0 8px 8px 0;
}

.rendered-content :deep(blockquote p) {
  margin-bottom: 0.5rem;
}

.rendered-content :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

/* Lists */
.rendered-content :deep(ul),
.rendered-content :deep(ol) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.rendered-content :deep(ul) {
  list-style-type: disc;
}

.rendered-content :deep(ol) {
  list-style-type: decimal;
}

.rendered-content :deep(li) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 0.5rem;
  line-height: 1.7;
}

.rendered-content :deep(li > ul),
.rendered-content :deep(li > ol) {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

/* Task Lists */
.rendered-content :deep(ul[data-type="taskList"]) {
  list-style: none;
  padding-left: 0;
}

.rendered-content :deep(ul[data-type="taskList"] li) {
  display: flex;
  align-items: start;
  gap: 0.5rem;
}

.rendered-content :deep(ul[data-type="taskList"] li input[type="checkbox"]) {
  margin-top: 0.25rem;
  cursor: pointer;
}

.rendered-content :deep(ul[data-type="taskList"] li label) {
  cursor: pointer;
}

/* Tables */
.rendered-content :deep(table) {
  @apply text-surface-on dark:text-surface-dark-on border border-outline dark:border-outline-dark;
  width: 100%;
  margin: 1.5rem 0;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
}

.rendered-content :deep(th),
.rendered-content :deep(td) {
  @apply border border-outline/30 dark:border-outline-dark/30;
  padding: 0.75rem;
  text-align: left;
}

.rendered-content :deep(th) {
  @apply bg-surface-variant dark:bg-surface-dark-variant font-bold;
}

.rendered-content :deep(tr:nth-child(even)) {
  @apply bg-surface-variant/50 dark:bg-surface-dark-variant/50;
}

/* Text Formatting */
.rendered-content :deep(strong) {
  @apply text-surface-on dark:text-surface-dark-on font-bold;
}

.rendered-content :deep(em) {
  @apply text-surface-on dark:text-surface-dark-on italic;
}

.rendered-content :deep(u) {
  text-decoration: underline;
}

.rendered-content :deep(s) {
  text-decoration: line-through;
  opacity: 0.7;
}

/* Images */
.rendered-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  @apply dark:shadow-none;
}

/* Horizontal Rules */
.rendered-content :deep(hr) {
  @apply border-outline/30 dark:border-outline-dark/30;
  margin: 2rem 0;
  border: none;
  border-top: 2px solid;
}

/* Text Alignment */
.rendered-content :deep([style*="text-align: left"]) {
  text-align: left;
}

.rendered-content :deep([style*="text-align: center"]) {
  text-align: center;
}

.rendered-content :deep([style*="text-align: right"]) {
  text-align: right;
}

@media (max-width: 1024px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }
  .preview-container {
    position: static;
    border-top: 1px solid;
    @apply border-outline/30 dark:border-outline-dark/30 pt-8 mt-8;
  }
}
</style>

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
        <!-- Editor Section -->
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

        <!-- Preview Section -->
        <div class="preview-container">
          <div class="sticky top-24">
            <h3 class="text-lg font-semibold text-surface-on dark:text-surface-dark-on mb-3">미리보기</h3>
            <div class="preview-content bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-md3-md p-6 min-h-[400px] overflow-auto">
              <h2 class="text-2xl font-bold text-surface-on dark:text-surface-dark-on mb-4">{{ post.title || '제목을 입력하세요' }}</h2>
              <div v-if="post.content" v-html="post.content" class="markdown-preview"></div>
              <p v-else class="text-surface-on-variant dark:text-surface-dark-on">내용을 입력하면 여기에 미리보기가 표시됩니다.</p>
            </div>
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
  min-height: 600px;
}

.editor-container {
  min-width: 0;
}

.preview-container {
  min-width: 0;
  position: sticky;
  top: 6rem;
}

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

/* Markdown Preview Styles */
.markdown-preview {
  line-height: 1.7;
  word-wrap: break-word;
  overflow-wrap: break-word;
  @apply text-surface-on dark:text-surface-dark-on;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3),
.markdown-preview :deep(h4),
.markdown-preview :deep(h5),
.markdown-preview :deep(h6) {
  @apply text-surface-on dark:text-surface-dark-on font-bold;
  border-bottom: 1px solid;
  @apply border-outline/30 dark:border-outline-dark/30;
  padding-bottom: 0.5rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.markdown-preview :deep(h1) { @apply text-3xl; }
.markdown-preview :deep(h2) { @apply text-2xl; }
.markdown-preview :deep(h3) { @apply text-xl; }

.markdown-preview :deep(p) {
  margin-bottom: 1rem;
  @apply text-surface-on dark:text-surface-dark-on;
}

.markdown-preview :deep(a) {
  @apply text-primary dark:text-primary-dark underline hover:text-primary-600 dark:hover:text-primary-300;
}

.markdown-preview :deep(code) {
  @apply bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-preview :deep(pre) {
  @apply bg-surface-variant dark:bg-surface-dark-variant;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-preview :deep(pre) code {
  background-color: transparent;
  padding: 0;
  @apply text-surface-on dark:text-surface-dark-on;
}

.markdown-preview :deep(blockquote) {
  @apply border-l-4 border-primary dark:border-primary-dark;
  padding-left: 1rem;
  margin-left: 0;
  margin-bottom: 1rem;
  @apply text-surface-on-variant dark:text-surface-dark-on;
}

.markdown-preview :deep(ul),
.markdown-preview :deep(ol) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.markdown-preview :deep(li) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 0.5rem;
}

.markdown-preview :deep(table) {
  @apply text-surface-on dark:text-surface-dark-on border border-outline dark:border-outline-dark;
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
}

.markdown-preview :deep(th),
.markdown-preview :deep(td) {
  @apply border border-outline dark:border-outline-dark;
  padding: 0.5rem;
}

.markdown-preview :deep(th) {
  @apply bg-surface-variant dark:bg-surface-dark-variant font-bold;
}

.markdown-preview :deep(strong) {
  @apply text-surface-on dark:text-surface-dark-on font-bold;
}

.markdown-preview :deep(em) {
  @apply text-surface-on dark:text-surface-dark-on italic;
}

.markdown-preview :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1rem 0;
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

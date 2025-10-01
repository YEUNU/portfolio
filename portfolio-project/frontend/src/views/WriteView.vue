&lt;template>
  &lt;div class="write-view">
    &lt;h1 class="page-title">{{ isEditing ? '게시글 수정' : '새 글 작성하기' }}&lt;/h1>
    &lt;ContentEditor
      :initial-data="post"
      :api-endpoint="apiEndpoint"
      :method="isEditing ? 'PUT' : 'POST'"
      @saved="handleSaved"
    />
  &lt;/div>
&lt;/template>

&lt;script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ContentEditor from '@/components/editor/ContentEditor.vue';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();

const post = ref({
  title: '',
  content: '',
  tags: '',
});

const isEditing = computed(() => !!route.params.id);

const apiEndpoint = computed(() => {
  return isEditing.value 
    ? `/api/v1/board/${route.params.id}`
    : '/api/v1/board/';
});

const handleSaved = () => {
  router.push({ name: 'Board' });
};

onMounted(async () => {
  if (isEditing.value) {
    try {
      const response = await api.get(`/api/v1/board/${route.params.id}`);
      post.value = response.data;
    } catch (err) {
      console.error('Failed to load post:', err);
    }
  }
});
&lt;/script>

&lt;style scoped>
.write-view {
  color: var(--color-text);
  max-width: 1600px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}
&lt;/style>

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
  if (isEditing.value) {
    try {
      const postId = route.params.id;
      const response = await api.get(`/api/v1/board/${postId}`);
      post.value = response.data;
    } catch (err) {
      error.value = '게시글을 불러오는 데 실패했습니다.';
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
      headers: {
        'Content-Type': 'multipart/form-data',
      },
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
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.write-view {
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
}
textarea { resize: vertical; }
.btn-submit {
  padding: 0.8rem 1.5rem;
  border: none;
  background-color: #3d8bfd;
  color: white;
  border-radius: 8px;
  cursor: pointer;
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
}
.error-message {
  color: #e57373;
  margin-top: 1rem;
}
.editor-toolbar {
  margin-bottom: 10px;
}
.btn-upload {
  padding: 6px 12px;
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 6px;
  cursor: pointer;
}

/* 모바일 화면에서 1열 레이아웃으로 변경 */
@media (max-width: 1024px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }
  .preview-container {
    border-left: none;
    border-top: 1px solid #444;
    padding-left: 0;
    padding-top: 2rem;
    margin-top: 2rem;
  }
}
</style>


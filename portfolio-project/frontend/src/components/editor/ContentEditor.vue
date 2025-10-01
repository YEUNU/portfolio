&lt;template>
  &lt;div class="content-editor">
    &lt;div class="editor-layout">
      &lt;div class="editor-container">
        &lt;form @submit.prevent="handleSubmit" class="write-form">
          &lt;BaseFormField
            v-model="formData.title"
            label="제목"
            required
          />
          
          &lt;BaseFormField
            v-if="showTags"
            v-model="formData.tags"
            label="해시태그 (쉼표로 구분)"
            placeholder="e.g., vue, fastapi, portfolio"
          />
          
          &lt;div class="form-group">
            &lt;label>내용 (Markdown 지원)&lt;/label>
            &lt;div class="editor-toolbar">
              &lt;BaseButton
                type="button"
                @click="triggerFileInput"
                variant="secondary"
              >
                이미지 업로드
              &lt;/BaseButton>
              &lt;input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                accept="image/*"
                hidden
              />
            &lt;/div>
            &lt;BaseFormField
              v-model="formData.content"
              type="textarea"
              :rows="15"
              required
            />
          &lt;/div>
          
          &lt;BaseButton
            type="submit"
            :disabled="loading"
          >
            {{ loading ? '저장 중...' : '저장하기' }}
          &lt;/BaseButton>
          
          &lt;p v-if="error" class="error-message">{{ error }}&lt;/p>
        &lt;/form>
      &lt;/div>
      
      &lt;div class="preview-container">
        &lt;h2 class="preview-title">미리보기&lt;/h2>
        &lt;MarkdownPreview :content="formData.content" />
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import BaseButton from '@/components/common/BaseButton.vue';
import BaseFormField from '@/components/common/BaseFormField.vue';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      tags: ''
    })
  },
  showTags: {
    type: Boolean,
    default: true
  },
  apiEndpoint: {
    type: String,
    required: true
  },
  method: {
    type: String,
    default: 'POST'
  }
});

const emit = defineEmits(['saved']);

const formData = ref({ ...props.initialData });
const loading = ref(false);
const error = ref(null);
const fileInput = ref(null);

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
    
    const textarea = document.querySelector('textarea');
    const start = textarea.selectionStart;
    
    formData.value.content = 
      formData.value.content.substring(0, start) + 
      markdownImage + 
      formData.value.content.substring(textarea.selectionEnd);
    
    textarea.focus();
    textarea.selectionStart = textarea.selectionEnd = start + markdownImage.length;

  } catch (err) {
    error.value = '이미지 업로드에 실패했습니다.';
  } finally {
    event.target.value = '';
  }
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const contentToSave = formData.value.content.replace(
      new RegExp(api.defaults.baseURL, 'g'),
      ''
    );
    
    const payload = { 
      ...formData.value,
      content: contentToSave
    };
    
    await api({
      method: props.method,
      url: props.apiEndpoint,
      data: payload
    });
    
    emit('saved');
    
  } catch (err) {
    error.value = '저장에 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  formData.value = { ...props.initialData };
});
&lt;/script>

&lt;style scoped>
.content-editor {
  color: var(--color-text);
}

.editor-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.preview-container {
  border-left: 1px solid var(--color-border);
  padding-left: var(--spacing-lg);
}

.preview-title {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
}

.editor-toolbar {
  margin-bottom: var(--spacing-sm);
}

@media (max-width: 1024px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }
  
  .preview-container {
    border-left: none;
    border-top: 1px solid var(--color-border);
    padding-left: 0;
    padding-top: var(--spacing-lg);
    margin-top: var(--spacing-lg);
  }
}
&lt;/style>
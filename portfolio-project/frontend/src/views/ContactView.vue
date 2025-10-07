<template>
  <div class="page-container contact-view">
    <div v-if="loading">콘텐츠를 불러오는 중입니다...</div>
    <div v-else-if="error">{{ error }}</div>
    <article v-else-if="page">
      <header class="page-header">
        <h1 class="page-title">{{ page.title }}</h1>
        <div v-if="authStore.isAdmin" class="admin-actions">
          <router-link :to="{ name: 'Edit', params: { id: 'contact' } }" class="btn btn-secondary">
            수정하기
          </router-link>
        </div>
      </header>
      <hr class="divider" />
      <MarkdownPreview :content="page.content" />
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';
import { useMeta } from '@/composables/useMeta';

const router = useRouter();
const authStore = useAuthStore();
const page = ref(null);
const loading = ref(true);
const error = ref(null);
const { updateMeta, addStructuredData } = useMeta();

onMounted(async () => {
  try {
    // [핵심 수정] 올바른 slug 기반 API 엔드포인트를 호출합니다.
    const response = await api.get('/api/v1/board/slug/contact');
    page.value = response.data;
    
    // SEO 메타 데이터 설정
    updateMeta({
      title: `${page.value.title} - 성연우의 포트폴리오`,
      description: '성연우에게 연락하세요. 이메일, GitHub 등 다양한 연락 방법을 확인할 수 있습니다.',
      keywords: '성연우, Contact, 연락처, 이메일, GitHub, 문의',
      canonical: 'https://your-domain.com/contact'
    });

    // Contact 페이지 구조화된 데이터
    addStructuredData({
      "@context": "https://schema.org",
      "@type": "ContactPage",
      "name": page.value.title,
      "description": "성연우의 연락처 정보",
      "author": {
        "@type": "Person",
        "name": "성연우"
      },
      "url": "https://your-domain.com/contact"
    });
    
  } catch (err) {
    console.error('Failed to load page content:', err);
    error.value = '페이지를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* AboutView.vue와 동일한 스타일을 사용합니다. */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--color-text, #e0e0e0);
  margin: 0;
}
.admin-actions {
  display: flex;
  gap: 0.75rem;
}
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
.divider {
  border: none;
  height: 1px;
  background-color: #2a2a2a;
  margin-bottom: 2rem;
}
</style>


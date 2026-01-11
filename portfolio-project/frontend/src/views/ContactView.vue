<template>
  <PageContainer 
    :title="page?.title || 'Contact'" 
    :loading="loading" 
    :error="error"
    edit-id="contact"
    :show-edit-button="authStore.isAdmin"
  >
    <div v-if="page" class="prose prose-invert max-w-none">
      <MarkdownPreview :content="page.content" />
    </div>
  </PageContainer>
</template>

<script setup>
import { useAuthStore } from '@/store/auth';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';
import PageContainer from '@/components/common/PageContainer.vue';
import { usePageData } from '@/composables/usePageData';
import { useMeta } from '@/composables/useMeta';
import { watch } from 'vue';

const { updateMeta } = useMeta();

const authStore = useAuthStore();

const { page, loading, error } = usePageData('contact', {
  title: undefined, // 페이지 제목을 API에서 가져와 자동으로 설정
  description: '성연우에게 연락하세요. 이메일, GitHub 등 다양한 연락 방법을 확인할 수 있습니다.',
  keywords: '성연우, Contact, 연락처, 이메일, GitHub, 문의',
  canonical: 'https://your-domain.com/contact',
  structuredData: {
    '@type': 'ContactPage',
    description: '성연우의 연락처 정보',
    author: {
      '@type': 'Person',
      name: '성연우',
    },
  },
});

watch(() => page.value, (val) => {
  if (!val) return;
  const origin = window.location?.origin || '';
  const fallbackDescription = val?.content
    ? val.content.replace(/<[^>]+>/g, '').slice(0, 160)
    : '성연우에게 연락하는 방법을 확인하세요.';
  updateMeta({
    title: val.title || 'Contact - 성연우 포트폴리오',
    description: fallbackDescription,
    canonical: `${origin}/contact`,
    ogImage: '/og-image.jpg',
  });
}, { immediate: true });
</script>

<template>
  <PageContainer 
    :title="page?.title || 'About'" 
    :loading="loading" 
    :error="error"
    edit-id="about"
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

const { page, loading, error } = usePageData('about', {
  title: undefined, // 페이지 제목을 API에서 가져와 자동으로 설정
  description: '성연우에 대해 알아보세요. 개발자로서의 경험과 기술 스택을 소개합니다.',
  keywords: '성연우, About, 소개, 개발자, 경력, 기술스택',
  canonical: 'https://your-domain.com/about',
  structuredData: {
    '@type': 'AboutPage',
    description: '성연우에 대한 소개 페이지',
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
    : '성연우에 대해 알아보세요.';
  updateMeta({
    title: val.title || 'About - 성연우 포트폴리오',
    description: fallbackDescription,
    canonical: `${origin}/about`,
    ogImage: '/og-image.jpg',
  });
}, { immediate: true });
</script>



<template>
  <div class="max-w-7xl mx-auto">
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-surface-variant dark:border-surface-dark-variant border-t-primary rounded-full animate-spin"></div>
      </div>
    </div>
    
    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[400px] space-y-4">
      <svg class="w-20 h-20 text-error dark:text-error-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xl text-surface-on dark:text-surface-dark-on">{{ error }}</p>
    </div>

    <!-- Page Content -->
    <article v-else-if="page">
      <header class="flex justify-between items-start mb-8 flex-wrap gap-4">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold text-primary dark:text-primary-dark mb-2 animate-fade-in">
            {{ page.title }}
          </h1>
          <div class="h-1 w-20 bg-primary dark:bg-primary-dark rounded-md3-full"></div>
        </div>
        <router-link 
          v-if="authStore.isAdmin" 
          :to="{ name: 'Edit', params: { id: 'about' } }" 
          class="px-4 py-2 bg-primary-100 dark:bg-primary-800 text-primary-900 dark:text-primary-100 rounded-md3-md hover:shadow-md3-2 transition-all duration-200"
        >
          수정하기
        </router-link>
      </header>
      <div class="prose prose-invert max-w-none">
        <MarkdownPreview :content="page.content" />
      </div>
    </article>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth';
import MarkdownPreview from '@/components/common/MarkdownPreview.vue';
import { usePageData } from '@/composables/usePageData';

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
</script>



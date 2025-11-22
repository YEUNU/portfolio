<template>
  <div class="relative">
    <!-- Search Button/Input -->
    <div class="relative">
      <button
        v-if="!isExpanded"
        @click="expandSearch"
        class="p-2 sm:p-2.5 rounded-md3-full text-surface-on-variant dark:text-surface-dark-on hover:text-surface-on dark:hover:text-surface-dark-on hover:bg-surface-variant dark:hover:bg-surface-dark-variant transition-all shadow-md3-1 flex-shrink-0"
        aria-label="검색"
      >
        <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
      
      <div v-else class="absolute right-0 top-0 z-50 flex items-center gap-2 bg-surface/95 dark:bg-surface-dark/95 backdrop-blur-md p-2 rounded-md3-full shadow-md3-4 border border-outline/20 dark:border-outline-dark/20">
        <div class="relative">
          <input
            ref="searchInput"
            v-model="query"
            type="text"
            placeholder="전체 검색..."
            class="w-56 sm:w-64 px-4 py-2 pl-10 bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-md3-full text-surface-on dark:text-surface-dark-on placeholder-surface-on-variant dark:placeholder-surface-dark-on focus:outline-none focus:border-primary dark:focus:border-primary-dark focus:ring-2 focus:ring-primary/20 dark:focus:ring-primary-dark/20 transition-all text-sm"
            @input="handleSearch"
            @blur="handleBlur"
            @keydown.esc="collapseSearch"
          />
          <svg 
            class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-surface-on-variant dark:text-surface-dark-on"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <button
            v-if="query"
            @click="clearSearch"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-surface-on-variant dark:text-surface-dark-on hover:text-surface-on dark:hover:text-surface-dark-on transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <button
          @click="collapseSearch"
          class="p-2 rounded-md3-full text-surface-on-variant dark:text-surface-dark-on hover:text-surface-on dark:hover:text-surface-dark-on hover:bg-surface-variant dark:hover:bg-surface-dark-variant transition-all flex-shrink-0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Search Results Dropdown -->
    <div
      v-if="isExpanded && (results.length > 0 || isSearching)"
      class="absolute right-0 top-full mt-2 w-[calc(100vw-2rem)] sm:w-96 max-h-96 overflow-y-auto bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-md3-lg shadow-md3-5 z-50"
    >
      <!-- Loading -->
      <div v-if="isSearching" class="p-4 text-center text-surface-on-variant dark:text-surface-dark-on">
        검색 중...
      </div>

      <!-- Results -->
      <div v-else-if="results.length > 0">
        <div
          v-for="result in results"
          :key="result.id"
          @click="goToResult(result)"
          class="p-4 hover:bg-surface-variant dark:hover:bg-surface-dark-variant cursor-pointer border-b border-outline/10 dark:border-outline-dark/10 last:border-b-0 transition-colors"
        >
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 mt-1">
              <svg v-if="result.type === 'post'" class="w-5 h-5 text-primary dark:text-primary-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <svg v-else class="w-5 h-5 text-primary dark:text-primary-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-surface-on dark:text-surface-dark-on truncate">
                {{ result.title }}
              </div>
              <div class="text-xs text-surface-on-variant dark:text-surface-dark-on mt-1 line-clamp-2" v-html="result.snippet"></div>
              <div class="flex items-center gap-2 mt-2">
                <span class="text-xs px-2 py-0.5 bg-primary/10 dark:bg-primary-dark/10 text-primary dark:text-primary-dark rounded-md3-sm">
                  {{ result.type === 'post' ? '게시물' : result.type === 'about' ? 'About' : 'Contact' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="query && !isSearching" class="p-4 text-center text-surface-on-variant dark:text-surface-dark-on">
        검색 결과가 없습니다
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const isExpanded = ref(false);
const query = ref('');
const results = ref([]);
const isSearching = ref(false);
const searchInput = ref(null);
let searchTimeout = null;

const expandSearch = async () => {
  isExpanded.value = true;
  await nextTick();
  searchInput.value?.focus();
};

const collapseSearch = () => {
  isExpanded.value = false;
  query.value = '';
  results.value = [];
};

const handleBlur = () => {
  // 결과 클릭을 위해 약간의 딜레이
  setTimeout(() => {
    if (!query.value) {
      collapseSearch();
    }
  }, 200);
};

const clearSearch = () => {
  query.value = '';
  results.value = [];
  searchInput.value?.focus();
};

const handleSearch = async () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  if (!query.value.trim()) {
    results.value = [];
    return;
  }

  searchTimeout = setTimeout(async () => {
    isSearching.value = true;
    try {
      // 게시물 검색
      const postsResponse = await api.get(`/api/v1/board/?search=${encodeURIComponent(query.value)}`);
      const posts = postsResponse.data.map(post => ({
        id: post.id,
        type: 'post',
        title: post.title,
        snippet: stripHtml(post.content).substring(0, 100) + '...',
        url: `/board/${post.id}`
      }));

      // About 페이지 검색
      let aboutResults = [];
      try {
        const aboutResponse = await api.get('/api/v1/board/slug/about');
        if (aboutResponse.data && (
          aboutResponse.data.title.toLowerCase().includes(query.value.toLowerCase()) ||
          aboutResponse.data.content.toLowerCase().includes(query.value.toLowerCase())
        )) {
          const content = stripHtml(aboutResponse.data.content);
          const index = content.toLowerCase().indexOf(query.value.toLowerCase());
          const snippet = index >= 0 
            ? '...' + content.substring(Math.max(0, index - 40), index + 60) + '...'
            : content.substring(0, 100) + '...';
          
          aboutResults.push({
            id: 'about',
            type: 'about',
            title: aboutResponse.data.title,
            snippet: snippet,
            url: '/about'
          });
        }
      } catch (err) {
        // About 페이지가 없으면 무시
      }

      // Contact 페이지 검색
      let contactResults = [];
      try {
        const contactResponse = await api.get('/api/v1/board/slug/contact');
        if (contactResponse.data && (
          contactResponse.data.title.toLowerCase().includes(query.value.toLowerCase()) ||
          contactResponse.data.content.toLowerCase().includes(query.value.toLowerCase())
        )) {
          const content = stripHtml(contactResponse.data.content);
          const index = content.toLowerCase().indexOf(query.value.toLowerCase());
          const snippet = index >= 0 
            ? '...' + content.substring(Math.max(0, index - 40), index + 60) + '...'
            : content.substring(0, 100) + '...';
          
          contactResults.push({
            id: 'contact',
            type: 'contact',
            title: contactResponse.data.title,
            snippet: snippet,
            url: '/contact'
          });
        }
      } catch (err) {
        // Contact 페이지가 없으면 무시
      }

      // 결과 합치기 (고정 페이지 우선)
      results.value = [...aboutResults, ...contactResults, ...posts].slice(0, 10);
    } catch (err) {
      console.error('Search error:', err);
      results.value = [];
    } finally {
      isSearching.value = false;
    }
  }, 300);
};

const stripHtml = (html) => {
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
};

const goToResult = (result) => {
  router.push(result.url);
  collapseSearch();
};
</script>

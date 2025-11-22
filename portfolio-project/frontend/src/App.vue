<template>
  <div class="flex min-h-screen bg-surface dark:bg-surface-dark transition-colors duration-300">
    <PreloadLinks />

    <!-- Navigation Rail (Desktop Only) -->
    <NavigationRail />

    <!-- Main Container -->
    <div class="flex flex-col flex-1 lg:ml-20">
      <!-- Header -->
      <header class="sticky top-0 z-30 bg-surface/95 dark:bg-surface-dark/95 backdrop-blur-md border-b border-outline/20 dark:border-outline-dark/20 shadow-md3-2 transition-colors duration-300">
        <div class="flex items-center justify-between gap-2 px-3 md:px-6 py-3 md:py-4">
          <router-link 
            to="/" 
            class="text-base md:text-xl font-bold text-primary dark:text-primary-dark transition-all duration-300 truncate flex-shrink min-w-0"
          >
            <span class="hidden sm:inline">성연우의 포트폴리오</span>
            <span class="sm:hidden">포트폴리오</span>
          </router-link>
        
        <div class="flex items-center gap-2 sm:gap-3 md:gap-4 flex-shrink-0">
          <!-- Global Search -->
          <GlobalSearch />

          <!-- Dark Mode Toggle -->
          <button 
            @click="themeStore.toggleTheme()" 
            class="p-2 sm:p-2.5 rounded-md3-full text-surface-on-variant dark:text-surface-dark-on hover:text-surface-on dark:hover:text-surface-dark-on hover:bg-surface-variant dark:hover:bg-surface-dark-variant transition-all shadow-md3-1 flex-shrink-0"
            :aria-label="themeStore.isDark ? '라이트 모드로 전환' : '다크 모드로 전환'"
          >
            <svg v-if="themeStore.isDark" class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <div v-if="authStore.isLoggedIn && authStore.isAdmin" class="flex items-center gap-2">
            <!-- PDF Download Button -->
            <button 
              @click="handlePDFDownload"
              :disabled="downloadingPDF"
              class="inline-flex items-center justify-center gap-2 px-3 sm:px-5 py-2 sm:py-2.5 bg-secondary dark:bg-secondary-dark hover:bg-secondary-600 dark:hover:bg-secondary-400 text-white text-sm font-medium rounded-md3-full shadow-md3-2 hover:shadow-md3-3 transition-all duration-200 flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
              title="포트폴리오 PDF 다운로드"
            >
              <svg v-if="!downloadingPDF" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="hidden sm:inline whitespace-nowrap">{{ downloadingPDF ? 'PDF 생성중...' : 'PDF' }}</span>
            </button>
            
            <!-- Write Button - Hidden on mobile (use FAB instead) -->
            <router-link 
              to="/write" 
              class="hidden sm:inline-flex items-center justify-center gap-2 px-5 md:px-6 py-2.5 bg-primary hover:bg-primary-dark dark:bg-primary-dark dark:hover:bg-primary text-primary-on text-sm font-medium rounded-md3-full shadow-md3-2 hover:shadow-md3-3 transition-all duration-200 flex-shrink-0"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <span class="whitespace-nowrap">글쓰기</span>
            </router-link>
            
            <!-- Logout Button - Icon only on mobile -->
            <button 
              @click="handleLogout" 
              class="inline-flex items-center justify-center px-3 sm:px-5 py-2 sm:py-2.5 bg-surface-variant dark:bg-surface-dark-variant hover:bg-outline/20 dark:hover:bg-outline-dark/20 text-surface-on dark:text-surface-dark-on text-sm font-medium rounded-md3-full transition-all duration-200 flex-shrink-0"
            >
              <span class="hidden sm:inline whitespace-nowrap">로그아웃</span>
              <svg class="w-5 h-5 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
          <div v-else>
            <router-link 
              to="/login" 
              class="inline-flex items-center justify-center px-3 sm:px-5 py-2 sm:py-2.5 bg-surface-variant dark:bg-surface-dark-variant hover:bg-outline/20 dark:hover:bg-outline-dark/20 text-surface-on dark:text-surface-dark-on text-sm font-medium rounded-md3-full transition-all duration-200 flex-shrink-0"
            >
              <span class="hidden sm:inline whitespace-nowrap">로그인</span>
              <svg class="w-5 h-5 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
            </router-link>
          </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-6 lg:p-10 pb-24 lg:pb-10 bg-surface dark:bg-surface-dark transition-colors duration-300">
        <router-view />
      </main>

      <!-- MD3 Docked Toolbar (Mobile Only) -->
      <DockedToolbar />
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { useThemeStore } from '@/store/theme';
import PreloadLinks from '@/components/common/PreloadLinks.vue';
import NavigationRail from '@/components/common/NavigationRail.vue';
import DockedToolbar from '@/components/common/DockedToolbar.vue';
import GlobalSearch from '@/components/common/GlobalSearch.vue';
import { generatePortfolioPDF } from '@/utils/pdfGenerator';

const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const downloadingPDF = ref(false);

const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Login' });
};

const handlePDFDownload = async () => {
  if (downloadingPDF.value) return;
  
  try {
    downloadingPDF.value = true;
    await generatePortfolioPDF();
    // 성공 메시지는 브라우저의 다운로드 알림으로 대체
  } catch (error) {
    console.error('PDF 다운로드 실패:', error);
    alert('PDF 생성에 실패했습니다. 다시 시도해주세요.');
  } finally {
    downloadingPDF.value = false;
  }
};

onUnmounted(() => {
  authStore.clearTimer();
});
</script>
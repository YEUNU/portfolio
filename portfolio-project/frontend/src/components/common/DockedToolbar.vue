<template>
  <!-- MD3 Expressive Floating Toolbar + FAB - Mobile Only -->
  <div class="lg:hidden fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3">
    <!-- Floating Toolbar with Flutter Material Blue -->
    <nav 
      class="bg-primary-100 dark:bg-primary-800 shadow-md3-3 rounded-md3-full px-3 py-2 backdrop-blur-md"
    >
      <div class="flex items-center gap-2">
        <!-- Portfolio -->
        <router-link
          to="/"
          class="flex items-center justify-center gap-2 px-4 py-2.5 transition-all duration-200 rounded-md3-full"
          :class="isActive('/') 
            ? 'bg-primary dark:bg-primary-200 text-white dark:text-primary-900 shadow-md3-1' 
            : 'text-primary-900 dark:text-primary-100 hover:bg-primary-200/30 dark:hover:bg-primary-700/30'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <span class="text-sm font-medium">Portfolio</span>
        </router-link>

        <!-- About -->
        <router-link
          to="/about"
          class="flex items-center justify-center gap-2 px-4 py-2.5 transition-all duration-200 rounded-md3-full"
          :class="isActive('/about') 
            ? 'bg-primary dark:bg-primary-200 text-white dark:text-primary-900 shadow-md3-1' 
            : 'text-primary-900 dark:text-primary-100 hover:bg-primary-200/30 dark:hover:bg-primary-700/30'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="text-sm font-medium">About</span>
        </router-link>

        <!-- Contact -->
        <router-link
          to="/contact"
          class="flex items-center justify-center gap-2 px-4 py-2.5 transition-all duration-200 rounded-md3-full"
          :class="isActive('/contact') 
            ? 'bg-primary dark:bg-primary-200 text-white dark:text-primary-900 shadow-md3-1' 
            : 'text-primary-900 dark:text-primary-100 hover:bg-primary-200/30 dark:hover:bg-primary-700/30'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <span class="text-sm font-medium">Contact</span>
        </router-link>
      </div>
    </nav>

    <!-- FAB (Floating Action Button) - Admin Only -->
    <router-link
      v-if="authStore.isLoggedIn && authStore.isAdmin"
      to="/write"
      class="flex items-center justify-center w-14 h-14 bg-primary dark:bg-primary-dark text-primary-on dark:text-primary-dark-on rounded-md3-xl shadow-md3-3 hover:shadow-md3-4 transition-all duration-200 hover:scale-105"
      aria-label="글쓰기"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </router-link>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const route = useRoute();
const authStore = useAuthStore();

const isActive = (path) => {
  if (path === '/') {
    return route.name === 'Board' || route.name === 'PostDetail';
  }
  return route.path === path;
};
</script>

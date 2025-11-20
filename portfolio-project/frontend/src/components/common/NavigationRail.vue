<template>
  <!-- MD3 Expressive Navigation Rail - Desktop Only -->
  <nav 
    class="hidden lg:flex fixed left-0 top-0 bottom-0 w-20 bg-surface dark:bg-surface-dark border-r border-outline/20 dark:border-outline-dark/20 flex-col items-center py-6 z-40 shadow-md3-1"
  >
    <!-- Logo / Home -->
    <router-link 
      to="/" 
      class="flex items-center justify-center w-14 h-14 mb-8 text-primary dark:text-primary-dark hover:bg-surface-variant dark:hover:bg-surface-dark-variant rounded-md3-md transition-all duration-200"
    >
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    </router-link>

    <!-- Divider -->
    <div class="w-12 h-px bg-outline/20 dark:bg-outline-dark/20 mb-4"></div>

    <!-- Navigation Items -->
    <div class="flex-1 flex flex-col gap-2 w-full items-center">
      <!-- Portfolio -->
      <router-link
        to="/"
        class="group relative flex flex-col items-center justify-center w-14 h-14 transition-all duration-200"
      >
        <div 
          class="flex items-center justify-center w-full h-full rounded-md3-md transition-all duration-200"
          :class="isActive('/') 
            ? 'bg-primary-100 dark:bg-primary-800' 
            : 'hover:bg-surface-variant/50 dark:hover:bg-surface-dark-variant/50'"
        >
          <svg 
            class="w-6 h-6 transition-colors duration-200" 
            :class="isActive('/') 
              ? 'text-primary-900 dark:text-primary-100' 
              : 'text-surface-on dark:text-surface-dark-on'"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <!-- Indicator -->
        <div 
          v-if="isActive('/')"
          class="absolute -left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary dark:bg-primary-dark rounded-r-md3-full transition-all duration-200"
        ></div>
        <!-- Label on hover -->
        <div class="absolute left-full ml-4 px-3 py-1.5 bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on rounded-md3-sm text-sm font-medium opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-200 whitespace-nowrap shadow-md3-2 z-50 border border-outline/20 dark:border-outline-dark/20">
          Portfolio
        </div>
      </router-link>

      <!-- About -->
      <router-link
        to="/about"
        class="group relative flex flex-col items-center justify-center w-14 h-14 transition-all duration-200"
      >
        <div 
          class="flex items-center justify-center w-full h-full rounded-md3-md transition-all duration-200"
          :class="isActive('/about') 
            ? 'bg-primary-100 dark:bg-primary-800' 
            : 'hover:bg-surface-variant/50 dark:hover:bg-surface-dark-variant/50'"
        >
          <svg 
            class="w-6 h-6 transition-colors duration-200" 
            :class="isActive('/about') 
              ? 'text-primary-900 dark:text-primary-100' 
              : 'text-surface-on dark:text-surface-dark-on'"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <!-- Indicator -->
        <div 
          v-if="isActive('/about')"
          class="absolute -left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary dark:bg-primary-dark rounded-r-md3-full transition-all duration-200"
        ></div>
        <!-- Label on hover -->
        <div class="absolute left-full ml-4 px-3 py-1.5 bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on rounded-md3-sm text-sm font-medium opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-200 whitespace-nowrap shadow-md3-2 z-50 border border-outline/20 dark:border-outline-dark/20">
          About
        </div>
      </router-link>

      <!-- Contact -->
      <router-link
        to="/contact"
        class="group relative flex flex-col items-center justify-center w-14 h-14 transition-all duration-200"
      >
        <div 
          class="flex items-center justify-center w-full h-full rounded-md3-md transition-all duration-200"
          :class="isActive('/contact') 
            ? 'bg-primary-100 dark:bg-primary-800' 
            : 'hover:bg-surface-variant/50 dark:hover:bg-surface-dark-variant/50'"
        >
          <svg 
            class="w-6 h-6 transition-colors duration-200" 
            :class="isActive('/contact') 
              ? 'text-primary-900 dark:text-primary-100' 
              : 'text-surface-on dark:text-surface-dark-on'"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <!-- Indicator -->
        <div 
          v-if="isActive('/contact')"
          class="absolute -left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary dark:bg-primary-dark rounded-r-md3-full transition-all duration-200"
        ></div>
        <!-- Label on hover -->
        <div class="absolute left-full ml-4 px-3 py-1.5 bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on rounded-md3-sm text-sm font-medium opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-200 whitespace-nowrap shadow-md3-2 z-50 border border-outline/20 dark:border-outline-dark/20">
          Contact
        </div>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();

const isActive = (path) => {
  if (path === '/') {
    return route.name === 'Board' || route.name === 'PostDetail';
  }
  return route.path === path;
};
</script>

<template>
  <div>
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

    <!-- Content -->
    <div v-else>
      <PageHeader 
        v-if="!hideHeader && title"
        :title="title" 
        :edit-id="editId"
        :show-edit-button="showEditButton"
      />
      <div class="px-4">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import PageHeader from './PageHeader.vue';

defineProps({
  title: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  editId: {
    type: String,
    default: null
  },
  showEditButton: {
    type: Boolean,
    default: false
  },
  hideHeader: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <div 
    class="group relative bg-surface dark:bg-surface-dark rounded-md3-xl overflow-hidden cursor-pointer transform transition-all duration-300 hover:scale-[1.02] shadow-md3-1 hover:shadow-md3-3 border border-outline/20 dark:border-outline-dark/20"
    @click="$emit('click')"
  >
    <!-- Thumbnail with overlay gradient -->
    <div class="relative h-48 overflow-hidden">
      <div 
        v-if="thumbnailStyle.backgroundImage"
        :style="thumbnailStyle"
        class="w-full h-full bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
      ></div>
      <div 
        v-else
        class="w-full h-full bg-surface-variant dark:bg-surface-dark-variant flex items-center justify-center"
      >
        <svg class="w-16 h-16 text-surface-on-variant dark:text-surface-dark-on" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <div class="absolute inset-0 bg-surface-dark/60"></div>
    </div>

    <!-- Content -->
    <div class="p-5 space-y-3">
      <h2 class="text-xl font-bold text-surface-on dark:text-surface-dark-on line-clamp-2 group-hover:text-primary transition-colors duration-200">
        {{ post.title }}
      </h2>
      
      <!-- Tags -->
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="tag in tagList" 
          :key="tag"
          class="inline-flex items-center px-2.5 py-1 rounded-md3-sm text-xs font-medium bg-primary-100 dark:bg-primary-800 text-primary-900 dark:text-primary-100"
        >
          {{ tag }}
        </span>
      </div>

      <!-- Admin Actions -->
      <div v-if="showAdmin" class="flex gap-2 pt-2 border-t border-outline/20 dark:border-outline-dark/20">
        <BaseButton 
          variant="primary" 
          size="sm"
          @click.stop="$emit('edit')"
          class="flex-1"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          수정
        </BaseButton>
        <BaseButton 
          variant="danger" 
          size="sm"
          @click.stop="$emit('delete')"
          class="flex-1"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          삭제
        </BaseButton>
      </div>
    </div>

    <!-- Hover effect overlay -->
    <div class="absolute inset-0 border-2 border-primary rounded-md3-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300 pointer-events-none"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import api from '@/services/api';
import BaseButton from '@/components/common/BaseButton.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  showAdmin: {
    type: Boolean,
    default: false
  }
});

const thumbnailStyle = computed(() => {
  const firstImage = extractFirstImage(props.post.content);
  if (firstImage) {
    const fullUrl = firstImage.startsWith('/') 
      ? `${api.defaults.baseURL}${firstImage}` 
      : firstImage;
    return {
      backgroundImage: `url(${fullUrl})`
    };
  }
  return {};
});

const tagList = computed(() => {
  if (!props.post.tags) return [];
  return props.post.tags.split(',').map(tag => tag.trim()).filter(Boolean);
});

function extractFirstImage(content) {
  if (!content) return null;
  const regex = /!\[.*?\]\((.*?)\)/;
  const match = content.match(regex);
  return match ? match[1] : null;
}

defineEmits(['click', 'edit', 'delete']);
</script>

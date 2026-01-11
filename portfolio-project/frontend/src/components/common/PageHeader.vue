<template>
  <div class="px-4 mb-12">
    <h1 class="text-4xl md:text-5xl font-bold text-primary dark:text-primary-dark mb-2 animate-fade-in">
      {{ title }}
    </h1>
    <div class="h-1 w-20 bg-primary dark:bg-primary-dark rounded-md3-full"></div>
    <div v-if="showEditButton" class="mt-4">
      <router-link 
        :to="{ name: 'Edit', params: { id: editId } }" 
        class="inline-block px-4 py-2 bg-primary-100 dark:bg-primary-800 text-primary-900 dark:text-primary-100 rounded-md3-md hover:shadow-md3-2 transition-all duration-200"
      >
        수정하기
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  editId: {
    type: String,
    default: null
  },
  showEditButton: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}
</style>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="isOpen" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm cursor-zoom-out" @click="close">
        <div class="relative max-w-screen-xl max-h-screen p-2" @click.stop>
          <!-- 닫기 버튼 (모바일에서도 접근 쉽도록 화면 우측 상단 배치 고려) -->
          <button 
            type="button"
            class="absolute -top-12 right-0 p-2 text-white/70 hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-white/50 rounded-full"
            @click="close"
            aria-label="닫기"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <img 
            :src="imageUrl" 
            alt="Image preview" 
            class="max-h-[85vh] max-w-full w-auto h-auto rounded-lg shadow-2xl object-contain select-none bg-black/20"
            @click.stop
          />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  imageUrl: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

// 키보드 ESC 키로 닫기 지원
const handleKeydown = (e) => {
  if (props.isOpen && e.key === 'Escape') {
    close();
  }
};

// 모달이 열려있을 때 스크롤 방지
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
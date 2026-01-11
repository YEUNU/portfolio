<template>
  <div class="markdown-preview" v-html="renderedMarkdown" @click="handleImageClick"></div>
  <ImageModal :is-open="isModalOpen" :image-url="modalImageUrl" @close="closeModal" />
</template>

<script setup>
import { computed, ref } from 'vue';
import { renderMarkdownSafe } from '@/utils/markdown';
import ImageModal from '@/components/common/ImageModal.vue';

// 'content'라는 이름의 prop을 정의합니다. 부모 컴포넌트로부터 마크다운 문자열을 전달받습니다.
const props = defineProps({
  content: {
    type: String,
    default: '',
  },
});

// 전달받은 content prop을 안전한 HTML로 변환합니다.
// DOMPurify를 통해 XSS 공격이 방지됩니다.
const renderedMarkdown = computed(() => {
  return renderMarkdownSafe(props.content);
});

// 이미지 모달 상태 관리
const isModalOpen = ref(false);
const modalImageUrl = ref('');

const handleImageClick = (event) => {
  // 클릭된 요소가 이미지인지 확인
  if (event.target.tagName === 'IMG') {
    // 이미지를 감싸는 a 태그가 있는지 확인 (링크 이동 방지)
    const parentLink = event.target.closest('a');
    if (parentLink) {
        // 이미지가 링크 안에 있으면 모달을 띄우지 않고 링크 동작을 따름 (또는 e.preventDefault()로 막고 모달 띄우기 선택)
        // 여기서는 링크가 없는 순수 이미지일 때만 모달을 띄우는 것이 안전함.
        // 하지만 마크다운 에디터에서 이미지를 단순히 넣으면 a 태그 없이 들어가는 경우가 많음.
        // 만약 링크가 있어도 모달을 띄우고 싶다면 preventDefault 호출 필요.
        
        // 요구사항: "이미지 눌렀을 때 모달 해서 이미지 크게 볼 수 있는거"
        // 링크가 '새 탭 열기' 같은게 아니라면 모달이 우선일 수 있습니다.
        // 일단 a태그가 없을 때만 동작하게 합니다.
        return; 
    }

    modalImageUrl.value = event.target.src;
    isModalOpen.value = true;
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  // 닫기 애니메이션 시간 고려
  setTimeout(() => {
    if (!isModalOpen.value) modalImageUrl.value = '';
  }, 200);
};
</script>

<style scoped>
.markdown-preview {
  line-height: 1.7;
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  overflow-x: hidden;
  @apply text-surface-on dark:text-surface-dark-on;
}

/* 이미지 스타일 및 커서 추가 */
.markdown-preview :deep(img) {
  @apply rounded-lg my-6 cursor-zoom-in transition-all duration-200;
  max-height: 500px;
  width: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.markdown-preview :deep(img):hover {
  transform: scale(1.01);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 제목 스타일 */
.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3),
.markdown-preview :deep(h4),
.markdown-preview :deep(h5),
.markdown-preview :deep(h6) {
  @apply text-surface-on dark:text-surface-dark-on font-bold;
  border-bottom: 1px solid;
  @apply border-outline/30 dark:border-outline-dark/30;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.markdown-preview :deep(h1) {
  @apply text-3xl;
}

.markdown-preview :deep(h2) {
  @apply text-2xl;
}

.markdown-preview :deep(h3) {
  @apply text-xl;
}

/* 본문 텍스트 */
.markdown-preview :deep(p) {
  margin-bottom: 1rem;
  @apply text-surface-on dark:text-surface-dark-on;
}

/* 링크 */
.markdown-preview :deep(a) {
  @apply text-primary dark:text-primary-dark underline hover:text-primary-600 dark:hover:text-primary-300;
}

/* 인라인 코드 */
.markdown-preview :deep(code) {
  @apply bg-surface-variant dark:bg-surface-dark-variant text-surface-on dark:text-surface-dark-on;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}

/* 코드 블록 */
.markdown-preview :deep(pre) {
  @apply bg-surface-variant dark:bg-surface-dark-variant;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}

.markdown-preview :deep(pre) code {
  background-color: transparent;
  padding: 0;
  @apply text-surface-on dark:text-surface-dark-on;
}

/* 인용구 */
.markdown-preview :deep(blockquote) {
  @apply border-l-4 border-outline dark:border-outline-dark;
  padding-left: 1rem;
  margin-left: 0;
  @apply text-surface-on-variant dark:text-surface-dark-on;
}

/* 목록 */
.markdown-preview :deep(ul),
.markdown-preview :deep(ol) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.markdown-preview :deep(li) {
  @apply text-surface-on dark:text-surface-dark-on;
  margin-bottom: 0.5rem;
}

/* 테이블 */
.markdown-preview :deep(table) {
  @apply text-surface-on dark:text-surface-dark-on border border-outline dark:border-outline-dark;
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
}

.markdown-preview :deep(th),
.markdown-preview :deep(td) {
  @apply border border-outline dark:border-outline-dark;
  padding: 0.5rem;
}

.markdown-preview :deep(th) {
  @apply bg-surface-variant dark:bg-surface-dark-variant font-bold;
}

/* 강조 */
.markdown-preview :deep(strong) {
  @apply text-surface-on dark:text-surface-dark-on font-bold;
}

.markdown-preview :deep(em) {
  @apply text-surface-on dark:text-surface-dark-on italic;
}

.markdown-preview :deep(img) {
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  max-height: 500px; /* 최대 높이 제한 */
  border-radius: 8px;
  display: block;
  margin: 1rem auto; /* 중앙 정렬 */
  object-fit: contain; /* 이미지 비율 유지하며 컨테이너에 맞춤 */
}

/* 테이블이나 다른 요소 안의 이미지도 동일하게 처리 */
.markdown-preview :deep(table img),
.markdown-preview :deep(p img),
.markdown-preview :deep(div img) {
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  max-height: 500px;
}
</style>

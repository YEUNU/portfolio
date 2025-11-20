<template>
  <div class="markdown-preview" v-html="renderedMarkdown"></div>
</template>

<script setup>
import { computed } from 'vue';
import marked from '@/utils/markdown';

// 'content'라는 이름의 prop을 정의합니다. 부모 컴포넌트로부터 마크다운 문자열을 전달받습니다.
const props = defineProps({
  content: {
    type: String,
    default: '',
  },
});

// 전달받은 content prop을 HTML로 변환합니다.
const renderedMarkdown = computed(() => {
  return marked(props.content);
});
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

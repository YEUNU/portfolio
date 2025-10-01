<template>
  <div class="markdown-preview" v-html="renderedMarkdown"></div>
</template>

<script setup>
import { computed } from 'vue';
import marked from '@/utils/markdown'; // PageEditView에서 사용했던 동일한 마크다운 파서를 사용합니다.

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
}

/* v-html로 렌더링되는 컨텐츠는 scoped 스타일이 적용되지 않으므로,
  :deep() 선택자나 별도의 전역 스타일을 사용해야 합니다.
  여기서는 간단히 :deep()을 사용합니다.
*/
.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3) {
  border-bottom: 1px solid #444;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.markdown-preview :deep(p) {
  margin-bottom: 1rem;
}

.markdown-preview :deep(code) {
  background-color: #2a2a2a;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-preview :deep(pre) {
  background-color: #1e1e1e;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}

.markdown-preview :deep(pre) code {
  background-color: transparent;
  padding: 0;
}

.markdown-preview :deep(blockquote) {
  border-left: 4px solid #444;
  padding-left: 1rem;
  margin-left: 0;
  color: #aaa;
}

.markdown-preview :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>
<template>
  <div class="tiptap-editor">
    <!-- Toolbar -->
    <div v-if="editor" class="editor-toolbar bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 rounded-t-md3-md p-2 flex flex-wrap gap-1">
      <!-- Text Formatting -->
      <div class="toolbar-group">
        <button
          @click="editor.chain().focus().toggleBold().run()"
          :class="{ 'is-active': editor.isActive('bold') }"
          class="toolbar-btn"
          type="button"
          title="굵게 (Ctrl+B)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 4h8a4 4 0 014 4 4 4 0 01-4 4H6z M6 12h9a4 4 0 014 4 4 4 0 01-4 4H6z" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleItalic().run()"
          :class="{ 'is-active': editor.isActive('italic') }"
          class="toolbar-btn"
          type="button"
          title="기울임 (Ctrl+I)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 4h10M14 4v16M4 20h10" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleUnderline().run()"
          :class="{ 'is-active': editor.isActive('underline') }"
          class="toolbar-btn"
          type="button"
          title="밑줄 (Ctrl+U)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19h14M7 5v6a5 5 0 0010 0V5" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleStrike().run()"
          :class="{ 'is-active': editor.isActive('strike') }"
          class="toolbar-btn"
          type="button"
          title="취소선"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12h18M8 6h8M6 18h12" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleCode().run()"
          :class="{ 'is-active': editor.isActive('code') }"
          class="toolbar-btn"
          type="button"
          title="인라인 코드"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleHighlight({ color: '#fef08a' }).run()"
          :class="{ 'is-active': editor.isActive('highlight') }"
          class="toolbar-btn"
          type="button"
          title="형광펜"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10M9 18h6M9 15h6M5 12h.01M5 12l5-5m0 0L14 3l4 4-5 5" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleSubscript().run()"
          :class="{ 'is-active': editor.isActive('subscript') }"
          class="toolbar-btn"
          type="button"
          title="아래 첨자"
        >
          X<sub class="text-xs">₂</sub>
        </button>
        <button
          @click="editor.chain().focus().toggleSuperscript().run()"
          :class="{ 'is-active': editor.isActive('superscript') }"
          class="toolbar-btn"
          type="button"
          title="위 첨자"
        >
          X<sup class="text-xs">²</sup>
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Headings -->
      <div class="toolbar-group">
        <button
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 1"
        >
          H1
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 2"
        >
          H2
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 3"
        >
          H3
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 4"
        >
          H4
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 5 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 5"
        >
          H5
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 6 }).run()"
          :class="{ 'is-active': editor.isActive('heading', { level: 6 }) }"
          class="toolbar-btn"
          type="button"
          title="제목 6"
        >
          H6
        </button>
        <button
          @click="editor.chain().focus().setParagraph().run()"
          :class="{ 'is-active': editor.isActive('paragraph') }"
          class="toolbar-btn"
          type="button"
          title="본문"
        >
          P
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Lists -->
      <div class="toolbar-group">
        <button
          @click="editor.chain().focus().toggleBulletList().run()"
          :class="{ 'is-active': editor.isActive('bulletList') }"
          class="toolbar-btn"
          type="button"
          title="목록"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleOrderedList().run()"
          :class="{ 'is-active': editor.isActive('orderedList') }"
          class="toolbar-btn"
          type="button"
          title="번호 목록"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleTaskList().run()"
          :class="{ 'is-active': editor.isActive('taskList') }"
          class="toolbar-btn"
          type="button"
          title="체크리스트"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleBlockquote().run()"
          :class="{ 'is-active': editor.isActive('blockquote') }"
          class="toolbar-btn"
          type="button"
          title="인용구"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Insert -->
      <div class="toolbar-group">
        <button
          @click="setLink"
          :class="{ 'is-active': editor.isActive('link') }"
          class="toolbar-btn"
          type="button"
          title="링크"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
        </button>
        <button
          @click="$emit('upload-image')"
          class="toolbar-btn"
          type="button"
          title="이미지 업로드"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().toggleCodeBlock().run()"
          :class="{ 'is-active': editor.isActive('codeBlock') }"
          class="toolbar-btn"
          type="button"
          title="코드 블록"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </button>
        <button
          @click="insertTable"
          class="toolbar-btn"
          type="button"
          title="표 삽입"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().setHorizontalRule().run()"
          class="toolbar-btn"
          type="button"
          title="구분선"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14" />
          </svg>
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Table Operations (표 수정 기능들) -->
      <div v-if="editor.isActive('table')" class="toolbar-group">
        <button
          @click="editor.chain().focus().addColumnBefore().run()"
          class="toolbar-btn"
          type="button"
          title="왼쪽에 열 추가"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m-8-8h16" />
          </svg>
          ←
        </button>
        <button
          @click="editor.chain().focus().addColumnAfter().run()"
          class="toolbar-btn"
          type="button"
          title="오른쪽에 열 추가"
        >
          →
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m-8-8h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().deleteColumn().run()"
          class="toolbar-btn"
          type="button"
          title="열 삭제"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Col
        </button>
        <button
          @click="editor.chain().focus().addRowBefore().run()"
          class="toolbar-btn"
          type="button"
          title="위에 행 추가"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m-8-8h16" />
          </svg>
          ↑
        </button>
        <button
          @click="editor.chain().focus().addRowAfter().run()"
          class="toolbar-btn"
          type="button"
          title="아래에 행 추가"
        >
          ↓
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m-8-8h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().deleteRow().run()"
          class="toolbar-btn"
          type="button"
          title="행 삭제"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          Row
        </button>
        <button
          @click="editor.chain().focus().deleteTable().run()"
          class="toolbar-btn"
          type="button"
          title="표 삭제"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().mergeCells().run()"
          :disabled="!editor.can().mergeCells()"
          class="toolbar-btn"
          type="button"
          title="셀 병합"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().splitCell().run()"
          :disabled="!editor.can().splitCell()"
          class="toolbar-btn"
          type="button"
          title="셀 분할"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Text Align -->
      <div class="toolbar-group">
        <button
          @click="editor.chain().focus().setTextAlign('left').run()"
          :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }"
          class="toolbar-btn"
          type="button"
          title="왼쪽 정렬"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h10M4 18h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().setTextAlign('center').run()"
          :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
          class="toolbar-btn"
          type="button"
          title="가운데 정렬"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M7 12h10M4 18h16" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().setTextAlign('right').run()"
          :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }"
          class="toolbar-btn"
          type="button"
          title="오른쪽 정렬"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M10 12h10M4 18h16" />
          </svg>
        </button>
      </div>

      <div class="toolbar-divider"></div>

      <!-- Undo/Redo -->
      <div class="toolbar-group">
        <button
          @click="editor.chain().focus().undo().run()"
          :disabled="!editor.can().undo()"
          class="toolbar-btn"
          type="button"
          title="실행 취소 (Ctrl+Z)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
          </svg>
        </button>
        <button
          @click="editor.chain().focus().redo().run()"
          :disabled="!editor.can().redo()"
          class="toolbar-btn"
          type="button"
          title="다시 실행 (Ctrl+Y)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10h-10a8 8 0 00-8 8v2M21 10l-6 6m6-6l-6-6" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Editor Content -->
    <editor-content :editor="editor" class="editor-content" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import Underline from '@tiptap/extension-underline';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import Table from '@tiptap/extension-table';
import TableCell from '@tiptap/extension-table-cell';
import TableHeader from '@tiptap/extension-table-header';
import TableRow from '@tiptap/extension-table-row';
import TaskList from '@tiptap/extension-task-list';
import TaskItem from '@tiptap/extension-task-item';
import TextAlign from '@tiptap/extension-text-align';
import TextStyle from '@tiptap/extension-text-style';
import Color from '@tiptap/extension-color';
import Highlight from '@tiptap/extension-highlight';
import Subscript from '@tiptap/extension-subscript';
import Superscript from '@tiptap/extension-superscript';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { createLowlight } from 'lowlight';
import javascript from 'highlight.js/lib/languages/javascript';
import typescript from 'highlight.js/lib/languages/typescript';
import python from 'highlight.js/lib/languages/python';
import css from 'highlight.js/lib/languages/css';
import xml from 'highlight.js/lib/languages/xml';

// lowlight 인스턴스 생성 및 언어 등록
const lowlight = createLowlight();
lowlight.register('javascript', javascript);
lowlight.register('typescript', typescript);
lowlight.register('python', python);
lowlight.register('css', css);
lowlight.register('html', xml);
lowlight.register('xml', xml);

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue', 'upload-image']);

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      codeBlock: false, // CodeBlockLowlight를 사용하기 위해 비활성화
    }),
    Underline,
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: 'text-primary dark:text-primary-dark underline',
      },
    }),
    Image.configure({
      HTMLAttributes: {
        class: 'max-w-full h-auto rounded-md3-md',
      },
    }),
    Table.configure({
      resizable: true,
      HTMLAttributes: {
        class: 'border-collapse table-auto w-full',
      },
    }),
    TableRow,
    TableHeader,
    TableCell,
    TaskList,
    TaskItem.configure({
      nested: true,
    }),
    TextAlign.configure({
      types: ['heading', 'paragraph'],
    }),
    TextStyle,
    Color,
    Highlight.configure({
      multicolor: true,
    }),
    Subscript,
    Superscript,
    CodeBlockLowlight.configure({
      lowlight,
      HTMLAttributes: {
        class: 'bg-surface-variant dark:bg-surface-dark-variant p-4 rounded-md3-md overflow-x-auto',
      },
    }),
  ],
  editorProps: {
    attributes: {
      class: 'prose prose-invert max-w-none focus:outline-none h-[600px] overflow-y-auto p-4 bg-surface dark:bg-surface-dark border border-outline/30 dark:border-outline-dark/30 border-t-0 rounded-b-md3-md text-surface-on dark:text-surface-dark-on',
    },
  },
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML());
  },
});

// 링크 삽입
const setLink = () => {
  const previousUrl = editor.value.getAttributes('link').href;
  const url = window.prompt('URL을 입력하세요:', previousUrl);

  if (url === null) {
    return;
  }

  if (url === '') {
    editor.value.chain().focus().extendMarkRange('link').unsetLink().run();
    return;
  }

  editor.value.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
};

// 표 삽입
const insertTable = () => {
  editor.value.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run();
};

// 이미지 삽입 (외부에서 URL을 받아서)
const insertImage = (url) => {
  if (url) {
    editor.value.chain().focus().setImage({ src: url }).run();
  }
};

// modelValue 변경 감지
watch(() => props.modelValue, (value) => {
  const isSame = editor.value.getHTML() === value;
  if (isSame) {
    return;
  }
  editor.value.commands.setContent(value, false);
});

onBeforeUnmount(() => {
  editor.value?.destroy();
});

defineExpose({
  insertImage,
  editor,
});
</script>

<style scoped>
.tiptap-editor {
  @apply w-full;
}

.toolbar-group {
  @apply flex gap-1;
}

.toolbar-divider {
  @apply w-px bg-outline/30 dark:bg-outline-dark/30 mx-1;
}

.toolbar-btn {
  @apply p-2 rounded-md3-sm text-surface-on dark:text-surface-dark-on hover:bg-surface-variant dark:hover:bg-surface-dark-variant transition-colors duration-200;
}

.toolbar-btn.is-active {
  @apply bg-primary-100 dark:bg-primary-800 text-primary-900 dark:text-primary-100;
}

.toolbar-btn:disabled {
  @apply opacity-30 cursor-not-allowed;
}

/* TipTap 에디터 스타일 */
:deep(.ProseMirror) {
  @apply focus:outline-none;
}

:deep(.ProseMirror h1) {
  @apply text-4xl font-bold mb-4 text-primary dark:text-primary-dark;
}

:deep(.ProseMirror h2) {
  @apply text-3xl font-bold mb-3 text-primary dark:text-primary-dark;
}

:deep(.ProseMirror h3) {
  @apply text-2xl font-bold mb-2 text-primary dark:text-primary-dark;
}

:deep(.ProseMirror p) {
  @apply mb-3;
}

:deep(.ProseMirror ul),
:deep(.ProseMirror ol) {
  @apply pl-6 mb-3;
}

:deep(.ProseMirror ul) {
  @apply list-disc;
}

:deep(.ProseMirror ol) {
  @apply list-decimal;
}

:deep(.ProseMirror code) {
  @apply bg-surface-variant dark:bg-surface-dark-variant px-1.5 py-0.5 rounded text-sm;
}

:deep(.ProseMirror pre) {
  @apply bg-surface-variant dark:bg-surface-dark-variant p-4 rounded-md3-md overflow-x-auto mb-3;
}

:deep(.ProseMirror blockquote) {
  @apply border-l-4 border-primary dark:border-primary-dark pl-4 italic my-3;
}

:deep(.ProseMirror hr) {
  @apply my-6 border-outline/30 dark:border-outline-dark/30;
}

:deep(.ProseMirror a) {
  @apply text-primary dark:text-primary-dark underline cursor-pointer;
}

:deep(.ProseMirror img) {
  @apply max-w-full h-auto rounded-md3-md my-3;
}

:deep(.ProseMirror table) {
  @apply border-collapse table-auto w-full my-3;
}

:deep(.ProseMirror table td),
:deep(.ProseMirror table th) {
  @apply border border-outline/30 dark:border-outline-dark/30 px-3 py-2 text-left;
}

:deep(.ProseMirror table th) {
  @apply bg-surface-variant dark:bg-surface-dark-variant font-bold;
}

:deep(.ProseMirror ul[data-type="taskList"]) {
  @apply list-none pl-0;
}

:deep(.ProseMirror ul[data-type="taskList"] li) {
  @apply flex items-start gap-2;
}

:deep(.ProseMirror ul[data-type="taskList"] li input[type="checkbox"]) {
  @apply mt-1;
}
</style>

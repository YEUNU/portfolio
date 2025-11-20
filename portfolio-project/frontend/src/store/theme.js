import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  // 초기값을 localStorage에서 가져오거나 시스템 설정 사용
  const isDark = ref(
    localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  // 다크모드 토글 함수
  const toggleTheme = () => {
    isDark.value = !isDark.value;
  };

  // 다크모드 상태가 변경되면 localStorage와 HTML 클래스 업데이트
  watch(isDark, (newValue) => {
    if (newValue) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, { immediate: true });

  return {
    isDark,
    toggleTheme,
  };
});

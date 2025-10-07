<script>
import { onMounted } from 'vue';

export default {
  name: 'PreloadLinks',
  props: {
    urls: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    onMounted(() => {
      // 중요한 리소스들을 미리 로드하도록 link 태그 추가
      const preloadUrls = [
        '/api/v1/board/tags', // 태그 목록
        '/api/v1/board/', // 메인 게시글 목록
        ...props.urls
      ];

      preloadUrls.forEach(url => {
        // 이미 preload된 URL인지 확인
        if (!document.querySelector(`link[href="${url}"]`)) {
          const link = document.createElement('link');
          link.rel = 'preload';
          link.href = url;
          link.as = 'fetch';
          link.crossOrigin = 'anonymous';
          document.head.appendChild(link);
        }
      });
    });

    // 렌더링하지 않음
    return () => null;
  }
};
</script>
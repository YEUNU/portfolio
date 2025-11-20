<script>
import { onMounted } from 'vue';

export default {
  name: 'PreloadLinks',
  props: {
    urls: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    onMounted(() => {
      // API 요청은 preload하지 않음 (효과가 없고 경고만 발생)
      // 필요시 정적 리소스(이미지, 폰트 등)만 preload
      const preloadUrls = [
        ...props.urls, // 외부에서 전달된 정적 리소스만 preload
      ];

      preloadUrls.forEach((url) => {
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
  },
};
</script>

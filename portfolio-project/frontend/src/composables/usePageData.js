import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useMeta } from '@/composables/useMeta';

/**
 * About/Contact 같은 정적 페이지 데이터를 가져오는 재사용 가능한 composable
 * @param {string} slug - 페이지 식별자 (about, contact 등)
 * @param {Object} metaConfig - SEO 메타 데이터 설정
 */
export function usePageData(slug, metaConfig = {}) {
  const page = ref(null);
  const loading = ref(true);
  const error = ref(null);
  const { updateMeta, addStructuredData } = useMeta();

  const fetchPage = async () => {
    try {
      loading.value = true;
      error.value = null;
      const response = await api.get(`/api/v1/board/slug/${slug}`);
      page.value = response.data;

      // SEO 메타 데이터 설정
      if (metaConfig.title || metaConfig.description) {
        updateMeta({
          title: metaConfig.title || `${page.value.title} - 성연우의 포트폴리오`,
          description: metaConfig.description || page.value.title,
          keywords: metaConfig.keywords || `성연우, ${slug}`,
          canonical: metaConfig.canonical || `https://your-domain.com/${slug}`,
        });
      }

      // 구조화된 데이터 추가
      if (metaConfig.structuredData) {
        addStructuredData({
          '@context': 'https://schema.org',
          ...metaConfig.structuredData,
          name: page.value.title,
          url: metaConfig.canonical || `https://your-domain.com/${slug}`,
        });
      }
    } catch (err) {
      console.error(`Failed to load ${slug} page:`, err);
      error.value = '페이지를 불러오는 데 실패했습니다.';
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    fetchPage();
  });

  return {
    page,
    loading,
    error,
    refetch: fetchPage,
  };
}

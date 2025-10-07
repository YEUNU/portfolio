import { ref, watch } from 'vue';

// 현재 페이지의 메타 정보를 관리하는 composable
export function useMeta() {
  const title = ref('성연우의 포트폴리오');
  const description = ref('성연우의 개발자 포트폴리오입니다.');
  const keywords = ref('성연우, 포트폴리오, 개발자, 웹개발');
  const ogImage = ref('/og-image.jpg');

  // 메타 태그 업데이트 함수
  const updateMeta = (metaData) => {
    if (metaData.title) {
      title.value = metaData.title;
      document.title = metaData.title;
    }
    
    if (metaData.description) {
      description.value = metaData.description;
      updateMetaTag('name', 'description', metaData.description);
      updateMetaTag('property', 'og:description', metaData.description);
      updateMetaTag('name', 'twitter:description', metaData.description);
    }
    
    if (metaData.keywords) {
      keywords.value = metaData.keywords;
      updateMetaTag('name', 'keywords', metaData.keywords);
    }
    
    if (metaData.ogImage) {
      ogImage.value = metaData.ogImage;
      updateMetaTag('property', 'og:image', metaData.ogImage);
      updateMetaTag('name', 'twitter:image', metaData.ogImage);
    }
    
    // 페이지별 canonical URL 설정
    if (metaData.canonical) {
      updateCanonicalUrl(metaData.canonical);
    }
  };

  // 메타 태그 업데이트 헬퍼 함수
  const updateMetaTag = (attribute, name, content) => {
    let element = document.querySelector(`meta[${attribute}="${name}"]`);
    if (element) {
      element.setAttribute('content', content);
    } else {
      element = document.createElement('meta');
      element.setAttribute(attribute, name);
      element.setAttribute('content', content);
      document.getElementsByTagName('head')[0].appendChild(element);
    }
  };

  // Canonical URL 업데이트
  const updateCanonicalUrl = (url) => {
    let link = document.querySelector('link[rel="canonical"]');
    if (link) {
      link.setAttribute('href', url);
    } else {
      link = document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', url);
      document.getElementsByTagName('head')[0].appendChild(link);
    }
  };

  // 구조화된 데이터 추가
  const addStructuredData = (data) => {
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(data);
    document.getElementsByTagName('head')[0].appendChild(script);
  };

  return {
    title,
    description,
    keywords,
    ogImage,
    updateMeta,
    addStructuredData
  };
}
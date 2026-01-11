import { ref } from 'vue';

// 현재 페이지의 메타 정보를 관리하는 composable
export function useMeta() {
  const title = ref('성연우의 포트폴리오');
  const description = ref('성연우의 개발자 포트폴리오입니다.');
  const keywords = ref('성연우, Portfolio, AI Engineer, Software Developer');
  const ogImage = ref('/og-image.jpg');

  const toAbsoluteUrl = (url) => {
    if (!url) return '';
    try {
      return new URL(url, window.location.origin).href;
    } catch (e) {
      return url;
    }
  };

  // 메타 태그 업데이트 함수
  const updateMeta = (metaData) => {
    if (metaData.title) {
      title.value = metaData.title;
      document.title = metaData.title;
      updateMetaTag('property', 'og:title', metaData.title);
      updateMetaTag('name', 'twitter:title', metaData.title);
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
      const absImage = toAbsoluteUrl(metaData.ogImage);
      ogImage.value = absImage;
      updateMetaTag('property', 'og:image', absImage);
      updateMetaTag('name', 'twitter:image', absImage);
    }

    // 페이지별 canonical URL 설정
    if (metaData.canonical) {
      const absCanonical = toAbsoluteUrl(metaData.canonical);
      updateCanonicalUrl(absCanonical);
      updateMetaTag('property', 'og:url', absCanonical);
      updateMetaTag('name', 'twitter:url', absCanonical);
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

  // 구조화된 데이터 추가 (동일 키를 교체해 중복 방지)
  const addStructuredData = (data, id = 'dynamic-ld-json') => {
    const head = document.getElementsByTagName('head')[0];
    const prev = head.querySelector(`script[type="application/ld+json"][data-meta-id="${id}"]`);
    if (prev) {
      head.removeChild(prev);
    }

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.setAttribute('data-meta-id', id);
    script.text = JSON.stringify(data);
    head.appendChild(script);
  };

  return {
    title,
    description,
    keywords,
    ogImage,
    updateMeta,
    addStructuredData,
  };
}

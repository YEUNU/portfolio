<template>
  <div class="board-container">
    <!-- 왼쪽 사이드바: 태그 필터 -->
    <aside class="sidebar">
      <h2 class="sidebar-title">Categories</h2>
      <ul class="tag-list">
        <li
          @click="filterByTag(null)"
          :class="{ active: !selectedTag }"
          class="tag-item"
        >
          All Posts
        </li>
        <li
          v-for="tag in allTags"
          :key="tag"
          @click="filterByTag(tag)"
          :class="{ active: selectedTag === tag }"
          class="tag-item"
        >
          {{ tag }}
        </li>
      </ul>
    </aside>

    <!-- 메인 콘텐츠: 게시글 갤러리 -->
    <main class="main-content">
      <h1 class="page-title">Portfolio</h1>
      <div v-if="loading" class="loading-spinner"></div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="!loading && !error" class="posts-grid">
        <!-- ✅ 수정: 게시물 카드를 클릭하면 상세 페이지로 이동 -->
        <div v-for="post in posts" :key="post.id" class="post-card" @click="viewPost(post.id)">
          <!-- ✅ 수정: 게시물 내용에서 첫 이미지를 찾아 썸네일로 설정 -->
          <div
            class="post-thumbnail"
            :style="getFirstImage(post.content) ? { backgroundImage: `url(${getFirstImage(post.content)})` } : {}"
          ></div>
          <div class="post-info">
            <h2 class="post-title">{{ post.title }}</h2>
            <p class="post-tags">{{ post.tags }}</p>
            <div v-if="authStore.isAdmin" class="admin-actions">
              <!-- ✅ 수정: .stop 수식어를 추가하여 이벤트 버블링 방지 -->
              <button @click.stop="editPost(post.id)" class="btn-edit">수정</button>
              <button @click.stop="deletePost(post.id)" class="btn-delete">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

const posts = ref([]);
const allTags = ref([]);
const selectedTag = ref(null);
const loading = ref(true);
const error = ref(null);
const router = useRouter();
const authStore = useAuthStore();

// ✅ 추가: Markdown 내용에서 첫 번째 이미지 URL을 추출하는 함수
const getFirstImage = (content) => {
  if (!content) return null;
  // 정규표현식을 사용하여 마크다운 이미지 URL을 찾습니다.
  const regex = /!\[.*?\]\((.*?)\)/;
  const match = content.match(regex);
  if (match && match[1]) {
    const imageUrl = match[1];
    // 상대 경로인 경우, 전체 URL을 구성합니다.
    if (imageUrl.startsWith('/')) {
      return `${api.defaults.baseURL}${imageUrl}`;
    }
    return imageUrl; // 이미 전체 URL인 경우
  }
  return null; // 이미지가 없는 경우
};

const fetchAllTags = async () => {
  try {
    const response = await api.get('/api/v1/board/tags');
    allTags.value = response.data;
  } catch (err) {
    console.error('Failed to fetch tags:', err);
  }
};

const fetchPosts = async () => {
  try {
    loading.value = true;
    let url = '/api/v1/board/';
    if (selectedTag.value) {
      url += `?tags=${selectedTag.value}`;
    }
    const response = await api.get(url);
    posts.value = response.data;
    error.value = null;
  } catch (err) {
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

const filterByTag = (tag) => {
  selectedTag.value = tag;
  fetchPosts();
};

onMounted(() => {
  fetchAllTags();
  fetchPosts();
});

// ✅ 추가: 게시물 상세 보기 페이지로 이동하는 함수
const viewPost = (id) => {
  router.push({ name: 'PostDetail', params: { id } });
};

const editPost = (id) => {
  router.push({ name: 'Edit', params: { id } });
};

const deletePost = async (id) => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/v1/board/${id}`);
      fetchPosts();
      fetchAllTags();
    } catch (err) {
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};
</script>

<style scoped>
.board-container {
  display: flex;
  color: #fff;
}
.sidebar {
  width: 250px;
  padding-right: 30px;
  border-right: 1px solid #333;
}
.sidebar-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
}
.tag-list {
  list-style: none;
  padding: 0;
}
.tag-item {
  padding: 10px 0;
  cursor: pointer;
  transition: color 0.2s;
}
.tag-item:hover, .tag-item.active {
  color: #3d8bfd;
}
.main-content {
  flex: 1;
  padding-left: 40px;
}
.page-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #fff;
    margin-bottom: 30px;
}
.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}
.post-card {
    background-color: #1e1e1e;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    cursor: pointer;
}
.post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
.post-thumbnail {
    width: 100%;
    height: 200px;
    background-color: #333;
    /* --- ✅ 추가: 배경 이미지 스타일 --- */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.post-info {
    padding: 20px;
}
.post-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0 0 10px 0;
    color: #f0f0f0;
}
.post-tags {
    font-size: 0.9rem;
    color: #757575;
    margin-bottom: 15px;
}
.admin-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}
.btn-edit, .btn-delete {
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: pointer;
}
.btn-edit {
    background-color: #3d8bfd;
    color: white;
}
.btn-delete {
    background-color: #e53935;
    color: white;
}
</style>


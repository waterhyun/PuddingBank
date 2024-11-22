<template>
  <div>
    <h1>게시글 목록 페이지</h1>

    <!-- 게시글 작성 버튼 및 내가 쓴 글 보기 버튼 -->
    <div class="create-button-container">
      <div>
        <router-link v-if="authStore.isAuthenticated" :to="{ name: 'ArticleCreate' }" class="create-button">
          게시글 작성
        </router-link>
        <button v-else @click="redirectToLogin" class="create-button">
          게시글 작성
        </button>
      </div>
      <div>
        <button @click="toggleMyArticles" class="my-articles-button">
          {{ showMyArticles ? "전체 글 보기" : "내가 쓴 글 보기" }}
        </button>
      </div>
    </div>

    <!-- 검색창 -->
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="작성자, 제목, 내용"
        class="search-input"
      />
      <button @click="filterArticlesBySearch" class="search-button">검색</button>
    </div>

    <hr />

    <!-- 카테고리 탭 -->
    <div class="category-tabs">
      <div
        v-for="category in categories"
        :key="category"
        @click="selectCategory(category)"
        :class="{ active: currentCategory === category }"
        class="category-tab"
      >
        {{ category }}
        <span class="count">({{ getArticleCount(category) }})</span>
      </div>
    </div>

    <hr />

    <!-- 부합한 글이 없는 경우 -->
    <div v-if="filteredArticles.length === 0" class="no-articles">
      '{{searchQuery}}'에 대한 검색어가 없습니다.
    </div>

    <!-- 게시글 목록 -->
    <div v-else>
      <ArticleList :articles="filteredArticles" />
    </div>
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { ref, onMounted, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'

const articleStore = useArticleStore()
const authStore = useAuthStore()
const router = useRouter()

const currentCategory = ref('전체') // 현재 선택된 카테고리
const categories = ref(['전체', '공지', '자유', '질문', '추천']) // 모든 카테고리 목록
const searchQuery = ref('') // 검색어 상태 추가
const showMyArticles = ref(false) // 내가 쓴 글 보기 상태

onMounted(() => {
  articleStore.getArticles()
})

// 검색어와 카테고리에 따라 필터링된 게시글
const filteredArticles = computed(() => {
  const categoryFiltered = currentCategory.value === '전체'
    ? articleStore.articles
    : articleStore.articles.filter(
        article => article.category_display === currentCategory.value
      );

  const myArticlesFiltered = showMyArticles.value
    ? categoryFiltered.filter(article => article.username === authStore.user?.username)
    : categoryFiltered;

  // 검색어 필터링 추가
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    return myArticlesFiltered.filter(article => {
      const title = article.title?.toLowerCase() || '';
      const content = article.content?.toLowerCase() || '';
      const author = article.author?.toLowerCase() || '';
      return title.includes(query) || content.includes(query) || author.includes(query);
    });
  }
  return myArticlesFiltered;
});

// 특정 카테고리의 게시글 수 반환
const getArticleCount = (category) => {
  if (category === '전체') {
    return articleStore.articles.length
  }
  return articleStore.articles.filter(
    article => article.category_display === category
  ).length
}

// 내가 쓴 글 보기 토글
const toggleMyArticles = () => {
  console.log('Current User:', authStore.user); // 디버깅 로그 추가
  console.log('Show My Articles:', showMyArticles.value); // 상태 확인
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.');
    return;
  }
  showMyArticles.value = !showMyArticles.value;
};

// 로그인 페이지로 리다이렉트
const redirectToLogin = () => {
  alert('로그인이 필요한 서비스입니다.')
  router.push({ name: 'Login' })
}
</script>

<style scoped>
/* 게시글 작성 버튼 컨테이너 */
.create-button-container {
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
  align-items: center; /* 높이 정렬 */
  gap: 10px; /* 버튼 간 간격 */
  margin-bottom: 20px;
}

/* 게시글 작성 버튼 스타일 */
.create-button,
.my-articles-button {
  display: inline-flex; /* 버튼 내부 콘텐츠 정렬 */
  align-items: center; /* 텍스트 세로 정렬 */
  justify-content: center; /* 텍스트 가로 정렬 */
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-button:hover,
.my-articles-button:hover {
  background-color: #0056b3;
}

.create-button:active,
.my-articles-button:active {
  background-color: #004494;
}
/* 검색창 스타일 */
.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px 0 0 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #5a6268;
}

/* 카테고리 탭 */
.category-tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.category-tab {
  padding: 10px 20px;
  cursor: pointer;
  font-weight: bold;
  color: #6c757d; /* 기본 회색 */
  border-bottom: 2px solid transparent; /* 기본 밑줄 숨김 */
  transition: color 0.2s ease, border-bottom 0.2s ease;
}

.category-tab:hover {
  color: #007bff; /* 호버 시 파란색 */
}

.category-tab.active {
  color: #007bff; /* 활성화된 탭 파란색 */
  border-bottom: 2px solid #007bff; /* 활성화된 밑줄 */
}

.count {
  font-weight: normal;
  color: #6c757d;
  margin-left: 5px;
}

/* 부합한 글 없음 스타일 */
.no-articles {
  text-align: center;
  color: #6c757d;
  font-size: 16px;
  margin-top: 20px;
}
</style>

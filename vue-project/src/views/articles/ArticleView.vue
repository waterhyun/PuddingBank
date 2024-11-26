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

// 카테고리 선택 함수
const selectCategory = (category) => {
  currentCategory.value = category
}

// 로그인 페이지로 리다이렉트
const redirectToLogin = () => {
  alert('로그인이 필요한 서비스입니다.')
  router.push({ name: 'Login' })
}
</script>


<template>
  <div class="community-container">
    <h1 class="community-title">커뮤니티</h1>

    <!-- 상단 버튼 영역 -->
    <div class="action-container">
      <div class="button-group">
        <router-link 
          v-if="authStore.isAuthenticated" 
          :to="{ name: 'ArticleCreate' }" 
          class="btn create-btn"
        >
          글쓰기
        </router-link>
        <button 
          v-else 
          @click="redirectToLogin" 
          class="btn create-btn"
        >
          글쓰기
        </button>
        <button 
          @click="toggleMyArticles" 
          class="btn toggle-btn"
        >
          {{ showMyArticles ? "전체 글 보기" : "내가 쓴 글 보기" }}
        </button>
      </div>

      <!-- 검색 영역 -->
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="검색어를 입력하세요"
          class="search-input"
        />
        <button @click="filterArticlesBySearch" class="btn search-btn">
          검색
        </button>
      </div>
    </div>

    <!-- 카테고리 탭 -->
    <div class="category-tabs">
      <button
        v-for="category in categories"
        :key="category"
        @click="selectCategory(category)"
        :class="['category-tab', { active: currentCategory === category }]"
      >
        {{ category }}
        <span class="count">({{ getArticleCount(category) }})</span>
      </button>
    </div>

    <!-- 검색 결과 없음 -->
    <div v-if="filteredArticles.length === 0" class="empty-result">
      '{{ searchQuery }}'에 대한 검색 결과가 없습니다.
    </div>

    <!-- 게시글 목록 -->
    <div v-else class="article-container">
      <ArticleList :articles="filteredArticles" />
    </div>
  </div>
</template>

<style scoped>
.community-container {
  max-width: 1400px;
  margin: 24px auto;
  padding: 32px;
  background-color: #fffefb;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(115, 85, 60, 0.12);
}

.community-title {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 16px;
  font-size: 32px;
  line-height: 1.4;
}

/* 상단 버튼 영역 */
.action-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

/* 버튼 스타일 */
.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-family: 'jjinbbangM';
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn {
  background: #FDE49B;
  color: #73553C;
  text-decoration: none;
}

.toggle-btn {
  background: #73553C;
  color: #FFFEFB;
}

.search-btn {
  background: #FEF0AC;
  color: #73553C;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
}

/* 검색 영역 */
.search-container {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  padding: 0.8rem 1rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  width: 300px;
}

.search-input:focus {
  outline: none;
  border-color: #73553C;
}

/* 카테고리 탭 */
.category-tabs {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  padding: 1rem 0;
  border-top: 1px solid #FDE49B;
  border-bottom: 1px solid #FDE49B;
}

.category-tab {
  padding: 0.6rem 1.2rem;
  border: none;
  background: none;
  font-family: 'jjinbbangM';
  color: #73553C;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.6;
}

.category-tab:hover {
  opacity: 1;
}

.category-tab.active {
  opacity: 1;
  background: #FEF0AC;
  border-radius: 20px;
}

.count {
  font-size: 0.9rem;
  margin-left: 0.3rem;
}

/* 검색 결과 없음 */
.empty-result {
  text-align: center;
  padding: 3rem;
  font-family: 'jjinbbangM';
  color: #73553C;
  background: #FEF0AC;
  border-radius: 12px;
  margin: 2rem 0;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin: 32px auto 0;
  padding: 32px;
  background: #FFFEFB;
  border-radius: 16px;
  border: 3px solid #FDE49B;
  min-height: 500px;
}


/* 반응형 */
@media (max-width: 1440px) {
  .community-container {
    margin: 16px;
    padding: 24px;
  }
  
  .content-wrapper {
    padding: 24px;
    gap: 24px;
  }
}

@media (max-width: 1024px) {
  .community-container {
    margin: 16px;
    padding: 24px;
  }

  h1 {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .community-container {
    margin: 8px;
    padding: 16px;
  }

  h1 {
    font-size: 24px;
  }

  .content-wrapper {
    padding: 16px;
  }
}

@media (max-width: 768px) {
  .action-container {
    flex-direction: column;
  }

  .search-container {
    width: 100%;
  }

  .search-input {
    width: 100%;
  }

  .category-tabs {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>

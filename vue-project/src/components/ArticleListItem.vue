<template>
  <div class="article-card">
    <RouterLink
      :to="{ 
        name: 'ArticleDetail', 
        params: { id: article.id }
      }"
      class="article-link"
    >
      <!-- 카테고리 표시 -->
      <div class="article-category">
        {{ article.category_display }}
      </div>
      <!-- 게시글 제목 및 정보 -->
      <h2 class="article-title">{{ article.id }}번 게시글</h2>
      <p class="article-info">
        <strong>제목:</strong> {{ article.title }}
      </p>
      <div class="article-stats">
        <span class="stat-item">
          <i class="fas fa-heart"></i>
          {{ article.like_count }}
        </span>
        <span class="stat-item">
          <i class="fas fa-comment"></i>
          {{ article.comment_count }}
        </span>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
defineProps({
  article: Object,
});

</script>

<style scoped>
.article-card {
  padding: 20px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.article-category {
  color: #007bff; /* 파란색으로 강조 */
  font-weight: bold;
  margin-bottom: 5px; /* 제목과 약간의 간격 추가 */
  display: inline-block;
}

.article-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 0 10px;
}

.article-info {
  font-size: 1rem;
  margin: 0 0 10px;
}

.article-stats {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.stat-item i.fa-heart {
  color: #ff4757;
}

.stat-item i.fa-comment {
  color: #2f3542;
}
</style>
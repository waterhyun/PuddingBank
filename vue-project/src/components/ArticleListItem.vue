<!-- ArticleListItem.vue -->
<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  article: Object,
});

const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString();
}
</script>

<template>
  <div class="article-card">
    <RouterLink
      :to="{ name: 'ArticleDetail', params: { id: article.id }}"
      class="article-link"
    >
      <div class="article-header">
        <div class="article-main-info">
          <span class="article-category">{{ article.category_display }}</span>
          <span class="separator">|</span>
          <span class="article-title">{{ article.title }}</span>
        </div>
      </div>
      
      <div class="article-footer">
        <div class="article-sub-info">
          <span class="article-date">{{ formatDate(article.created_at) }}</span>
          <span class="separator">|</span>
          <span class="article-author">{{ article.username }}</span>
        </div>
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
      </div>
    </RouterLink>
  </div>
</template>

<style scoped>
.article-card {
  background: #FFFEFB;
  border: 1px solid #FDE49B;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.1);
  border-color: #73553C;
}

.article-link {
  text-decoration: none;
  color: inherit;
  display: block;
  padding: 1.2rem 1rem 0.5rem 1rem;
}

.article-header, .article-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.article-main-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.article-sub-info {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.article-category {
  font-family: 'jjinbbangM';
  color: #73553C;
  font-size: 0.9rem;
  padding: 0.2rem 0.8rem;
  background: #FEF0AC;
  border-radius: 12px;
  white-space: nowrap;
}

.separator {
  color: #73553C;
  opacity: 0.5;
}

.article-title {
  font-family: 'jjinbbangB';
  color: #73553C;
  font-size: 1.1rem;
}

.article-author {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem;
  padding: 0.1rem;
}

.article-date {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem;
  padding: 0.3rem;
}

.article-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem;
}

.stat-item i.fa-heart {
  color: #FF9B9B;
}

.stat-item i.fa-comment {
  color: #73553C;
}
</style>

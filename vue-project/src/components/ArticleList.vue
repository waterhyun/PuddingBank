<!-- ArticleList.vue -->
<template>
  <div class="articles-container">
    <ArticleListItem 
      v-for="article in articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import { useArticleStore } from '@/stores/article'
import ArticleListItem from './ArticleListItem.vue';

defineProps({
  articles: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.articles-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}
</style>

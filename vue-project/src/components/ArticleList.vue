<template>
  <div>

    <!-- Article 데이터를 반복 렌더링 -->
    <ArticleListItem 
      v-for="article in articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
// import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article'
import ArticleListItem from './ArticleListItem.vue';
defineProps({
  articles: {
    type: Array,
    required: true
  }
})
// const store = useArticleStore()
// onMounted(() => {
//   store.getArticles()
// })

// console.log(store.articles)

</script>

<style scoped>

</style>

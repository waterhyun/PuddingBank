<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
    v-for="article in store.articles"
    :key="article.id"
    :article="article"
    />
    
  </div>
</template>

<script setup>
// import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/articles'
import ArticleListItem from './ArticleListItem.vue';
const store = useArticleStore()
// onMounted(() => {
//   store.getArticles()
// })

// console.log(store.articles)
</script>

<style lang="scss" scoped>

</style>

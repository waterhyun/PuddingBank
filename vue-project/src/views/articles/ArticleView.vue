<template>
  <div>
    <h1>게시글 목록 페이지</h1>
    <RouterLink :to="{name: 'create'}"><button>게시글 생성</button></RouterLink>
    <hr>
    <ArticleList />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article'
import ArticleList from '@/components/ArticleList.vue';

const store = useArticleStore()

onMounted(() => {
  store.getArticles()
})

// console.log(store.articles)

</script>

<style lang="scss" scoped>

</style>
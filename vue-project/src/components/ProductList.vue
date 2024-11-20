<template>
  <div>
    <h3>Products List</h3>
    <ProductListItem 
    v-for="article in store.articles"
    :key="article.id"
    :article="article"
    />
    
  </div>
</template>

<script setup>
// import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article'
import ProductListItem from './ProductListItem.vue';
const store = useArticleStore()

</script>

<style scoped>

</style>
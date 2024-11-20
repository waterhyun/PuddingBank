<template>
  <div>
    <h2>상품 페이지</h2>
    <ProductList />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article'
import ProductList from '@/components/ProductList.vue';

const store = useArticleStore()

onMounted(() => {
  store.getArticles()
})

</script>

<style scoped>

</style>
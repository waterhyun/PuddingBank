<template>
  <div>
    <h1>상세페이지</h1>
    <h1 class="detail-title">{{ id }}</h1>
    <p class="detail-content">{{ store.articles.values[0] }}</p>
    <div class="detail-meta">
      <!-- <span class="detail-author">작성자: {{ article.author }}</span>
      <span class="detail-date">작성일: {{ article.date }}</span> -->
    </div>
    <RouterLink to="/articles/">목록으로 돌아가기</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { onMounted } from 'vue';
const store = useArticleStore()
onMounted(() => {
  store.getArticles()
})
console.log(store.articles)
// useRoute를 사용하여 params에서 id와 title 가져오기
const route = useRoute();
const id = route.params.id; // 전달받은 id
// const title = route.params.title; // 전달받은 title

console.log("ID:", id);
// console.log("Title:", title);
// defineProps({
//   id: Number,
//   title: Object,
// });
</script>

<style scoped>

</style>

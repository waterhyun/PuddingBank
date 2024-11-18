<!-- <template>
  <div>
    <h2>{{ idx+1 }}번 게시글</h2>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <RouterLink :to="{name:'detail'}">상세보기</RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
defineProps({
  article:Object,
  idx:Number,
})
</script>

<style scoped>

</style> -->

<template>
  <div class="article-card">
    <!-- <h2>게시글</h2> -->
    <h2 class="article-title">{{ article.id }}번 게시글</h2>
    <p class="article-info"><strong>제목:</strong> {{ article.title }}</p>
    <!-- <p class="article-content"><strong>내용:</strong> {{ article.content }}</p> -->
    <!-- <RouterLink :to="{ name: 'articledetail', params:{id:article.id}}" class="detail-link">
      상세보기
    </RouterLink> -->
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
defineProps({
  article: Object,
});

// console.log(article)

</script>

<style scoped>
.article-card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease-in-out;
}

.article-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.article-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 8px;
}

.article-info,
.article-content {
  font-size: 1rem;
  color: #555;
  margin-bottom: 8px;
}

.detail-link {
  display: inline-block;
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: background-color 0.3s ease-in-out;
}

.detail-link:hover {
  background-color: #0056b3;
}
</style>

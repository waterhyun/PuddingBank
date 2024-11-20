<template>
  <RouterLink
    :to="{ 
      name: 'articledetail', 
      params: { id: article.id }
    }"
    class="article-card"
  >
    <h2 class="article-title">{{ article.id }}번 게시글</h2>
    <p class="article-info"><strong>제목:</strong> {{ article.title }}</p>
  </RouterLink>
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
  display: block; /* 박스 전체를 클릭 가능 영역으로 설정 */
  padding: 20px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  text-decoration: none; /* 기본 링크 스타일 제거 */
  color: inherit; /* 부모 요소의 색상 상속 */
  cursor: pointer; /* 마우스 포인터 변경 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.article-card:hover {
  transform: translateY(-5px); /* hover 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* hover 시 그림자 */
  background-color: #f9f9f9; /* hover 시 배경색 변경 */
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 0 10px;
}

.article-info {
  font-size: 1rem;
  margin: 0;
}
</style>

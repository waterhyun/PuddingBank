<template>
  <div>
    <h1>게시글 생성</h1>
    <form @submit.prevent="create">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"> </textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useArticleStore } from '../../stores/article';
const title = ref(null)
const content = ref(null)
const store = useArticleStore()

const create = function() {
  store.createArticle(title.value, content.value)
}
</script>

<style scoped>

</style>
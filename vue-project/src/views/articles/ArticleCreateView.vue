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
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const title = ref('')
const content = ref('')
const router = useRouter()

const create = async function() {
  try {
    const token = localStorage.getItem('token')
    await axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      data: {
        title: title.value,
        content: content.value
      },
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    // 게시글 생성 성공 시 게시판 페이지로 이동
    router.push({ name: 'Articles' })
  } catch (error) {
    console.error('Error:', error)
    if (error.response && error.response.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'Login' })
    } else {
      alert('게시글 작성에 실패했습니다.')
    }
  }
}
</script>

<style scoped>
</style>
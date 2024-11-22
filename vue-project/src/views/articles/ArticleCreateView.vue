<template>
  <div class="create-article-page">
    <h1 class="title">게시글 생성</h1>
    <form @submit.prevent="create" class="form-container">
      
      <!-- 카테고리 선택 -->
      <div class="form-group">
        <label for="category">카테고리 :</label>
        <select id="category" v-model="category" class="form-select">
          <option disabled value="">카테고리를 선택하세요</option>
          <option value="NOTICE">공지</option>
          <option value="FREE">자유</option>
          <option value="QUESTION">질문</option>
          <option value="RECOMMEND">추천</option>
        </select>
      </div>
      
      <!-- 제목 입력 -->
      <div class="form-group">
        <label for="title">제목 :</label>
        <input type="text" id="title" v-model.trim="title" class="form-input">
      </div>

      <!-- 내용 입력 -->
      <div class="form-group">
        <label for="content">내용 :</label>
        <textarea id="content" v-model.trim="content" class="form-textarea"></textarea>
      </div>

       <!-- 버튼 컨테이너 -->
       <div class="button-container">
        <input type="submit" value="게시글 생성" class="submit-button">
        <RouterLink to="/articles/" class="back-button">목록으로 돌아가기</RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const title = ref('')
const content = ref('')
const category = ref('')
const router = useRouter()

const create = async function() {
  try {
    const token = localStorage.getItem('token')
    await axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      data: {
        title: title.value,
        content: content.value,
        category: category.value
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

/* 페이지 전체 컨테이너 */
.create-article-page {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px; /* 내부 여백 추가 */
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* 폼 컨테이너 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 필드 간격 */
}

/* 각 입력 필드 그룹 */
.form-group {
  display: flex;
  flex-direction: column;
}

/* 레이블 스타일 */
label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

/* 공통 입력 필드 스타일 */
.form-input,
.form-textarea,
.form-select {
  width: calc(100% - 20px); /* 양쪽 여백 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 10px;
  font-size: 14px;
  color: #555;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  outline: none;
  transition: border-color 0.3s ease;
}

/* 포커스 시 효과 */
.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  border-color: #007bff;
}

/* 텍스트 영역 */
.form-textarea {
  resize: none;
  height: 100px;
}

/* 버튼 컨테이너 */
.button-container {
  display: flex; /* 버튼 나란히 배치 */
  justify-content: space-between; /* 양옆 정렬 */
  gap: 10px; /* 버튼 간격 */
  margin-top: 20px;
}

/* 공통 버튼 스타일 */
button,
.submit-button,
.back-button {
  flex: 1; /* 버튼 크기 균등 */
  padding: 12px;
  font-size: 16px;
  color: white;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* 게시글 생성 버튼 스타일 */
.submit-button {
  background-color: #007bff;
}

.submit-button:hover {
  background-color: #0056b3;
}

.submit-button:active {
  background-color: #004494;
}

/* 뒤로가기 버튼 스타일 */
.back-button {
  background-color: #6c757d;
}

.back-button:hover {
  background-color: #5a6268;
}

.back-button:active {
  background-color: #4e555b;
}
</style>

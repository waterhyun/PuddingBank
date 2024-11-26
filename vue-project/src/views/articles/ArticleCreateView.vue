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
    const token = sessionStorage.getItem('token')
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

<template>
  <div class="create-article-page">
    <h1 class="page-title">게시글 작성</h1>
    <form @submit.prevent="create" class="form-container">
      
      <!-- 카테고리 선택 -->
      <div class="form-group">
        <label for="category">카테고리</label>
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
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title" 
          v-model.trim="title" 
          class="form-input"
          placeholder="제목을 입력하세요"
        >
      </div>

      <!-- 내용 입력 -->
      <div class="form-group">
        <label for="content">내용</label>
        <textarea 
          id="content" 
          v-model.trim="content" 
          class="form-textarea"
          placeholder="내용을 입력하세요"
          rows="10"
        ></textarea>
      </div>

      <!-- 버튼 영역 -->
      <div class="button-group">
        <RouterLink to="/articles/" class="btn cancel-btn">취소</RouterLink>
        <button type="submit" class="btn submit-btn">작성완료</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-article-page {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: #FFFEFB;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.page-title {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid #FDE49B;
  border-radius: 12px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-family: 'jjinbbangM';
  color: #73553C;
  margin-bottom: 0.5rem;
}

.form-select,
.form-input,
.form-textarea {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  background: #FFFEFB;
  transition: all 0.2s ease;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2373553C' d='M6 8.825L1.175 4 2.238 2.938 6 6.7l3.763-3.762L10.825 4z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
}

.form-textarea {
  resize: vertical;
  min-height: 200px;
}

.form-select:focus,
.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #73553C;
  box-shadow: 0 0 0 3px rgba(115, 85, 60, 0.1);
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px;
  font-family: 'jjinbbangM';
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.submit-btn {
  background: #FDE49B;
  color: #73553C;
}

.cancel-btn {
  background: #73553C;
  color: #FFFEFB;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
}

@media (max-width: 768px) {
  .create-article-page {
    margin: 1rem;
    padding: 1rem;
  }

  .form-container {
    padding: 1rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>

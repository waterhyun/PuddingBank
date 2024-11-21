<template>
  <div class="article-container">
    <div v-if="store.article">
      <div class="article-detail">
        <h1 class="article-id">{{ id }}번 게시글 상세페이지</h1>

        <!-- 게시글 수정 모드 -->
        <div v-if="editMode === 'article'" class="edit-form">
          <input 
            type="text" 
            v-model="editTitle" 
            class="edit-input" 
            placeholder="제목 수정"
          />
          <textarea 
            v-model="editContent" 
            class="edit-input" 
            placeholder="내용 수정"
          ></textarea>
          <div class="button-group">
            <button @click="handleUpdateArticle" class="save-button">저장</button>
            <button @click="cancelEditArticle" class="cancel-button">취소</button>
          </div>
        </div>

        <!-- 게시글 표시 모드 -->
        <div v-else>
          <h3 class="article-title">제목: {{ store.article.title }}</h3>
          <p class="article-content">내용: {{ store.article.content }}</p>
          <!-- 작성자 본인만 수정/삭제 버튼 보이도록 -->
          <div v-if="authStore.user && store.article.user === authStore.user.id" class="button-group">
            <button @click="startEditArticle" class="edit-button">수정</button>
            <button @click="handleDeleteArticle" class="delete-button">삭제</button>
          </div>
        </div>

        <div class="detail-meta">
          <span class="detail-author">작성자: {{ store.article.username }}</span>
          <span class="detail-date">작성일: {{ store.article.created_at }}</span>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comment-section">
        <h3>댓글</h3>
        <!-- 로그인한 사용자만 댓글 작성 가능하도록 -->
        <div v-if="authStore.user" class="comment-form">
          <input 
            type="text" 
            v-model="commentContent" 
            class="comment-input" 
            placeholder="댓글을 입력하세요..."
          />
          <button 
            @click="handleSubmitComment" 
            class="comment-button" 
            :disabled="!commentContent.trim()"
          >
            댓글 추가
          </button>
        </div>
        <div v-else class="login-message">
          <p>댓글을 작성하려면 로그인이 필요합니다.</p>
        </div>

        <ul class="comment-list">
          <li v-for="comment in store.comments" :key="comment.id" class="comment-item">
            <p class="comment-author">유저: {{ comment.username }}</p>
            <p class="comment-date">작성일: {{ comment.created_at }}</p>

            <!-- 댓글 수정 모드 -->
            <div v-if="editMode === comment.id" class="edit-form">
              <input type="text" v-model="editContent" class="edit-input" />
              <div class="button-group">
                <button @click="handleUpdateComment(comment.id, editContent)" class="save-button">저장</button>
                <button @click="cancelEdit" class="cancel-button">취소</button>
              </div>
            </div>

            <!-- 댓글 표시 모드 -->
            <div v-else>
              <p class="comment-content">{{ comment.content }}</p>
              <!-- 댓글 작성자 본인만 수정/삭제 버튼 보이도록 -->
              <div v-if="authStore.user && comment.user === authStore.user.id" class="button-group">
                <button @click="startEdit(comment)" class="edit-button">수정</button>
                <button @click="handleDeleteComment(comment.id)" class="delete-button">삭제</button>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <RouterLink to="/articles/" class="back-button">목록으로 돌아가기</RouterLink>
    </div>
    <div v-else>
      <p>게시글 데이터를 불러오는 중입니다...</p>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const store = useArticleStore()
const authStore = useAuthStore()

const commentContent = ref('')
const editMode = ref(null)
const editTitle = ref('')
const editContent = ref('')

onMounted(() => {
  store.getArticle(id)
})

// 게시글 수정 관련
const startEditArticle = () => {
  editMode.value = 'article'
  editTitle.value = store.article.title
  editContent.value = store.article.content
}

const handleUpdateArticle = async () => {
  if (editTitle.value.trim() === '' || editContent.value.trim() === '') return
  
  const token = localStorage.getItem('token')
  try {
    await axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/articles/${id}/`,
      data: {
        title: editTitle.value,
        content: editContent.value,
      },
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    editMode.value = null
    store.getArticle(id)
  } catch (error) {
    console.error('Error:', error)
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'Login' })
    } else {
      alert('게시글 수정에 실패했습니다.')
    }
  }
}


// 게시글 삭제
const handleDeleteArticle = async () => {
  if (!authStore.user) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!confirm('정말 삭제하시겠습니까?')) return
  
  const token = localStorage.getItem('token')
  try {
    await axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/articles/${id}/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    router.push({ name: 'Articles' })
  } catch (error) {
    if (error.response?.status === 403) {
      alert('삭제 권한이 없습니다.')
    } else {
      alert('게시글 삭제에 실패했습니다.')
    }
  }
}



const cancelEditArticle = () => {
  editMode.value = null
  editTitle.value = ''
  editContent.value = ''
}

// 댓글 관련
const handleSubmitComment = async () => {
  if (!commentContent.value.trim()) return
  
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'Login' })
    return
  }

  try {
    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/articles/${id}/comments/`,
      data: {
        content: commentContent.value
      },
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    commentContent.value = ''
    store.getArticle(id)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'Login' })
    } else {
      alert('댓글 작성에 실패했습니다.')
    }
  }
}

const startEdit = (comment) => {
  editMode.value = comment.id
  editContent.value = comment.content
}

const cancelEdit = () => {
  editMode.value = null
  editContent.value = ''
}

const handleUpdateComment = async (commentId, content) => {
  if (!content.trim()) return
  
  const token = localStorage.getItem('token')
  try {
    await axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/articles/comments/${commentId}/`,
      data: { content },
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    cancelEdit()
    store.getArticle(id)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('권한이 없습니다.')
    } else {
      alert('댓글 수정에 실패했습니다.')
    }
  }
}

const handleDeleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  
  const token = localStorage.getItem('token')
  try {
    await axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/articles/comments/${commentId}/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    store.getArticle(id)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('권한이 없습니다.')
    } else {
      alert('댓글 삭제에 실패했습니다.')
    }
  }
}
</script>


<style scoped>
.article-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-detail {
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

.article-id {
  font-size: 1.8em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.article-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 15px;
}

.article-content {
  font-size: 1.2em;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #555;
}

.detail-meta {
  font-size: 0.9em;
  color: #7f8c8d;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.comment-section {
  background-color: #f4f4f4;
  border-radius: 10px;
  padding: 20px;
  margin-top: 30px;
}

.comment-list {
  list-style-type: none;
  padding: 0;
}

.comment-item {
  background-color: white;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.comment-author {
  font-weight: bold;
  color: #34495e;
  margin-bottom: 5px;
}

.comment-form {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.edit-form {
  margin-top: 10px;
}

.edit-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.save-button {
  background-color: #2ecc71;
  color: white;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
}

.edit-button {
  background-color: #3498db;
  color: white;
}

.delete-button {
  background-color: #e74c3c;
  color: white;
  margin-left: 10px;
}

.back-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #95a5a6;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 20px;
}

button:hover {
  opacity: 0.9;
}

.comment-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.comment-button {
  background-color: #3498db;
  color: white;
}

.comment-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
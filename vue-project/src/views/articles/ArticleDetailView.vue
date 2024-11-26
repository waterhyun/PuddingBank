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

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 게시글 수정 관련
const startEditArticle = () => {
  editMode.value = 'article'
  editTitle.value = store.article.title
  editContent.value = store.article.content
}

const handleUpdateArticle = async () => {
  if (editTitle.value.trim() === '' || editContent.value.trim() === '') return
  
  const token = sessionStorage.getItem('token')
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
  
  const token = sessionStorage.getItem('token')
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
  
  const token = sessionStorage.getItem('token')
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

// const handleUpdateComment = async (commentId) => {
//   if (!content.trim()) return
  
//   const token = localStorage.getItem('token')
//   try {
//     await axios({
//       method: 'put',
//       url: `http://127.0.0.1:8000/api/v1/articles/comments/${commentId}/`,
//       data: { content },
//       headers: {
//         'Authorization': `Token ${token}`
//       }
//     })
    
//     cancelEdit()
//     store.getArticle(id)
//   } catch (error) {
//     if (error.response?.status === 401) {
//       alert('권한이 없습니다.')
//     } else {
//       alert('댓글 수정에 실패했습니다.')
//     }
//   }
// }

const handleUpdateComment = async (commentId) => {
  if (!editContent.value.trim()) return
  
  const token = sessionStorage.getItem('token')
  try {
    await axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/articles/comments/${commentId}/`,
      data: {
        content: editContent.value
      },
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    editMode.value = null
    editContent.value = ''
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
  
  const token = sessionStorage.getItem('token')
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

const handleLike = async () => {
  if (!authStore.user) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'Login' })
    return
  }

  const token = sessionStorage.getItem('token')
  try {
    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/articles/${id}/like/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    store.getArticle(id)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'Login' })
    } else {
      alert('좋아요 처리에 실패했습니다.')
    }
  }
}
</script>

<template>
  <div class="article-container">
    <div v-if="store.article" class="article-detail">
      <!-- 수정 모드가 아닐 때 -->
      <div v-if="editMode !== 'article'">
        <div class="article-header">
          <div class="article-main-info">
            <div class="article-info">
              <span class="article-category">{{ store.article.category_display }}</span>
              <span class="separator">|</span>
              <span class="author">{{ store.article.username }}</span>
              <span class="separator">|</span>
              <span class="date">{{ formatDate(store.article.created_at) }}</span>
            </div>
            <div v-if="authStore.user && store.article.user === authStore.user.id" class="button-group">
              <button @click="startEditArticle" class="btn edit-btn">수정</button>
              <button @click="handleDeleteArticle" class="btn delete-btn">삭제</button>
            </div>
          </div>
          <h2 class="article-title">{{ store.article.title }}</h2>
        </div>
        <div class="article-content">{{ store.article.content }}</div>
      </div>

      <!-- 수정 모드일 때 -->
      <div v-else class="edit-form">
        <div class="edit-label">제목</div>
        <input 
          v-model="editTitle" 
          class="edit-title-input" 
          placeholder="제목을 입력하세요" 
        />
        <div class="edit-label">내용</div>
        <textarea 
          v-model="editContent" 
          class="edit-content-input" 
          placeholder="내용을 입력하세요"
        ></textarea>
        <div class="edit-buttons">
          <button @click="handleUpdateArticle" class="btn save-btn">저장</button>
          <button @click="cancelEditArticle" class="btn cancel-btn">취소</button>
        </div>
      </div>

      <!-- 좋아요 섹션 -->
      <div v-show="editMode !== 'article'" class="like-section">
        <button @click="handleLike" class="like-btn" :class="{ 'liked': store.article.is_liked }">
          <i class="fas fa-heart"></i>
          <span>{{ store.article.like_users_count }}</span>
        </button>
      </div>

      <!-- 댓글 섹션 -->
      <div v-show="editMode !== 'article'" class="comment-section">
        <h3>댓글</h3>
        <div v-if="authStore.user" class="comment-form">
          <input 
            type="text" 
            v-model="commentContent" 
            class="comment-input" 
            placeholder="댓글을 입력하세요..."
          />
          <button 
            @click="handleSubmitComment" 
            class="btn comment-btn"
            :disabled="!commentContent.trim()"
          >
            작성
          </button>
        </div>

        <ul class="comment-list">
          <li v-for="comment in store.comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.username }}</span>
              <div class="comment-actions">
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                <div v-if="authStore.user && comment.user === authStore.user.id" class="button-group">
                  <button 
                    v-if="editMode !== comment.id"
                    @click="startEdit(comment)" 
                    class="btn edit-btn"
                  >
                    수정
                  </button>
                  <button 
                    @click="handleDeleteComment(comment.id)" 
                    class="btn delete-btn"
                  >
                    삭제
                  </button>
                </div>
              </div>
            </div>
            <!-- 댓글 수정 모드 -->
            <div v-if="editMode === comment.id" class="edit-comment-form">
              <input 
                v-model="editContent" 
                class="comment-input" 
                :placeholder="comment.content"
              />
              <div class="button-group">
                <button 
                  @click="handleUpdateComment(comment.id)" 
                  class="btn save-btn"
                >
                  저장
                </button>
                <button 
                  @click="cancelEdit" 
                  class="btn cancel-btn"
                >
                  취소
                </button>
              </div>
            </div>
            <!-- 일반 댓글 표시 -->
            <p v-else class="comment-content">{{ comment.content }}</p>
          </li>
        </ul>
      </div>
      
      <!-- 하단 버튼 -->
      <div v-if="editMode !== 'article'">
        <RouterLink to="/articles/" class="btn back-btn">목록으로</RouterLink>
      </div>
      <div v-else>
        <button @click="cancelEditArticle" class="btn back-btn">돌아가기</button>
      </div>
    </div>
    <div v-else class="loading">게시글을 불러오는 중입니다...</div>
  </div>
</template>

<style scoped>
.article-container {
  max-width: 1400px;
  margin: 24px auto;
  padding: 32px;
  background-color: #fffefb;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(115, 85, 60, 0.12);
}

.article-detail {
  padding: 32px;
  background: #FFFEFB;
  border-radius: 16px;
  border: 3px solid #FDE49B;
}

.article-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #FDE49B;
}

.article-main-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.article-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #73553C;
  font-family: 'GowunDodum-Regular';
}

.article-category {
  background: #FEF0AC;
  padding: 4px 12px;
  border-radius: 16px;
  font-weight: bold;
}

.separator {
  color: #FDE49B;
}

.article-title {
  font-family: 'JalnanFont';
  color: #73553C;
  font-size: 24px;
  margin-bottom: 16px;
  margin-left: 2px;
}

.article-content {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  line-height: 1.6;
  margin-bottom: 32px;
  white-space: pre-wrap;
  margin-left: 3px;
  min-height: 150px;
}

/* 버튼 스타일 */
.button-group {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'GowunDodum-Regular';
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
}

.edit-btn {
  background: #FDE49B;
  color: #73553C;
}

.delete-btn {
  background: #73553C;
  color: #FFFEFB;
  padding: 4px 8px;
  font-size: 14px;
}

.save-btn {
  background: #FDE49B;
  color: #73553C;
}

.cancel-btn {
  background: #73553C;
  color: #FFFEFB;
}

/* 수정 폼 스타일 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 24px;
  background: #FFFEFB;
  border-radius: 12px;
}

.edit-label {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-weight: bold;
  font-size: 1.1rem;
  margin-left: 3px;
}

.edit-title-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-size: 18px;
  color: #73553C;
  font-family: 'JalnanFont';
}

.edit-content-input {
  width: 100%;
  min-height: 300px;
  padding: 16px;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-size: 16px;
  color: #73553C;
  font-family: 'GowunDodum-Regular';
  resize: vertical;
}

.edit-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

/* 좋아요 섹션 */
.like-section {
  display: flex;
  justify-content: center;
  margin: 32px 0;
}

.like-btn {
  background: #FFFEFB;
  border: 2px solid #FDE49B;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #73553C;
}

.like-btn.liked {
  background: #FDE49B;
}

.like-btn i {
  margin-right: 8px;
}

/* 댓글 섹션 */
.comment-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 2px solid #FDE49B;
}

.comment-section h3 {
  font-family: 'JalnanFont';
  color: #73553C;
  margin-bottom: 16px;
}

.comment-form {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.comment-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
}

.comment-btn {
  background: #FDE49B;
  color: #73553C;
}

.comment-list {
  list-style: none;
  padding: 0;
}

.comment-item {
  padding: 16px;
  border-bottom: 1px solid #FDE49B;
  background: #FFFEFB;
  border-radius: 8px;
  margin-bottom: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-author {
  font-weight: bold;
  color: #73553C;
}

.comment-date {
  color: #73553C;
  opacity: 0.7;
  font-size: 0.8rem;
}

.comment-content {
  color: #73553C;
  line-height: 1.4;
  margin-top: 8px;
  margin-bottom: 0;
}

.edit-comment-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

/* 기타 */
.back-btn {
  display: inline-block;
  margin-top: 32px;
  text-decoration: none;
  background: #73553C;
  color: #FFFEFB;
}

.loading {
  text-align: center;
  padding: 32px;
  color: #73553C;
  font-family: 'GowunDodum-Regular';
}

@media (max-width: 768px) {
  .article-container {
    margin: 16px;
    padding: 16px;
  }

  .article-detail {
    padding: 16px;
  }

  .comment-form {
    flex-direction: column;
  }

  .comment-btn {
    width: 100%;
  }
}
</style>

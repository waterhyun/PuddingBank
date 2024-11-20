<template>
  <div class="article-container">
    <!-- 게시글 섹션 -->
    <div class="article-detail">
      <h1 class="article-id">{{ id }}번 게시글 상세페이지</h1>
      <h3 class="article-title">제목: {{ store.article.title }}</h3>
      <p class="article-content">내용: {{ store.article.content }}</p>
      <div class="detail-meta">
        <span class="detail-author">작성자: {{ store.article.username }}</span>
        <span class="detail-date">작성일: {{ store.article.created_at }}</span>
      </div>
    </div>
    
    <!-- 댓글 섹션 -->
    <div class="comment-section">
      <h3>댓글</h3>

      <ul class="comment-list">
        <li v-for="comment in store.comments" :key="comment.id" class="comment-item">
          <p class="comment-author">유저 : {{ comment.username }}</p>
          <p>수정일 : {{ comment.updated_at }}</p>
          
          <!-- 수정 중이면 텍스트박스를 보여줌 -->
          <div v-if="editMode === comment.id" class="edit-form">
            <input 
              type="text"
              v-model="editContent"
              class="edit-input"
            />
            <button @click="updateComment(comment.id, editContent)" class="save-button">저장</button>
            <button @click="cancelEdit" class="cancel-button">취소</button>
          </div>

          <div v-else>
            <p class="comment-content">{{ comment.content }}</p>
            <button @click="startEdit(comment)" class="edit-button">수정</button>
            <button @click="deleteComment(comment.id)" class="delete-button">삭제</button>
          </div>
        </li>
      </ul>

      <!-- 댓글입력창 -->
      <div class="comment-form">
        <input
          type="text"
          v-model="newComment"
          class="comment-input"
          placeholder="댓글을 입력하세요..."
        />
        <button @click="addComment" class="comment-button">댓글 추가</button>
      </div>
    </div>

    <!-- 목록으로 돌아가기 -->
    <RouterLink to="/articles/" class="back-button">목록으로 돌아가기</RouterLink>
  </div>
</template>



<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { useArticleStore } from '@/stores/articles';

///////////////게시글
// useRoute를 사용하여 params에서 id가져오기
const route = useRoute();
const id = route.params.id; // 전달받은 id

const store = useArticleStore()
onMounted(() => {
  store.getArticle(id)
})

// 댓글 수정 시작
const startEdit = (comment) => {
  editMode.value = comment.id; // 수정 중인 댓글 ID 설정
  editContent.value = comment.content; // 기존 댓글 내용 초기화
};

// 댓글 수정 취소
const cancelEdit = () => {
  editMode.value = null; // 수정 모드 종료
  editContent.value = ''; // 수정 내용 초기화
};

// 댓글 수정 저장
const updateComment = (comment_id, editContent) => {
  if (editContent.value.trim() === '') return; // 빈 내용 방지
  const updatedData = { content: editContent.value }; // 수정된 데이터 생성
  store.updateComment(comment_id, updatedData); // 스토어 호출
  cancelEdit(); // 수정 모드 종료
};


</script>

<style scoped>
/* 전체 컨테이너 */
.article-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

/* 게시글 섹션 스타일 */
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
  margin-bottom: 10px;
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
  margin-bottom: 20px;
}

/* 댓글 섹션 스타일 */
.comment-section {
  background-color: #f4f4f4;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.comment-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

.comment-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.comment-author {
  font-weight: bold;
  color: #34495e;
  margin-bottom: 5px;
}

.comment-content {
  font-size: 1em;
  color: #555;
}

.comment-form {
  display: flex;
  gap: 10px;
}

.comment-input {
  flex: 1;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.comment-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.comment-button:hover {
  background-color: #2980b9;
}

/* 목록으로 돌아가기 버튼 */
.back-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  text-align: center;
  font-size: 1em;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #2980b9;
}
</style>

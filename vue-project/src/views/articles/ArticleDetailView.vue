<template>
  <div class="article-container">
    <!-- 게시글 섹션 -->
    <div v-if="store.article">
      <div class="article-detail">
        <h1 class="article-id">{{ id }}번 게시글 상세페이지</h1>
        
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
          <button @click="updateArticle" class="save-button">저장</button>
          <button @click="cancelEditArticle" class="cancel-button">취소</button>
        </div>
        
        <div v-else>
          <h3 class="article-title">제목: {{ store.article.title }}</h3>
          <p class="article-content">내용: {{ store.article.content }}</p>
          <button @click="startEditArticle" class="edit-button">수정</button>
          <button @click="store.deleteArticle(id)" class="delete-button">삭제</button>
        </div>
        
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
              <button @click="store.deleteComment(comment.id)" class="delete-button">삭제</button>
            </div>
          </li>
        </ul>

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

      <RouterLink to="/articles/" class="back-button">목록으로 돌아가기</RouterLink>
    </div>
    <div v-else>
    <p>게시글 데이터를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { useArticleStore } from '@/stores/article';

// 게시글 관련 상태 및 로직
const route = useRoute();
const id = route.params.id; // 전달받은 id
const store = useArticleStore();
const newComment = ref(''); // 댓글 입력 내용
const editMode = ref(null); // 수정 모드: 'article' 또는 댓글 ID
const editTitle = ref(''); // 게시글 제목 수정
const editContent = ref(''); // 게시글 및 댓글 내용 수정

// 게시글 데이터 가져오기
onMounted(() => {
  store.getArticle(id);
});

// 게시글 수정 시작
const startEditArticle = () => {
  editMode.value = 'article'; // 게시글 수정 모드
  editTitle.value = store.article.title; // 기존 제목 설정
  editContent.value = store.article.content; // 기존 내용 설정
};

// 게시글 수정 저장
const updateArticle = async () => {
  if (editTitle.value.trim() === '' || editContent.value.trim() === '') return; // 빈 값 방지
  try {
    await store.updateArticle(id, {
      title: editTitle.value,
      content: editContent.value,
    });
    editMode.value = null; // 수정 모드 종료
  } catch (error) {
    console.error('게시글 수정 중 에러:', error);
  }
};

// 게시글 수정 취소
const cancelEditArticle = () => {
  editMode.value = null; // 수정 모드 종료
  editTitle.value = ''; // 제목 초기화
  editContent.value = ''; // 내용 초기화
};

// 댓글 추가 함수
const addComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return
  }
  store.addComment(id, newComment.value) // 댓글 추가 요청
  newComment.value = '';
}

// 댓글 수정 시작
const startEdit = (comment) => {
  editMode.value = comment.id; // 수정 중인 댓글 ID 설정
  editContent.value = comment.content; // 기존 댓글 내용 설정
};

// 댓글 수정 취소
const cancelEdit = () => {
  editMode.value = null; // 수정 모드 종료
  editContent.value = ''; // 수정 내용 초기화
};

// 댓글 수정 저장
const updateComment = (comment_id, editContent) => {
  if (editContent.trim() === '') return; // 빈 내용 방지
  const updatedData = { content: editContent }; // 수정된 데이터 생성
  store.updateComment(comment_id, updatedData); // 스토어 호출
  cancelEdit(); // 수정 모드 종료
};
</script>


<style scoped>
/* 전체 폼 컨테이너 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
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

/* 제목 입력 */
.edit-input {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.edit-input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

/* 버튼 그룹 */
button {
  padding: 10px 20px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button {
  background-color: #2ecc71;
  color: white;
}

.save-button:hover {
  background-color: #27ae60;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
  margin-left: 10px;
}

.cancel-button:hover {
  background-color: #c0392b;
}
</style>

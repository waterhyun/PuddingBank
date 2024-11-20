import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const article = ref([])
  const comments = ref([])
  const router = useRouter()

  // 전체 게시글 조회
  const getArticles = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/articles/'
    })
    .then(res => {
      // console.log(res.data)
      articles.value = res.data
    })
  }

  // 게시글 추가
  const createArticle = function (title, content) {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      data:{
        title, content
      }
    })
    .then(res => {
      router.push({name:'articles'})
    })
  }

  // 단일 게시글 + 댓글 조회
  const getArticle = function(article_id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/articles/detail/${article_id}/`,
    }).then(res => {
      article.value = res.data;
      comments.value = res.data.comments;
    })
  }

  // 단일 게시글 수정
  const updateArticle = function(article_id, updatedData) {
    axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/articles/detail/${article_id}/`,
      data: updatedData, // 수정된 데이터
    })
    .then(res => {
      article.value = res.data; // 수정된 게시글 데이터 저장
      console.log('Article updated successfully:', res.data);
    })
    .catch(error => {
      console.error('Error updating article:', error);
    });
  };
  
  // 게시글 삭제
  const deleteArticle = function(article_id) {
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/articles/detail/${article_id}/`,
    })
    .then(() => {
      article.value = null; // 삭제 후 게시글 상태 초기화
      comments.value = []; // 댓글 상태 초기화
      console.log(`Article with ID ${article_id} deleted successfully.`);
    })
    .catch(error => {
      console.error('Error deleting article:', error);
    });
  };


  // 댓글 수정
  const updateComment = function(comment_id, updatedData) {
    axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/comments/${comment_id}/`,
      data: updatedData, // 수정된 데이터
    })
    .then(res => {
      const updatedComment = res.data;
      comments.value = comments.value.map(comment =>
        comment.id === updatedComment.id ? updatedComment : comment
      );
      console.log('Comment updated successfully:', updatedComment);
    })
    .catch(error => {
      console.error('Error updating comment:', error);
    });
  };

  // 댓글 삭제
  const deleteComment = function(comment_id) {
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/comments/${comment_id}/`,
    })
    .then(() => {
      comments.value = comments.value.filter(comment => comment.id !== comment_id);
      console.log(`Comment with ID ${comment_id} deleted successfully.`);
    })
    .catch(error => {
      console.error('Error deleting comment:', error);
    });
  };

  // 댓글 추가
  const addComment = function(article_id, content) {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/articles/${article_id}/comments/`,
      data: {
        content,
      },
    })
    .then(res => {
      comments.value.push(res.data);
    })
    .catch(error => {
      console.error('Error adding comment:', error);
    });
  };


  return { articles, article, comments,
    getArticles, getArticle, createArticle, 
    updateArticle, deleteArticle, updateComment, deleteComment, addComment
   }
})
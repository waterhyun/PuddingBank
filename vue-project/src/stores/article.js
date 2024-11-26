import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const article = ref(null)
  const comments = ref([])
  const myArticles = ref([])
  const myComments = ref([])
  const router = useRouter()
  const authStore = useAuthStore()

  // 전체 게시글 조회
  const getArticles = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then(res => {
      articles.value = res.data
      // 현재 로그인한 사용자의 글만 필터링
      myArticles.value = res.data.filter(
        article => article.username === authStore.user?.username
      )
    })
    .catch(error => {
      console.error('Error fetching articles:', error)
    })
  }

  // 단일 게시글 + 댓글 조회
  const getArticle = function(article_id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/articles/${article_id}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then(res => {
      article.value = res.data
      comments.value = res.data.comments
    })
    .catch(error => {
      console.error('Error fetching article:', error)
    })
  }

  // 내가 쓴 댓글 조회
  const getMyComments = function (userId) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/articles/my_comments/${userId}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then(res => {
      myComments.value = res.data
    })
    .catch(error => {
      console.error('Error fetching my comments:', error)
    })
  }

  return { 
    articles,
    article,
    comments,
    myArticles,
    myComments,
    getArticles, 
    getArticle,
    getMyComments
  }
})

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
    const headers = authStore.token 
      ? { Authorization: `Token ${authStore.token}` }
      : {}
      
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      headers
    })
    .then(res => {
      articles.value = res.data
      if (authStore.isAuthenticated) {
        myArticles.value = res.data.filter(
          article => article.username === authStore.user?.username
        )
      }
    })
    .catch(error => {
      console.error('Error fetching articles:', error)
    })
  }

  // 공지사항만 조회
  const getAnnouncements = function () {
    const headers = authStore.token 
      ? { Authorization: `Token ${authStore.token}` }
      : {}
      
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      headers
    })
    .then(res => {
      const announcements = res.data.filter(
        article => article.category_display === "공지"
      )
      return announcements
    })
    .catch(error => {
      console.error('Error fetching announcements:', error)
      return []
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
    getMyComments,
    getAnnouncements
  }
})
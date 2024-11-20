import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const article = ref([])
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

  // 단일 게시글 + 댓글 조회
  const getArticle = function(article_id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/articles/${article_id}/`,
    }).then(res => {
      article.value = res.data;
      comments.value = res.data.comments;
    })
  }


  return { articles, article, getArticles, getArticle }
})
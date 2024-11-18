import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const router = useRouter()
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

  return { articles, getArticles, createArticle }
})
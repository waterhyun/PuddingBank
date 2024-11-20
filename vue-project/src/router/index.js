import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleView from '../views/articles/ArticleView.vue'
import ArticleCreateView from '@/views/articles/ArticleCreateView.vue'
import ArticleDetailView from '@/views/articles/ArticleDetailView.vue'
import BankSearchView from '@/views/locations/BankSearchView.vue'
import ExchangesView from '@/views/exchanges/ExchangesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    { // 게시글 전체 조회
      path: '/articles/',
      name: 'articles',
      component: ArticleView,
    },
    { // 게시글 생성
      path: '/create',
      name: 'create',
      component: ArticleCreateView
    },
    { //단일 게시글 상세 페이지
      path:'/articledetail/:id',  //:id
      name:'articledetail',
      component: ArticleDetailView,
      props: true
    },
    {
      path: '/banks',
      name: 'BankSearch',
      component: BankSearchView
    },
    { //환율변환 페이지
      path:'/exchanges',
      name: 'exchanges',
      component: ExchangesView,
    }
  ]
  ,
  
})

export default router

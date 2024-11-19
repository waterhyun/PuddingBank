import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleView from '../views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ExchangesView from '@/views/ExchangesView.vue'

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
      component: ArticleDetailView
    },
    { //환율변환 페이지
      path:'/exchanges',
      name: 'exchanges',
      component: ExchangesView,
    }

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ]
  ,
  
})

export default router

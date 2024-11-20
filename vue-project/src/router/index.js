import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleView from '../views/articles/ArticleView.vue'
import ArticleCreateView from '@/views/articles/ArticleCreateView.vue'
import ArticleDetailView from '@/views/articles/ArticleDetailView.vue'
import BankSearchView from '@/views/locations/BankSearchView.vue'
import ExchangesView from '@/views/exchanges/ExchangesView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import ProfileView from '@/views/auth/ProfileView.vue'
import SignUpView from '@/views/auth/SignUpView.vue'
import { useAuthStore } from '@/stores/auth'
import ProductsView from '@/views/products/ProductsView.vue'

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
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: () => import('@/views/auth/SignUpView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/auth/ProfileView.vue'),
      meta: { requiresAuth: true }  // beforeEnter 대신 meta 사용
    },
    {
      path: '/products',
      name: 'Products',
      component: ProductsView
    }
  ] 
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  // 인증이 필요한 페이지에 접근 시
  if (to.meta.requiresAuth && !isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')  // 알림 추가
    next('/login')
  } 
  // 이미 로그인한 사용자가 로그인/회원가입 페이지에 접근 시
  else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } 
  // 그 외의 경우
  else {
    next()
  }
})

export default router

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
// MBTI 관련 컴포넌트 import
import LoanMBTIResultView from '@/views/products/LoanMBTIResultView.vue'
import LoanMBTITestView from '@/views/products/LoanMBTITestView.vue'

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
      name: 'Articles',
      component: ArticleView,
    },
    { // 게시글 생성
      path: '/articlecreate',
      name: 'ArticleCreate',
      component: ArticleCreateView
    },
    { //단일 게시글 상세 페이지
      path:'/articledetail/:id',  //:id
      name:'ArticleDetail',
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
    },
    {
      path: '/loan-test',
      name: 'LoanMBTITest',
      component: LoanMBTITestView
    },
    {
      path: '/loan-result',
      name: 'LoanMBTIResult',
      component: LoanMBTIResultView,
      props: true,  // MBTI 결과와 추천 상품 데이터를 props로 전달
      meta: { requiresTestComplete: true }  // MBTI 검사 완료 필요
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

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // ArticleDetail 페이지로 가려고 할 때
  if (to.name === 'ArticleDetail') {
    // 로그인된 상태라면 접근 허용
    if (authStore.isAuthenticated) {
      next()
    } else {
      // 로그인되지 않은 경우 로그인 페이지로 리다이렉트
      alert('로그인이 필요한 서비스입니다.')
      // next({ name: 'Login' })
    }
  } else {
    next()
  }
})

// MBTI 검사 완료 여부 확인을 위한 네비게이션 가드 추가
router.beforeEach((to, from, next) => {
  if (to.meta.requiresTestComplete && !from.name === 'LoanMBTITest') {
    // MBTI 검사를 거치지 않고 결과 페이지로 직접 접근하는 경우
    next({ name: 'LoanMBTITest' })
  } else {
    next()
  }
})

export default router

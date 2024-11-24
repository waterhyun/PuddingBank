<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

// 클릭 할 때 마다 새로고침이 되도록 함
const handleBankSearch = () => {
  if (router.currentRoute.value.path === '/banks') {
    window.location.reload()
  } else {
    router.push('/banks')
  }
}
</script>


<template>
    <div class="wrapper">
      <nav>
        <div>
          <RouterLink to="/">Home</RouterLink> |
          <RouterLink to="/products">예적금비교</RouterLink> |
          <RouterLink to="/loan-comparison">대출상품비교</RouterLink> | 
          <!-- <RouterLink to="/loan-test">대출상품추천</RouterLink> |  -->
          <RouterLink to="/articles">게시판</RouterLink> |
          <a href="#" @click.prevent="handleBankSearch">은행 찾기</a> |
          <RouterLink to="/exchanges">환율계산기</RouterLink>
        </div>
        <div class="'auth-menu'">
          <!-- 비로그인 상태 -->
          <template v-if="!isAuthenticated">
            <RouterLink to="/login">로그인</RouterLink> |
            <RouterLink to="/signup">회원가입</RouterLink>
          </template>
          <!-- 로그인 상태 -->
          <template v-if="isAuthenticated">
            <RouterLink to="/profile">마이페이지</RouterLink> |
            <button @click="handleLogout" class="logout-btn">로그아웃</button>
          </template>
        </div>
      </nav>

    </div> <RouterView/>
</template>

<style scoped>

</style>

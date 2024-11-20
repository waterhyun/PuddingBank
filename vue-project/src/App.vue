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
</script>


<template>
    <div class="wrapper">
      <nav>
        <div>
          <RouterLink to="/">Home</RouterLink> |
          <RouterLink to="/products">예적금비교</RouterLink> | 
          <RouterLink to="/articles">게시판</RouterLink> |
          <RouterLink to="/banks">은행 찾기</RouterLink> |
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
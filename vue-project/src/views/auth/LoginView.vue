<!-- views/auth/LoginView.vue -->
<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">아이디</label>
        <input 
          type="text" 
          id="username"
          v-model="formData.username"
          required
        >
      </div>
      
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input 
          type="password" 
          id="password"
          v-model="formData.password"
          required
        >
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="button-group">
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '로그인 중...' : '로그인' }}
        </button>
        <router-link to="/signup">회원가입</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const error = ref('')
const isLoading = ref(false)

const formData = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = ''
    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.non_field_errors?.[0] || '로그인에 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}
</script>
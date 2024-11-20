<!-- views/auth/SignUpView.vue -->
<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignup" class="signup-form">
      <div class="form-group">
        <label for="username">아이디 *</label>
        <input 
          type="text" 
          id="username"
          v-model="formData.username"
          required
        >
        <span class="error-message" v-if="errors.username">
          {{ errors.username[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="name">이름 *</label>
        <input 
          type="text" 
          id="name"
          v-model="formData.name"
          required
        >
        <span class="error-message" v-if="errors.name">
          {{ errors.name[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="email">이메일 *</label>
        <input 
          type="email" 
          id="email"
          v-model="formData.email"
          required
        >
        <span class="error-message" v-if="errors.email">
          {{ errors.email[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="password1">비밀번호 *</label>
        <input 
          type="password" 
          id="password1"
          v-model="formData.password1"
          required
        >
        <span class="error-message" v-if="errors.password1">
          {{ errors.password1[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인 *</label>
        <input 
          type="password" 
          id="password2"
          v-model="formData.password2"
          required
        >
        <span class="error-message" v-if="errors.password2">
          {{ errors.password2[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="birthdate">생년월일 *</label>
        <input 
          type="date" 
          id="birthdate"
          v-model="formData.birthdate"
          required
        >
        <span class="error-message" v-if="errors.birthdate">
          {{ errors.birthdate[0] }}
        </span>
      </div>

      <div class="form-group">
        <label for="phone">전화번호 (선택)</label>
        <input 
          type="tel" 
          id="phone"
          v-model="formData.phone"
          placeholder="010-0000-0000"
        >
      </div>

      <div class="button-group">
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '가입 중...' : '가입하기' }}
        </button>
        <router-link to="/login">이미 계정이 있으신가요?</router-link>
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
const errors = ref({})
const isLoading = ref(false)

const formData = ref({
  username: '',
  name: '',
  email: '',
  password1: '',
  password2: '',
  birthdate: '',
  phone: ''
})

const handleSignup = async () => {
  try {
    isLoading.value = true
    errors.value = {}
    await authStore.signup(formData.value)
    alert('회원가입이 완료되었습니다.')
    router.push('/login')
  } catch (err) {
    if (err.response?.data) {
      errors.value = err.response.data
    } else {
      alert('회원가입에 실패했습니다.')
    }
  } finally {
    isLoading.value = false
  }
}
</script>
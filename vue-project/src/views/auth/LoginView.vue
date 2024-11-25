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
    
    // 아이디 입력 여부 체크
    if (!formData.value.username) {
      error.value = '아이디를 입력해주세요.'
      return
    }
    
    // 비밀번호 입력 여부 체크 
    if (!formData.value.password) {
      error.value = '비밀번호를 입력해주세요.'
      return
    }

    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = '존재하지 않는 아이디입니다. 회원가입을 진행해주세요.'
    } else if (err.response?.status === 401) {
      error.value = '아이디 또는 비밀번호가 일치하지 않습니다.'
    } else if (err.response?.status === 400) {
      if (err.response.data?.username) {
        error.value = '아이디를 입력해주세요.'
      } else if (err.response.data?.password) {
        error.value = '비밀번호를 입력해주세요.'
      } else {
        error.value = '입력하신 정보를 다시 확인해주세요.'
      }
    } else if (!navigator.onLine) {
      error.value = '인터넷 연결을 확인해주세요.'
    } else {
      error.value = '서버와의 연결이 원활하지 않습니다. 잠시 후 다시 시도해주세요.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>


<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fffefb;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(115, 85, 60, 0.1);
}

h2 {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem;
}

input {
  padding: 0.8rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #73553C;
  background-color: #FEF0AC;
}

.error-message {
  color: #3D0F0E;
  font-family: 'GowunDodum-Regular';
  font-size: 0.9rem;
  text-align: center;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  margin-top: 1rem;
  width: 100%;
}

button, 
.button-group a {
  display: block;
  width: 100%;
  padding: 0.8rem 0;
  border-radius: 8px;
  font-family: 'jjinbbangB';
  font-size: 1rem;
  text-align: center;
  box-sizing: border-box;
}

button {
  background-color: #73553C;
  color: #fffefb;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-group a {
  background-color: #fffefb;
  color: #73553C;
  border: 2px solid #73553C;
  text-decoration: none;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #3D0F0E;
}

.button-group a:hover {
  background-color: #FEF0AC;
  color: #3D0F0E;
  border-color: #3D0F0E;
}
</style>
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
        <VueDatePicker
          v-model="formData.birthdate"
          :max-date="new Date()"
          auto-apply
          locale="ko"
          :enable-time-picker="false"
          :format="formatDate"
          text-input
          input-class-name="date-picker-input"
          placeholder="생년월일을 선택해주세요"
          :model-type="'yyyy-MM-dd'"
          required
        />
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
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

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
    
    // 날짜 형식 변환
    const signupData = {
      ...formData.value,
      birthdate: formData.value.birthdate ? new Date(formData.value.birthdate).toISOString().split('T')[0] : ''
    }
    
    await authStore.signup(signupData)
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

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}년 ${month}월 ${day}일`
}

</script>


<style scoped>
.signup-container {
  max-width: 500px;
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

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
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
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #73553C;
  background-color: #FEF0AC;
}

input[type="date"] {
  color: #73553C;
  font-family: 'GowunDodum-Regular';
}

input::placeholder {
  color: #bbb;
}

.error-message {
  color: #3D0F0E;
  font-family: 'GowunDodum-Regular';
  font-size: 0.8rem;
  margin-top: -0.2rem;
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

button:disabled {
  background-color: #FDE49B;
  cursor: not-allowed;
}

.button-group a {
  background-color: #fffefb;
  color: #73553C;
  border: 2px solid #73553C;
  text-decoration: none;
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #3D0F0E;
}

.button-group a:hover {
  background-color: #FEF0AC;
  color: #3D0F0E;
  border-color: #3D0F0E;
}

/* 기존 date-picker 스타일을 아래 코드로 교체 */
:deep(.dp__theme_light) {
  --dp-background-color: #fffefb;
  --dp-text-color: #73553C;
  --dp-hover-color: transparent; /* Remove hover background */
  --dp-hover-text-color: #73553C;
  --dp-primary-color: #73553C;
  --dp-primary-text-color: #fffefb;
  --dp-border-color: #FDE49B;
  --dp-menu-border-color: #FDE49B;
  --dp-highlight-color: transparent; /* Remove highlight background */
}

:deep(.date-picker-input) {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  transition: all 0.3s ease;
  background-color: #fffefb;
  color: #73553C;
}

:deep(.date-picker-input:focus) {
  outline: none;
  border-color: #73553C;
  background-color: #FEF0AC;
}

:deep(.dp__main) {
  font-family: 'GowunDodum-Regular';
}

:deep(.dp__active_date) {
  background-color: #73553C !important;
  color: #fffefb !important;
}
</style>
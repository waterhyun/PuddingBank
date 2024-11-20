<template>
  <div class="profile-container">
    <h2>마이 프로필</h2>
    
    <!-- 프로필 보기 모드 -->
    <div v-if="!isEditing" class="profile-info">
      <div class="info-group">
        <label>아이디</label>
        <p>{{ user?.username }}</p>
      </div>
      <div class="info-group">
        <label>이름</label>
        <p>{{ user?.name }}</p>
      </div>
      <div class="info-group">
        <label>이메일</label>
        <p>{{ user?.email }}</p>
      </div>
      <div class="info-group">
        <label>생년월일</label>
        <p>{{ formatDate(user?.birthdate) }}</p>
      </div>
      <div class="info-group">
        <label>전화번호</label>
        <p>{{ user?.phone || '미등록' }}</p>
      </div>
      
      <div class="button-group">
        <button @click="startEdit" class="edit-btn">정보 수정</button>
        <button @click="startPasswordChange" class="password-btn">비밀번호 변경</button>
      </div>
    </div>

    <!-- 프로필 수정 모드 -->
    <form v-else-if="isEditing && !isChangingPassword" @submit.prevent="handleUpdate" class="edit-form">
      <div class="form-group">
        <label for="name">이름 *</label>
        <input 
          type="text" 
          id="name"
          v-model="editForm.name"
          required
        >
        <span class="error-message" v-if="errors.name">{{ errors.name }}</span>
      </div>

      <div class="form-group">
        <label for="email">이메일 *</label>
        <input 
          type="email" 
          id="email"
          v-model="editForm.email"
          required
        >
        <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label for="phone">전화번호</label>
        <input 
          type="tel" 
          id="phone"
          v-model="editForm.phone"
          placeholder="010-0000-0000"
        >
        <span class="error-message" v-if="errors.phone">{{ errors.phone }}</span>
      </div>

      <div class="button-group">
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '저장 중...' : '저장' }}
        </button>
        <button type="button" @click="cancelEdit">취소</button>
      </div>
    </form>

    <!-- 비밀번호 변경 폼 -->
    <form v-else @submit.prevent="handlePasswordChange" class="password-form">
      <div class="form-group">
        <label for="old_password">현재 비밀번호 *</label>
        <input 
          type="password" 
          id="old_password"
          v-model="passwordForm.old_password"
          required
        >
        <span class="error-message" v-if="errors.old_password">
          {{ errors.old_password }}
        </span>
      </div>

      <div class="form-group">
        <label for="new_password1">새 비밀번호 *</label>
        <input 
          type="password" 
          id="new_password1"
          v-model="passwordForm.new_password1"
          required
        >
        <span class="error-message" v-if="errors.new_password1">
          {{ errors.new_password1 }}
        </span>
      </div>

      <div class="form-group">
        <label for="new_password2">새 비밀번호 확인 *</label>
        <input 
          type="password" 
          id="new_password2"
          v-model="passwordForm.new_password2"
          required
        >
        <span class="error-message" v-if="errors.new_password2">
          {{ errors.new_password2 }}
        </span>
      </div>

      <div class="button-group">
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '변경 중...' : '비밀번호 변경' }}
        </button>
        <button type="button" @click="cancelPasswordChange">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const isEditing = ref(false)
const isChangingPassword = ref(false)
const isLoading = ref(false)
const errors = ref({})

const editForm = ref({
  name: '',
  email: '',
  phone: ''
})

const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

// 수정 모드 시작
const startEdit = () => {
  editForm.value = {
    name: user.value?.name || '',
    email: user.value?.email || '',
    phone: user.value?.phone || ''
  }
  isEditing.value = true
  isChangingPassword.value = false
  errors.value = {}
}

// 비밀번호 변경 모드 시작
const startPasswordChange = () => {
  passwordForm.value = {
    old_password: '',
    new_password1: '',
    new_password2: ''
  }
  isChangingPassword.value = true
  isEditing.value = true
  errors.value = {}
}

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false
  errors.value = {}
}

// 비밀번호 변경 취소
const cancelPasswordChange = () => {
  isChangingPassword.value = false
  isEditing.value = false
  errors.value = {}
}

// 프로필 업데이트
const handleUpdate = async () => {
  try {
    isLoading.value = true
    errors.value = {}
    await authStore.updateProfile(editForm.value)
    isEditing.value = false
    alert('프로필이 성공적으로 업데이트되었습니다.')
  } catch (error) {
    errors.value = error.response?.data || {}
  } finally {
    isLoading.value = false
  }
}

// 비밀번호 변경
const handlePasswordChange = async () => {
  try {
    isLoading.value = true
    errors.value = {}
    await authStore.changePassword(passwordForm.value)
    isChangingPassword.value = false
    isEditing.value = false
    alert('비밀번호가 성공적으로 변경되었습니다.')
  } catch (error) {
    errors.value = error.response?.data || {}
  } finally {
    isLoading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 컴포넌트 마운트 시 사용자 정보 가져오기
onMounted(async () => {
  if (!user.value) {
    try {
      await authStore.fetchUserDetails()
    } catch (error) {
      console.error('Failed to fetch user details:', error)
    }
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.profile-info, .edit-form, .password-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-group, .form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.error-message {
  color: #ff4444;
  font-size: 0.8em;
  margin-top: 5px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.edit-btn {
  background-color: #42b983;
  color: white;
}

.password-btn {
  background-color: #666;
  color: white;
}

button[type="submit"] {
  background-color: #42b983;
  color: white;
}

button[type="button"] {
  background-color: #666;
  color: white;
}
</style>
<template>
  <div class="profile-container">
    <h2>마이 프로필</h2>
      
    <!-- 프로필 보기 모드 -->
    <div v-if="!isEditing" class="profile-info">
      <div class="profile-row">
        <strong>아이디:</strong>
        <span>{{ user.username }}</span>
      </div>
      <div class="profile-row">
        <strong>이름:</strong>
        <span>{{ user.name }}</span>
      </div>
      <div class="profile-row">
        <strong>이메일:</strong>
        <span>{{ user.email }}</span>
      </div>
      <div class="profile-row">
        <strong>생년월일:</strong>
        <span>{{ user.birthdate }}</span>
      </div>
      <div class="profile-row">
        <strong>전화번호:</strong>
        <span>{{ user.phone || "미등록" }}</span>
      </div>
      <div>
        <label>나의 위시 리스트</label>
          <div v-if="userWishList">
            <div class="wishlist-container">
              <table class="wishlist-table">
                <thead>
                  <tr>
                    <th>번호</th>
                    <th>상품명</th>
                    <th>은행명</th>
                    <th>유형</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in userWishList" :key="item.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.bank }}</td>
                    <td>{{ item.type === 'saving' ? '적금' : '예금' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
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
import axios from 'axios';
const userWishList = ref([])
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const isEditing = ref(false)
const isChangingPassword = ref(false)
const isLoading = ref(false)
const errors = ref({})

const editForm = ref({
  username: '', // 추가
  name: '',
  email: '',
  phone: '',
  birthdate: '' // 필요한 경우 추가
})

const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

// startEdit 수정 (editForm 변경에 따른)
const startEdit = () => {
  editForm.value = {
    username: user.value?.username || '',
    name: user.value?.name || '',
    email: user.value?.email || '',
    phone: user.value?.phone || '',
    birthdate: user.value?.birthdate || ''
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
    await authStore.fetchUserDetails()
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
const get_wish = function () {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/products/wishlist/',
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      userWishList.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
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
  get_wish()
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
h1 {
  text-align: center;
  font-size: 1.8rem;
  color: #333;
  font-weight: bold; /* 제목 강조 */
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd; /* 제목 아래 구분선 추가 */
  padding-bottom: 10px;
}

.wishlist-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 8px; /* 테이블 모서리를 둥글게 */
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
}

.wishlist-table th {
  background-color: #0046b3; /* 헤더 배경색 */
  color: #fff; /* 헤더 글씨 색 */
  padding: 15px; /* 헤더 패딩 조정 */
  text-align: center;
  font-size: 1rem; /* 헤더 글씨 크기 */
}

.wishlist-table td {
  padding: 12px;
  text-align: center;
  font-size: 0.9rem;
  color: #555; /* 본문 글씨 색상 */
  border-bottom: 1px solid #ddd; /* 행 구분선 */
}

.wishlist-table tbody tr:hover {
  background-color: #f9f9f9; /* 행 호버 효과 */
}

.wishlist-table tbody tr:nth-child(even) {
  background-color: #f8f8f8; /* 짝수 행 배경색 */
}
.profile-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.profile-container h1 {
  text-align: center;
  font-size: 1.8rem;
  color: #0046b3;
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
}

.profile-container .profile-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.profile-container .profile-row:last-child {
  border-bottom: none;
}

.profile-container .profile-row strong {
  font-size: 1rem;
  color: #333;
}

.profile-container .profile-row span {
  font-size: 1rem;
  color: #555;
}


</style>

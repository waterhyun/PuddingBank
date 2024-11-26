<template>
  <div class="profile-container">
    <!-- 기본 프로필 뷰 -->
    <div v-if="!isEditing">
      <!-- 프로필 헤더 -->
      <div class="profile-header">
        <div class="profile-info">
          <h2>{{ user.name }}</h2>
          <button @click="startEdit" class="edit-btn">EDIT</button>
        </div>
      </div>

      <!-- 메인 컨텐츠 -->
      <div class="main-content">
        <!-- 탭 메뉴 -->
        <div class="tab-menu">
          <button 
            v-for="tab in tabs" 
            :key="tab.id" 
            :class="['tab-button', { active: currentTab === tab.id }]"
            @click="currentTab = tab.id"
          >
            {{ tab.name }}
          </button>
        </div>

        <!-- 탭 컨텐츠 -->
        <div class="tab-content">
          <!-- 개인정보 탭 -->
          <div v-show="currentTab === 'contact'" class="contact-info">
            <div class="info-row">
              <div class="info-label">EMAIL</div>
              <div class="info-value">{{ user.email }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">MOBILE</div>
              <div class="info-value">{{ user.phone || "미등록" }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">BIRTH</div>
              <div class="info-value">{{ user.birthdate || "미등록" }}</div>
            </div>
          </div>

          <!-- 위시리스트 탭 -->
          <div v-show="currentTab === 'wishlist'" class="wishlist-content">
            <div v-if="userWishList?.length" class="wishlist-items">
              <div 
                v-for="item in userWishList" 
                :key="item.id" 
                class="wishlist-item"
                @click="router.push(`/products/${item.type === 'saving' ? 'saving' : 'deposit'}/${item.id}`)"
                style="cursor: pointer"
              >
                <h4>{{ item.name }}</h4>
                <p>{{ item.bank }}</p>
                <span :class="['type-badge', item.type === 'saving' ? 'saving' : 'deposit']">
                  {{ item.type === 'saving' ? '적금' : '예금' }}
                </span>
              </div>
            </div>
            <div v-else class="empty-content">찜한 상품이 없습니다.</div>
          </div>
          <!-- 내가 쓴 글 탭 -->
          <div v-show="currentTab === 'posts'" class="posts-content">
            <div v-if="myArticles?.length" class="articles-list">
              <div 
                v-for="article in myArticles" 
                :key="article.id" 
                class="article-item"
                @click="router.push(`/articledetail/${article.id}`)"
                style="cursor: pointer"
              >
                <div class="article-header">
                  <span class="article-category">{{ article.category_display }}</span>
                  <span class="separator">|</span>
                  <h4 class="article-title">{{ article.title }}</h4>
                </div>
                <div class="article-meta">
                  <span class="date">{{ formatDate(article.created_at) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-content">작성한 글이 없습니다.</div>
          </div>

          <!-- 내가 쓴 댓글 탭 -->
          <div v-show="currentTab === 'comments'" class="comments-content">
            <div v-if="myComments?.length" class="comments-list">
              <div 
                v-for="comment in myComments" 
                :key="comment.id" 
                class="comment-item"
                @click="router.push(`/articledetail/${comment.article}`)"
                style="cursor: pointer"
              >
                <p class="comment-content">{{ comment.content }}</p>
                <div class="comment-meta">
                  <span class="date">{{ formatDate(comment.created_at) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-content">작성한 댓글이 없습니다.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 프로필 수정 모드 -->
    <div v-else class="edit-container">
      <form v-if="!isChangingPassword" @submit.prevent="handleUpdate" class="edit-form">
        <h3>프로필 수정</h3>
        <div class="input-group">
          <label for="name">이름</label>
          <input type="text" id="name" v-model="editForm.name" required>
          <span class="error-message" v-if="errors.name">{{ errors.name }}</span>
        </div>
        <div class="input-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model="editForm.email" required>
          <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
        </div>
        <div class="input-group">
          <label for="phone">전화번호</label>
          <input type="tel" id="phone" v-model="editForm.phone" placeholder="010-0000-0000">
          <span class="error-message" v-if="errors.phone">{{ errors.phone }}</span>
        </div>
        <div class="form-buttons">
          <button type="submit" class="btn submit-btn" :disabled="isLoading">
            {{ isLoading ? '저장 중...' : '저장하기' }}
          </button>
          <button type="button" class="btn cancel-btn" @click="cancelEdit">취소</button>
          <button type="button" class="btn password-btn" @click="startPasswordChange">
            비밀번호 변경
          </button>
        </div>
      </form>

      <!-- 비밀번호 변경 폼 -->
      <form v-else @submit.prevent="handlePasswordChange" class="password-form">
        <h3>비밀번호 변경</h3>
        <div class="input-group">
          <label for="old_password">현재 비밀번호</label>
          <input type="password" id="old_password" v-model="passwordForm.old_password" required>
          <span class="error-message" v-if="errors.old_password">
            {{ errors.old_password }}
          </span>
        </div>
        <div class="input-group">
          <label for="new_password1">새 비밀번호</label>
          <input type="password" id="new_password1" v-model="passwordForm.new_password1" required>
          <span class="error-message" v-if="errors.new_password1">
            {{ errors.new_password1 }}
          </span>
        </div>
        <div class="input-group">
          <label for="new_password2">새 비밀번호 확인</label>
          <input type="password" id="new_password2" v-model="passwordForm.new_password2" required>
          <span class="error-message" v-if="errors.new_password2">
            {{ errors.new_password2 }}
          </span>
        </div>
        <div class="form-buttons">
          <button type="submit" class="btn submit-btn" :disabled="isLoading">
            {{ isLoading ? '변경 중...' : '변경하기' }}
          </button>
          <button type="button" class="btn cancel-btn" @click="cancelPasswordChange">
            취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useArticleStore } from '@/stores/article'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const userWishList = ref([])
const authStore = useAuthStore()
const articleStore = useArticleStore()
const { user } = storeToRefs(authStore)
const { myArticles, myComments } = storeToRefs(articleStore)

const isEditing = ref(false)
const isChangingPassword = ref(false)
const isLoading = ref(false)
const errors = ref({})
const currentTab = ref('contact')

const tabs = [
  { id: 'contact', name: '개인정보' },
  { id: 'wishlist', name: '찜한 상품' },
  { id: 'posts', name: '내가 쓴 글' },
  { id: 'comments', name: '내가 쓴 댓글' }
]

const editForm = ref({
  username: '',
  name: '',
  email: '',
  phone: '',
  birthdate: ''
})

const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

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

const cancelEdit = () => {
  isEditing.value = false
  errors.value = {}
}

const cancelPasswordChange = () => {
  isChangingPassword.value = false
  isEditing.value = false
  errors.value = {}
}

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

onMounted(async () => {
  if (!user.value) {
    try {
      await authStore.fetchUserDetails()
    } catch (error) {
      console.error('Failed to fetch user details:', error)
    }
  }
  if (authStore.user?.id) {
    articleStore.getArticles()
    articleStore.getMyComments(authStore.user.id)
  }
  get_wish()
})
</script>


<style scoped>
/* 기본 컨테이너 */
.profile-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: #FFFEFB;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 프로필 헤더 */
.profile-header {
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.profile-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.5rem;
}

.profile-info h2 {
  font-family: 'JalnanFont';
  font-size: 2rem;
  color: #73553C;
  margin: 0;
}

.edit-btn {
  padding: 0.5rem 1.5rem;
  background: transparent;
  border: 1px solid #73553C;
  color: #73553C;
  border-radius: 8px;
  font-family: 'jjinbbangM';
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-btn:hover {
  background: #73553C;
  color: #FFFEFB;
}

/* 탭 메뉴 */
.tab-menu {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding: 0 1.5rem;
  border-bottom: 2px solid #FEF0AC;
  margin-bottom: 1rem;
}

.tab-button {
  padding: 0.8rem 1.2rem;
  background: none;
  border: none;
  font-family: 'jjinbbangM';
  font-size: 1rem;
  color: #73553C;
  cursor: pointer;
  position: relative;
  opacity: 0.6;
  transition: all 0.2s ease;
}

.tab-button:hover {
  opacity: 1;
}

.tab-button.active {
  opacity: 1;
  font-weight: bold;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #73553C;
}

/* 컨텐츠 영역 */
.tab-content {
  padding: 1.5rem;
  min-height: 400px;
  max-width: 800px;
  margin: 0 auto;
}

/* 개인정보 탭 */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

.info-row {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #FDE49B;
  border-radius: 12px;
  background: #FFFEFB;
  transition: all 0.2s ease;
}

.info-row:hover {
  border-color: #73553C;
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.1);
}

.info-label {
  width: 100px;
  font-family: 'jjinbbangM';
  color: #73553C;
  font-size: 0.9rem;
  text-transform: uppercase;
  padding-right: 1rem;
  border-right: 1px solid #FDE49B;
}

.info-value {
  flex: 1;
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  padding-left: 1rem;
}

/* 위시리스트 */
.wishlist-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.wishlist-item {
  background: #FEF0AC;
  padding: 1.2rem;
  border-radius: 12px;
  transition: all 0.2s ease;
  border: 1px solid #FDE49B;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.wishlist-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.1);
  border-color: #73553C;
}

.wishlist-item h4 {
  font-family: 'jjinbbangB';
  color: #73553C;
  margin: 0;
  font-size: 1.1rem;
}

.wishlist-item p {
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  margin: 0;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.wishlist-item p::before {
  content: '🏦';
  font-size: 1.2rem;
}

.type-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: #73553C;
  color: #FFFEFB;
  border-radius: 20px;
  font-size: 0.85rem;
  font-family: 'jjinbbangM';
  align-self: flex-start;
}

.type-badge.saving {
  background: #73553C;
}

.type-badge.deposit {
  background: #3D0F0E;
}

.empty-content {
  text-align: center;
  padding: 3rem;
  background: #FEF0AC;
  border-radius: 12px;
  color: #73553C;
  font-family: 'jjinbbangM';
  font-size: 1rem;
}

/* 게시글 & 댓글 리스트 */
.article-item {
  padding: 1.2rem;
  background: #FFFEFB;
  border: 1px solid #FDE49B;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.article-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.5rem;
}

.article-category {
  font-family: 'jjinbbangM';
  color: #73553C;
  font-size: 0.9rem;
  padding: 0.2rem 0.8rem;
  background: #FEF0AC;
  border-radius: 12px;
}

.separator {
  color: #73553C;
  opacity: 0.5;
}

.article-title {
  font-family: 'jjinbbangB';
  color: #73553C;
  margin: 0;
  font-size: 1.1rem;
}

.article-meta {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem;
  opacity: 0.8;
}

.comment-item {
  padding: 1.2rem;
  background: #FFFEFB;
  border: 1px solid #FDE49B;
  border-radius: 12px;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.comment-item:hover {
  border-color: #73553C;
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.1);
}

.comment-content {
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
}

.comment-meta {
  font-family: 'jjinbbangM';
  color: #73553C;
  font-size: 0.85rem;
  opacity: 0.7;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-content {
  text-align: center;
  padding: 3rem;
  background: #FEF0AC;
  border-radius: 12px;
  color: #73553C;
  font-family: 'jjinbbangM';
}

/* 수정 폼 */
.edit-container {
  max-width: 500px;
  margin: 1.5rem auto;
  padding: 1.5rem;
  width: 100%;
}

.edit-form,
.password-form {
  background: #FFFEFB;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #FDE49B;
  width: 100%;
  box-sizing: border-box;
}

.input-group {
  margin-bottom: 1.2rem;
  width: 100%;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #73553C;
  font-family: 'jjinbbangM';
}

.input-group input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.input-group input:focus {
  outline: none;
  border-color: #73553C;
}

/* 버튼 */
.form-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-family: 'jjinbbangB';
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 저장하기/변경하기 버튼 - 주요 액션 */
.submit-btn {
  background: #FDE49B;
  color: #73553C;
}

.submit-btn:hover {
  background: #FFD24C;
}

/* 취소 버튼 - 보조 액션 */
.cancel-btn {
  background: #E5E5E5;
  color: #666666;
}

.cancel-btn:hover {
  background: #D4D4D4;
}

/* 비밀번호 변경 버튼 - 특별 액션 */
.password-btn {
  background: #73553C;
  color: #FFFEFB;
}

.password-btn:hover {
  background: #5D4431;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
}

/* 프로필 수정 */
.edit-form h3 {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 2rem;
}


/* 비밀번호 변경 */
.password-form h3 {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 2rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .profile-container {
    margin: 1rem;
    padding: 1rem;
  }

  .tab-menu {
    gap: 0.8rem;
    padding: 0 0.8rem;
  }

  .form-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>

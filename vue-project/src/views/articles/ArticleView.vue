<template>
  <div>
    <h1>게시글 목록 페이지</h1>
    <div v-if="authStore.isAuthenticated" class="create-button">
      <router-link :to="{ name: 'ArticleCreate' }" class="btn btn-primary">
        게시글 작성
      </router-link>
    </div>
    <div v-else>
      <!-- 로그인하지 않은 사용자에게 알림 -->
      <button @click="redirectToLogin" class="btn btn-secondary">
        게시글 작성
      </button>
    </div>
    <hr>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted  } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'

const articleStore = useArticleStore()
const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  articleStore.getArticles()
})

const redirectToLogin = () => {
  // 로그인 페이지로 리다이렉트
  alert('로그인이 필요한 서비스입니다.')
  router.push({ name: 'Login' })
}
</script>

<style lang="scss" scoped>

</style>
<script setup>
import { ref, onMounted } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { useArticleStore } from "./stores/article";


const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);



const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

// 은행 찾기
const handleBankSearch = () => {
  if (router.currentRoute.value.path === "/banks") {
    window.location.reload();
  } else {
    router.push("/banks");
  }
};

// 메뉴 열림 상태
const menuOpen = ref(false);

// 메뉴 토글 함수
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

</script>

<template>
  <div class="wrapper">
    <nav class="navbar">
      <div class="navbar-left">
        <RouterLink to="/">
          <img
            src="@/assets/puddingbank_logo.jpg"
            alt="PuddingBank Logo"
            class="logo-image"
          />
        </RouterLink>
      </div>
      <button class="hamburger-btn" @click="toggleMenu">
        ☰
      </button>
      <div class="navbar-center" :class="{ open: menuOpen }">
        <RouterLink to="/service">서비스 안내</RouterLink>
        <RouterLink to="/products">예적금 상품 비교</RouterLink>
        <RouterLink to="/loan-comparison">대출 상품 비교</RouterLink>
        <RouterLink to="/articles">게시판</RouterLink>
        <a href="#" @click.prevent="handleBankSearch">은행 찾기</a>
        <RouterLink to="/exchanges">환율계산기</RouterLink>
      </div>
      <div class="navbar-right" :class="{ open: menuOpen }">
        <template v-if="!isAuthenticated">
          <RouterLink to="/login">로그인</RouterLink>
          <RouterLink to="/signup">회원가입</RouterLink>
        </template>
        <template v-if="isAuthenticated">
          <RouterLink to="/profile">마이페이지</RouterLink>
          <button @click="handleLogout" class="logout-btn auth-btn">
            <RouterLink>로그아웃</RouterLink>
          </button>
        </template>
      </div>
    </nav>

    <RouterView />
  </div>
</template>


<style scoped>
@font-face {
  font-family: 'jjinbbangB'; /* Ajjinbbang 폰트 */
  src: url('@/assets/fonts/AjjinbbangB.TTF') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'jjinbbangM'; 
  src: url('@/assets/fonts/AjjinbbangM.TTF') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'JalnanFont'; /* Jalnan2TTF 폰트 */
  src: url('@/assets/fonts/Jalnan2TTF.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'GowunDodum-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

/* 전체 네비게이션 스타일 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #ffffff; /* 푸딩-1 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 20;
}

.navbar-left .logo-image {
  width: 150px;
}

.navbar-center {
  display: flex;
  gap: 50px;
}

.navbar-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.navbar-center a,
.navbar-center RouterLink,
.navbar-right a,
.navbar-right RouterLink {
  font-family: "JalnanFont", sans-serif;
  font-size: 1.3rem;
  color: #3d0f0e; /* 푸딩-5 */
  text-decoration: none;
  transition: color 0.3s ease;
}

.navbar-center a:hover,
.navbar-center RouterLink:hover,
.navbar-right a:hover,
.navbar-right RouterLink:hover {
  color: #73553c; /* 푸딩-3 */
}

/* 햄버거 버튼 */
.hamburger-btn {
  display: none;
  font-size: 1.8rem;
  color: #3d0f0e; /* 푸딩-5 */
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.hamburger-btn:hover {
  color: #73553c;
}

/* 햄버거 버튼 열림 상태 */
.navbar-center.open,
.navbar-right.open {
  display: flex;
}

/* 로그아웃 및 마이페이지 버튼 스타일 */
.auth-btn {
  font-family: "JalnanFont", sans-serif;
  font-size: 1rem;
  color: #3d0f0e; /* 푸딩-5 */
  text-decoration: none;
  background-color: transparent;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.auth-btn:hover {
  color: #73553c; /* 푸딩-3 */
}

.auth-btn:focus {
  outline: 2px solid #73553c;
  outline-offset: 2px;
}

/* 반응형 스타일 */

@media (max-width: 1028px) {
  .navbar-center a,
  .navbar-center RouterLink,
  .navbar-right a,
  .navbar-right RouterLink {
    font-size: 0.7rem; /* 글씨 크기를 0.8rem으로 줄임 */
    padding: 5px; /* 여백 조정 */
  }

  .hamburger-btn {
    font-size: 1.5rem; /* 햄버거 버튼 크기를 조정 */
  }
}

@media (max-width: 768px) {
  .hamburger-btn {
    display: block; /* 모바일에서 햄버거 버튼 표시 */
  }

  .navbar-center,
  .navbar-right {
    display: none; /* 기본적으로 숨김 */
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #ffffff; /* 푸딩-1 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    gap: 10px;
    padding: 10px 0;
    align-items: center;
    z-index: 100; /* 드롭다운 메뉴의 우선순위를 높임 */
  }

  .navbar-center {
    top: 100%; /* 네비게이션 바로 아래 위치 */
  }

  .navbar-right {
    top: calc(100% + 150px); /* .navbar-center 아래 배치 (적절한 높이로 수정 가능) */
  }

  .navbar-center.open,
  .navbar-right.open {
    display: flex; /* 메뉴 열림 상태에서 표시 */
  }

  .navbar-center a,
  .navbar-center RouterLink,
  .navbar-right a,
  .navbar-right RouterLink {
    font-size: 0.9rem;
    padding: 5px 10px;
    text-align: center;
  }
}


@font-face {
  font-family: 'JalnanFont'; /* Jalnan2TTF 폰트 */
  src: url('@/assets/fonts/Jalnan2TTF.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face{
  font-family: 'GowunDodum-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
</style>

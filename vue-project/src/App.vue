<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { useArticleStore } from "./stores/article";

const router = useRouter();
const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);

// Menu state
const menuOpen = ref(false);
const lastScrollPosition = ref(0);
const isNavVisible = ref(true);

// Logout handler
const handleLogout = async () => {
  try {
    await authStore.logout();
    menuOpen.value = false; // Close menu after logout
    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

// Bank search handler
const handleBankSearch = () => {
  menuOpen.value = false; // Close menu after navigation
  if (router.currentRoute.value.path === "/banks") {
    window.location.reload();
  } else {
    router.push("/banks");
  }
};

// Menu toggle
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

// Close menu when clicking outside
const handleClickOutside = (event) => {
  const nav = document.querySelector('.navbar');
  if (nav && !nav.contains(event.target) && menuOpen.value) {
    menuOpen.value = false;
  }
};

// Handle scroll for hiding/showing navbar
const handleScroll = () => {
  const currentScrollPosition = window.pageYOffset;
  if (currentScrollPosition < 0) {
    return;
  }
  
  // Show/hide navbar based on scroll direction
  if (Math.abs(currentScrollPosition - lastScrollPosition.value) < 60) {
    return;
  }
  
  isNavVisible.value = currentScrollPosition < lastScrollPosition.value;
  lastScrollPosition.value = currentScrollPosition;
};

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <div class="wrapper">
    <nav class="navbar" :class="{ 'nav-hidden': !isNavVisible, 'menu-open': menuOpen }">
      <div class="navbar-left">
        <RouterLink to="/" @click="menuOpen = false">
          <img
            src="@/assets/puddingbank_logo.jpg"
            alt="PuddingBank Logo"
            class="logo-image"
          />
        </RouterLink>
      </div>
      
      <button 
        class="hamburger-btn" 
        @click="toggleMenu"
        :aria-expanded="menuOpen"
        aria-label="Toggle navigation menu"
      >
        <span class="hamburger-icon" :class="{ 'open': menuOpen }">☰</span>
      </button>

      <div class="navbar-center" :class="{ open: menuOpen }">
        <RouterLink to="/service" @click="menuOpen = false">서비스 안내</RouterLink>
        <RouterLink to="/products" @click="menuOpen = false">예적금 상품 비교</RouterLink>
        <RouterLink to="/loan-comparison" @click="menuOpen = false">대출 상품 비교</RouterLink>
        <RouterLink to="/articles" @click="menuOpen = false">게시판</RouterLink>
        <a href="#" @click.prevent="handleBankSearch">은행 찾기</a>
        <RouterLink to="/exchanges" @click="menuOpen = false">환율계산기</RouterLink>
      </div>

      <div class="navbar-right" :class="{ open: menuOpen }">
        <template v-if="!isAuthenticated">
          <RouterLink to="/login" @click="menuOpen = false">로그인</RouterLink>
          <RouterLink to="/signup" @click="menuOpen = false">회원가입</RouterLink>
        </template>
        <template v-if="isAuthenticated">
          <RouterLink to="/profile" @click="menuOpen = false">마이페이지</RouterLink>
          <button @click="handleLogout" class="logout-btn auth-btn">
            로그아웃
          </button>
        </template>
      </div>
    </nav>

    <div class="content-wrapper">
      <RouterView />
    </div>
  </div>
  <footer class="footer">
    <p>© 2024 Pudding Bank. All Rights Reserved.</p>
  </footer>
</template>

<style scoped>
/* Your existing font-face declarations */
@font-face {
  font-family: 'jjinbbangB';
  src: url('@/assets/fonts/AjjinbbangB.TTF') format('truetype');
  font-display: swap; /* 폰트 로딩 최적화 */
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'jjinbbangM'; 
  src: url('@/assets/fonts/AjjinbbangM.TTF') format('truetype');
  font-display: swap; /* 폰트 로딩 최적화 */
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'JalnanFont'; /* Jalnan2TTF 폰트 */
  src: url('@/assets/fonts/Jalnan2TTF.ttf') format('truetype');
  font-display: swap; /* 폰트 로딩 최적화 */
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'GowunDodum-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-display: swap; /* 폰트 로딩 최적화 */
  font-weight: normal;
  font-style: normal;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: transform 0.3s ease-in-out;
}

.nav-hidden {
  transform: translateY(-100%);
}

.navbar-left .logo-image {
  width: 150px;
  height: auto;
  transition: transform 0.3s ease;
}

.navbar-left .logo-image:hover {
  transform: scale(1.05);
}

.navbar-center {
  display: flex;
  gap: 50px;
  transition: all 0.3s ease;
}

.navbar-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.navbar-center a,
.navbar-right a {
  font-family: "JalnanFont", sans-serif;
  font-size: 1.3rem;
  color: #3d0f0e;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.navbar-center a::after,
.navbar-right a::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -5px;
  left: 50%;
  background-color: #73553c;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.navbar-center a:hover::after,
.navbar-right a:hover::after {
  width: 100%;
}

.hamburger-btn {
  display: none;
  font-size: 1.8rem;
  color: #3d0f0e;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 10px;
  z-index: 1001;
}

.hamburger-icon {
  transition: transform 0.3s ease;
}

.hamburger-icon.open {
  transform: rotate(90deg);
}

.auth-btn {
  font-family: "JalnanFont", sans-serif;
  font-size: 1rem;
  color: #3d0f0e;
  background-color: transparent;
  border: 2px solid #3d0f0e;
  padding: 8px 16px;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.auth-btn:hover {
  background-color: #3d0f0e;
  color: #ffffff;
}

.wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  padding-top: 120px; /* navbar의 높이 + 여유 공간 */
}

/* Footer */
.footer {
  background: #3d0f0e;
  color: #fff;
  padding: 30px 0;
  text-align: center;
  position: relative;
  margin-top: auto;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, #FFE5D9, #FFF0E5);
}

.footer p {
  font-family: 'JalnanFont', sans-serif;
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding-top: 60px; /* 모바일에서는 더 작은 여백 */
  }
}

@media (max-width: 1028px) {
  .navbar-center a,
  .navbar-right a {
    font-size: 1rem;
  }
  
  .navbar-center {
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .hamburger-btn {
    display: block;
  }

  .navbar-center,
  .navbar-right {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px 0;
    text-align: center;
  }

  .navbar-center.open,
  .navbar-right.open {
    display: flex;
    animation: slideDown 0.3s ease-in-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .navbar-center a,
  .navbar-right a {
    padding: 15px 0;
    font-size: 1.1rem;
  }

  .navbar-center a::after,
  .navbar-right a::after {
    display: none;
  }
}
</style>

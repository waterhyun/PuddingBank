<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from '@/stores/auth'
import { useArticleStore } from "@/stores/article"
import { storeToRefs } from 'pinia'

const router = useRouter()
const authStore = useAuthStore()
const articleStore = useArticleStore()
const { user } = storeToRefs(authStore)
const latestPost = ref(null)

const slides = ref([
  {
    image: "/images/banner/banner1.png",
    title: "Millefeuille Special Event",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 1",
    alt: "Millefeuille Slide",
    link: '/loan-comparison',
  },
  {
    image: "/images/banner/banner2.png",
    title: "CMS 신규가입 이벤트 안내",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 2",
    alt: "Slide 2",
    link: '/loan-test',
  },
  {
    image: "/images/banner/banner3.png",
    title: "CMS 신규가입 혜택",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 3",
    alt: "Slide 3",
    link: '/products',
  },
])

const currentIndex = ref(0)
let intervalId

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % slides.value.length
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + slides.value.length) % slides.value.length
}

const navigateToArticle = (articleId) => {
  router.push(`/articledetail/${articleId}`)
}

const fetchArticles = async () => {
  try {
    const announcements = await articleStore.getAnnouncements()
    console.log(announcements)
    if (announcements && announcements.length > 0) {
      // 공지사항 중 가장 최근 글을 latestPost에 저장
      const noticeAnnouncements = announcements.filter(
        post => post.category_display === "공지"
      )
      if (noticeAnnouncements.length > 0) {
        latestPost.value = noticeAnnouncements[0]
      }
    }
  } catch (error) {
    console.error("공지사항을 불러오는 중 오류가 발생했습니다:", error)
  }
}

onMounted(async () => {
  // 캐러셀 인터벌 설정
  intervalId = setInterval(() => {
    nextSlide()
  }, 3000)
  
  // 공지사항 즉시 로드
  await fetchArticles()
})

// 컴포넌트가 언마운트될 때 인터벌 정리
onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`
}

const navigateToPage = (link) => {
  if (link) {
    router.push(link)
  }
}

const navigateToMyPage = () => {
  if (!authStore.isAuthenticated) {
    router.push("/login")
    return
  }
  router.push("/profile")
}

const navigateToLoan = () => {
  router.push("/loan-comparison")
}

const navigateToLoantest = () => {
  router.push("/loan-test")
}

const navigateToProducts = () => {
  router.push("/products")
}
</script>

<template>
  <div>
    <div class="main-container">
      <!-- 상단 섹션: 배너와 서비스 -->
      <div class="top-section">
        <!-- 이벤트 배너 -->
        <section class="banner">
          <div class="carousel">
            <div class="carousel-wrapper" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
              <div v-for="(slide, index) in slides" :key="index" class="carousel-slide" :class="{ active: index === currentIndex }" @click="navigateToPage(slide.link)">
                <img :src="slide.image" :alt="slide.alt" class="carousel-image" />
              </div>
            </div>
            <button class="prev-btn" @click="prevSlide">&#10094;</button>
            <button class="next-btn" @click="nextSlide">&#10095;</button>
          </div>
        </section>

        <!-- 주요 서비스 -->
        <section class="services-section">
          <!-- 상단 서비스 박스 -->
          <div class="services-box">
            <h2 v-if="authStore.isAuthenticated"> 🍮 반갑습니다, {{ user.name }}님!</h2>
            <h2 v-else>🍮 반갑습니다!</h2>
            <div class="service-icons">
              <div class="icon-card">
                <img @click='navigateToMyPage' src="/images/banner/mypage.png" alt="">
                <p>마이페이지</p>
              </div>
              <div class="service-hello">
                <p v-if="authStore.isAuthenticated">오늘도 {{ user.name }}님의 목표를 위해 Pudding Bank가 도와드릴게요🍯</p>
                <p v-else>로그인하고 Pudding Bank의
              다양한 서비스를 이용해보세요 🍯</p>
              </div>
            </div>
          </div>

          <!-- 하단 알림 박스 -->
          <div class="notification-box">
            <h3>📢 알려드립니다</h3>
            <div 
              class="notification-content" 
              v-if="latestPost"
              @click="navigateToArticle(latestPost.id)"
              style="cursor: pointer;"
            >
              <p>{{ latestPost.title }}</p>
              <span class="date">{{ formatDate(latestPost.created_at) }}</span>
            </div>
            <div class="notification-content" v-else>
              <p>최근 공지를 불러오는 중...</p>
            </div>
          </div>
        </section>
      </div>

      <!-- CMS 특징 -->
      <section class="features">
        <h2>"푸딩뱅크의 금융 상품 비교 서비스를 경험해보세요"</h2>
        <div class="feature-grid">
          <div class="feature-item1" @click="navigateToProducts">
            <img src="/images/banner/products_banner.png" alt="">
            <p class="feature-item1-p">예금 · 적금 상품 확인하기</p>
          </div>
          <div class="feature-item2" @click="navigateToLoan">
            <img src="/images/banner/loan_banner.png" alt="">
            <p>대출 상품 확인하기</p>
          </div>
        </div>
      </section>

      <!-- CTA 배너 -->
      <section class="cta" @click="navigateToLoantest">
        <div class="cta-item">
          <img src="/images/banner/recom_banner.png" alt="">
          <p>맞춤형 대출 추천받기</p>
        </div>
      </section>

        <!-- CMS 파트너 -->
        <!-- <section class="partners">
          <h2>나만의 CMS 파트너</h2>
          <div class="partner-grid">
            <div class="partner-item">세무/회계</div>
            <div class="partner-item">후원</div>
            <div class="partner-item">임대</div>
            <div class="partner-item">비영리</div>
            <div class="partner-item">IT 서비스</div>
          </div>
        </section> -->
    </div>
  </div>
</template>

<!-- <script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from '@/stores/auth'
import { useArticleStore } from "@/stores/article";
import { storeToRefs } from 'pinia'

const router = useRouter();
const authStore = useAuthStore()
const articleStore = useArticleStore()
const { user } = storeToRefs(authStore)
const latestPost = ref(null); // 최근 게시글 데이터를 저장할 변수

// 슬라이드 이미지 및 텍스트 정의
const slides = ref([
  {
    image: "/images/banner/banner1.png",
    title: "Millefeuille Special Event",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 1",
    alt: "Millefeuille Slide",
    link: '/loan-comparison',
  },
  {
    image: "/images/banner/banner2.png",
    title: "CMS 신규가입 이벤트 안내",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 2",
    alt: "Slide 2",
    link: '/loan-test',
  },
  {
    image: "/images/banner/banner3.png",
    title: "CMS 신규가입 혜택",
    description: "특정 은행 가입 시 제공되는 특별한 혜택 3",
    alt: "Slide 3",
    link: '/products',
  },
]);

const currentIndex = ref(0);

// 다음 슬라이드로 이동
const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % slides.value.length;
};

// 이전 슬라이드로 이동
const prevSlide = () => {
  currentIndex.value =
    (currentIndex.value - 1 + slides.value.length) % slides.value.length;
};

// 자동 슬라이드 기능
let intervalId;

const fetchArticles = async () => {
  try {
    // 데이터가 제대로 로드되었는지 확인
    if (!articleStore.articles || articleStore.articles.length === 0) {
      console.warn("게시글 데이터가 비어 있습니다. 다시 시도합니다...");
      // 3초 후에 다시 시도
      setTimeout(() => {
        fetchArticles(); // 재귀 호출
      }, 3000);
      return; // 다음 로직으로 넘어가지 않도록 함
    }

    // 게시글 로드 이후 로그 출력
    // console.log("Loaded Articles:", articleStore.articles);

    // 현재 카테고리에 맞는 게시글 필터링
    const filteredArticles = articleStore.articles.filter(
      article => article.category_display === "공지"
    );

    // 필터링 결과 처리
    if (filteredArticles && filteredArticles.length > 0) {
      latestPost.value = filteredArticles[0]; // 가장 최근 게시글 설정
      // console.log("Latest Post:", latestPost.value);
    } else {
      console.warn("공지 카테고리의 게시글이 없습니다. 다시 시도합니다...");
      // 3초 후에 다시 시도
      setTimeout(() => {
        fetchArticles(); // 재귀 호출
      }, 3000);
    }
  } catch (error) {
    console.error("게시글을 불러오는 중 오류가 발생했습니다:", error);
  }
};

 
onMounted(async () => {
  // 자동 슬라이드 시작
  intervalId = setInterval(() => {
    nextSlide();
  }, 3000);

  articleStore.getArticles();
  fetchArticles(); // 게시글 데이터를 가져오는 함수 실행

});

// 날짜 변환
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
};


// 페이지 이동 함수
const navigateToPage = (link) => {
  if (link) {
    router.push(link); // Vue Router로 페이지 이동
  }
};

// 클릭 이벤트로 "/loan-comparison"으로 이동
const navigateToMyPage = () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  router.push("/profile");
};

// 클릭 이벤트로 "/loan-comparison"으로 이동
const navigateToLoan = () => {
  router.push("/loan-comparison");
};

// 클릭 이벤트로 "/loan-test"으로 이동
const navigateToLoantest = () => {
  router.push("/loan-test");
};


// 클릭 이벤트로 "/products"으로 이동
const navigateToProducts = () => {
  router.push("/products");
};


</script> -->

<style scoped>
/* 공통 스타일 */
.main-container {
  max-width: 1200px;
  min-height: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fffefb;
}

/* 상단 섹션 스타일 */
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
  height: 300px;
}

/* 이벤트 배너 */
.banner {
  flex: 2;
  border-radius: 10px;
  overflow: hidden;
  height: 100%;
}

/* Carousel 스타일 */
.carousel {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
  height: 100%;
}

.carousel-slide {
  flex: 1 0 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 100%;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease-in-out;
}

.carousel-slide img:hover {
  transform: scale(1.05);
}

/* 텍스트 스타일 */
.slide-content {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  text-align: center;
  background: rgba(0, 0, 0, 0.336);
  padding: 15px 20px;
  border-radius: 8px;
  width: 90%;
  box-sizing: border-box;
}

.slide-content h1 {
  font-size: 1.5em;
  font-family: 'JalnanFont', sans-serif;
  margin-bottom: 10px;
  font-weight: bold;
}

.slide-content p {
  font-size: 1em;
  margin-bottom: 10px;
}

/* 버튼 스타일 */
.prev-btn,
.next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.103);
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prev-btn {
  left: 10px;
}

.next-btn {
  right: 10px;
}

.prev-btn:hover,
.next-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

/* 주요 서비스 */
.services-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
}

/* 서비스 박스 */
.services-box {
  flex: 1;
  background: #ffffff;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.services-box h2 {
  text-align: center;
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-family: 'JalnanFont', sans-serif;
}

.service-icons {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px;
}

.icon-card {
  flex: 0 0 auto;
  text-align: center;
  width: 80px;
}

.icon-card img {
  width: 40px;
  height: 40px;
}

.icon-card p {
  margin-top: 5px;
  margin-bottom: 0px;
  font-size: 0.8rem;
  font-family: 'JalnanFont', sans-serif;
}

.service-hello {
  flex: 1;
  text-align: left;
  font-family: 'GowunDodum-Regular', sans-serif;
}


/* 알림 박스 */
.notification-box {
  flex: 1;
  background: #fffbdb;
  border-radius: 10px;
  padding: 10px 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.notification-box h3 {
  font-size: 1.1rem;
  margin-top: 1px;
  margin-bottom: 8px;
  font-family: 'JalnanFont', sans-serif;
}

.notification-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.notification-content p {
  font-size: 0.9rem;
  margin: 0;
  font-family: 'JalnanFont', sans-serif;
}

.notification-content .date {
  font-size: 0.8rem;
  font-family: 'JalnanFont', sans-serif;
  color: #666;
}

.notification-content:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.btn {
  padding: 8px 16px;
  background: #ffcc00;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: bold;
  color: #333;
}

/* Dots Navigation */
.dots {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.dot {
  width: 10px;
  height: 10px;
  margin: 0 5px;
  background: #ddd;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.3s;
}

.dot.active {
  background: #333;
}

/* 주요 서비스 */
.services {
  flex: 1; /* 좁은 비율 */
  background: #f9f9f9;
  text-align: center;
  border-radius: 10px;
  padding: 20px;
}

.services h2 {
  margin-bottom: 20px;
}

.service-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.card {
  padding: 15px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Features 섹션 */
.features {
  margin-top: 60px;
  margin-bottom: 30px;
  padding: 0 20px;
}

.features h2 {
  text-align: center;
  font-family: 'JalnanFont', sans-serif;
  color: #3d0f0e;
  margin-bottom: 25px;
  font-size: 1.5rem;
}

.feature-grid {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.feature-item1, .feature-item2 {
  flex: 1;
  text-align: center;
  padding: 15px;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 15px;
  height: 120px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-item1 {
  background: #FFE5D9; /* 연한 살구색 */
}

.feature-item2 {
  background: #E5F1FF; /* 연한 하늘색 */
}

.feature-item1:hover, .feature-item2:hover {
  transform: translateY(-3px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}

.feature-item1 img, .feature-item2 img {
  width: 80px; /* 이미지 크기 조정 */
  height: 80px;
  padding-left: 50px;
  object-fit: contain; /* 이미지 비율 유지 */
  flex-shrink: 0; /* 이미지 크기 고정 */
}

.feature-item1 p, .feature-item2 p {
  font-family: 'JalnanFont', sans-serif;
  color: #3d0f0e;
  margin: 0;
  font-size: 1.1rem;

}

/* CTA 배너 */
.cta {
  margin: 30px auto;
  padding: 0 20px;
  max-width: 900px;
}

.cta-item {
  text-align: center;
  background: #E8F5E9; /* 연한 민트색 배경 */
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  height: 120px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}

.cta-item img {
  width: 100px;
  height: 100px;
  object-fit: contain;
  border-radius: 8px;
}

.cta-item p {
  font-family: 'JalnanFont', sans-serif;
  color: #3d0f0e;
  margin: 0;
  font-size: 1.1rem;
}


/* Footer
.footer {
  background: #3d0f0e;
  color: #fff;
  padding: 30px 0;
  margin-top: 50px;
  text-align: center;
  position: relative;
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
} */

/* CMS 파트너
.partners {
  text-align: center;
  padding: 40px 20px;
}

.partners h2 {
  margin-bottom: 30px;
}

.partner-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.partner-item {
  flex: 1 1 calc(25% - 20px);
  padding: 20px;
  background: #f5f5f5;
  text-align: center;
  border-radius: 10px;
} */

/* 반응형 */
/* 반응형 스타일 */
@media (max-width: 768px) {
  .services-box h2,
  .notification-box h3 {
    font-size: 1.2rem; /* 작은 화면에서 글씨 크기 줄이기 */
  }

  .service-icons p,
  .notification-content p {
    font-size: 0.9rem; /* 작은 화면에서 글씨 크기 줄이기 */
  }

  .notification-content .date {
    font-size: 0.8rem; /* 날짜 글씨 크기 줄이기 */
  }

  .feature-grid {
    flex-direction: column;
  }
  
  .feature-item1, .feature-item2 {
    height: 100px;
  }
  
  .feature-item1 img, .feature-item2 img {
    width: 80px;
    height: 80px;
  }
  
  .feature-item1 p, .feature-item2 p {
    font-size: 1rem;
  }

  .cta-item {
    height: 100px;
  }
  
  .cta-item img {
    width: 80px;
    height: 80px;
  }
  
  .cta-item p {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .services-box h2,
  .notification-box h3 {
    font-size: 1rem; /* 더 작은 화면에서 글씨 크기 줄이기 */
  }

  .service-icons p,
  .notification-content p {
    font-size: 0.8rem; /* 더 작은 화면에서 글씨 크기 줄이기 */
  }

  .notification-content .date {
    font-size: 0.7rem; /* 날짜 글씨 크기 줄이기 */
  }
}

</style>

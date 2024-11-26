<template>
  <div>
    <div class="main-container">
      <!-- 상단 섹션: 배너와 서비스 -->
      <div class="top-section">
        <!-- 이벤트 배너 -->
        <section class="banner">
          <div class="carousel">
            <div
              class="carousel-wrapper"
              :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
            >
              <div
                v-for="(slide, index) in slides"
                :key="index"
                class="carousel-slide"
                :class="{ active: index === currentIndex }"
                @click="navigateToPage(slide.link)"
              >
                <img :src="slide.image" :alt="slide.alt" class="carousel-image" />
                <!-- <div class="slide-content">
                  <button class="btn">자세히 보기</button>
                </div> -->
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
            <h2>🍮반갑습니다, {{ user.name }}님!</h2>
            <div class="service-icons">
              <div class="icon-card">
                <img @click='navigateToMyPage' src="/images/banner/mypage.png" alt="">
                <p>마이페이지</p>
              </div>
              <div class="service-hello">
                <p>오늘도 {{ user.name }}님의 목표를 위해 Pudding Bank가 도와드릴게요🍯</p>
              </div>
            </div>
          </div>

          <!-- 하단 알림 박스 -->
          <div class="notification-box">
            <h3>📢알려드립니다</h3>
            <div class="notification-content" v-if="latestPost">
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
            <p>예금 · 적금 상품 확인하기</p>
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
          <p>맟춤형 대출 추천받기</p>
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
  
  <footer class="footer">
    <p>© 2024 Pudding Bank. All Rights Reserved.</p>
  </footer>
</template>

<script setup>
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
const navigateToMyPage= () => {
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


</script>

<style scoped>
/* 공통 스타일 */

.main-container {
  max-width: 1200px;
  min-height: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fffefb;
}

/* 상단 섹션: 배너와 서비스 */
.top-section {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  align-items: center; /* 가로 방향 중앙 정렬 */
}

/* 이벤트 배너 */
.banner {
  flex: 2;
  border-radius: 10px;
  overflow: hidden;
  max-height: 400px;
  position: relative; /* 텍스트와 이미지 레이어 구분을 위한 설정 */
}

.carousel {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  display: flex;
  justify-content: center; /* 이미지 가운데 정렬 */
  align-items: center; /* 이미지 가운데 정렬 */
  width: 100%; /* 슬라이드 전체 너비 */
  height: 300px; /* 원하는 슬라이드 높이 */
  overflow: hidden; /* 이미지가 부모를 벗어나지 않도록 숨김 */
  position: relative; /* 필요 시 자식 요소 배치 조정 */
  background-color: #f8f8f8; /* 배경색 (선택 사항) */
  border-radius: 10px; /* 둥근 모서리 효과 (선택 사항) */
}

.carousel-slide img {
  width: 100%; /* 부모 컨테이너 너비에 맞춤 */
  height: 100%; /* 부모 컨테이너 높이에 맞춤 */
  object-fit: cover; /* 이미지가 영역을 꽉 채우도록 조정 */
  border-radius: 10px; /* 부모와 동일한 둥근 모서리 (선택 사항) */
  transition: transform 0.3s ease-in-out; /* 애니메이션 효과 (선택 사항) */
}

.carousel-slide img:hover {
  transform: scale(1.05); /* 마우스 오버 시 확대 효과 (선택 사항) */
}
.carousel-image {
  width: 100%; /* 이미지 너비 */
  height: auto; /* 비율 유지 */
  max-height: 500px; /* 최대 높이 제한 */
  object-fit: cover; /* 슬라이드에 꽉 차도록 조정 */
  border-radius: 10px; /* 선택 사항: 둥근 모서리 */
}

/* 텍스트 스타일 */
.slide-content {
  position: absolute;
  bottom: 20px; /* 텍스트 위치를 이미지 하단에서 20px 위로 조정 */
  left: 50%;
  transform: translateX(-50%);
  color: white;
  text-align: center;
  background: rgba(0, 0, 0, 0.336); /* 텍스트 배경 어두운 반투명 추가 */
  padding: 15px 20px; /* 배경 내부 여백 추가 */
  border-radius: 8px; /* 배경 모서리 둥글게 */
  width: 90%; /* 배경의 너비를 이미지에 비례 */
  box-sizing: border-box; /* 패딩 포함하여 박스 크기 계산 */
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
  gap: 20px;
}

/* 서비스 박스 */
.services-box {
  background: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.services-box h2 {
  text-align: center;
  margin-bottom: 15px;
  font-size: 1.5rem;
  font-family: 'JalnanFont', sans-serif;
}

.service-icons {
  display: flex;
  justify-content: space-around;
  gap: 10px;
}

.icon-card {
  text-align: center;
  width: 150px;
}

.icon-card img {
  width: 50px;
  height: 50px;
}

.icon-card p {
  margin-top: 5px;
  font-size: 0.9rem;
  font-family: 'JalnanFont', sans-serif;
}

/* 알림 박스 */
.notification-box {
  background: #fffbdb;
  border-radius: 10px;
  padding: 10px;
  padding-right: 20px;
  padding-left: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.notification-box h3 {
  font-size: 1.2rem;
  margin-top: 1px;
  margin-bottom: 10px;
  font-family: 'JalnanFont', sans-serif;
}

.notification-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
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


/* 상단 섹션 스타일 */
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

/* 이벤트 배너 */
.banner {
  flex: 2; /* 더 넓은 비율 */
  background: #0046b3;
  color: #ffffff;
  text-align: center;
  border-radius: 10px;
  overflow: hidden;
  max-height: 300px; /* 높이 제한 */
}

/* Carousel 스타일 */
.carousel {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  flex: 1 0 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.slide-content {
  position: absolute;
  color: white;
  text-align: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}

.slide-content h1 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.slide-content p {
  font-size: 1em;
  margin-bottom: 10px;
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

/* 버튼 스타일 */
.prev-btn,
.next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
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

.service-hello {
font-size: 0.9rem;
  margin: 0;
  font-family: 'GowunDodum-Regular', sans-serif;
}

.card {
  padding: 15px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* CMS 특징 */
.features {
  background: #ffffff;
  padding: 20px 20px;
}

.features h2 {
  margin-bottom: 30px;
  text-align: center; /* 텍스트 가운데 정렬 */
  font-family: 'JalnanFont', sans-serif;
}

.feature-grid {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  font-family: 'JalnanFont', sans-serif;
}

.feature-item1 {
  flex: 1;
  padding: 20px;
  background: #FFF4E6;
  border-radius: 10px;
  text-align: center;
  height: 150px; /* 고정 높이 지정 */
  display: flex; /* 내용 중앙 정렬을 위한 설정 */
  flex-direction: column; /* 세로 방향 정렬 */
  justify-content: center; /* 수직 중앙 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  color: #E67E22; /* 주황색 텍스트 */
}

.feature-item1 img {
  width: 30%; /* 이미지 너비 */
  height: auto; /* 비율 유지 */
  object-fit: contain; /* 이미지가 박스에 맞게 조정 */
}

.feature-item2 {
  flex: 1;
  padding: 20px;
  background: #E6F7FF;
  border-radius: 10px;
  text-align: center;
  height: 150px; /* 고정 높이 지정 */
  display: flex; /* 내용 중앙 정렬을 위한 설정 */
  flex-direction: column; /* 세로 방향 정렬 */
  justify-content: center; /* 수직 중앙 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  color: #3498DB; /* 파란색 텍스트 */
}

.feature-item2 img {
  width: 30%; /* 이미지 너비 */
  height: auto; /* 비율 유지 */
  object-fit: contain; /* 이미지가 박스에 맞게 조정 */
}

/* CTA 배너 */
.cta {
  display: flex;
  border-radius: 10px;
  justify-content: space-around;
  align-items: center;
  padding: 5px 20px;
  gap: 20px; /* 배너 간 간격 추가 */
  font-family: 'JalnanFont', sans-serif;
}

.cta-item {
  text-align: center;
  background: #EBF8E1; /* 연녹색 */
  border-radius: 10px;
  color: #27AE60; /* 진한 녹색 텍스트 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 수직 중앙 정렬 */
  gap: 15px; /* 이미지와 버튼 간격 */
  height: 200px;
  width: 100%;
}

.cta-item img {
  width: 150px; /* 이미지 너비 */
  height: auto; /* 비율 유지 */
  border-radius: 10px; /* 이미지 모서리 둥글게 */
}


.cta-item button {
  margin-top: 5px;
  padding: 10px 20px;
  background: #ff9933;
  border: none;
  color: #ffffff;
  cursor: pointer;
  border-radius: 5px;
}

/* CMS 파트너 */
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
}

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

.footer {
  margin-top: 40px;
  font-size: 0.9rem;
  color: #777;
  padding: 10px 0;
  background-color: #fffefb;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'GowunDodum-Regular', sans-serif;
}
</style>
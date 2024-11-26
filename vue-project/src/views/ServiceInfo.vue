<template>
  <div class="service-info">
    <section class="hero">
      <div class="hero-content">
        <h1>내 손안의<br>맛있는 금융,<br>푸딩뱅크</h1>
        <p>금융이 달콤해지는 순간, 당신의 첫 금융 상품 추천 플랫폼</p>
      </div>
      <div class="hero-image">
        <img src="/images/service/app-preview.png" alt="앱 미리보기">
      </div>
    </section>

    <!-- 주요 기능 소개 -->
    <section class="features">
      <h2 class="section-title">한눈에 확인하는<br>푸딩뱅크 서비스</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon">💰</div>
          <h3>예금/적금 상품 비교</h3>
          <p>정기예금과 적금 상품을 쉽게 비교하고<br>최적의 금리 상품을 찾아보세요</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🏦</div>
          <h3>대출 상품 비교</h3>
          <p>다양한 대출 상품의 금리와 한도를<br>한눈에 비교해보세요</p>
        </div>
      </div>
    </section>

    <!-- 서비스 상세 소개 -->
    <section class="service-details">
      <div class="detail-card">
        <div class="detail-content">
          <h3>맞춤형 대출 상품 추천 😉</h3>
          <p>재미있는 질문을 통해 대출 취향을 탐색할 수 있는 설문 서비스입니다. 각 질문에 디저트 일러스트가 포함되어 있어 더욱 즐겁게 참여할 수 있으며, 설문 결과로 나에게 딱 맞는 맞춤 대출 디저트를 추천해드립니다!</p>
        </div>
        <img src="/images/service/service1.png" alt="맞춤형 추천" class="detail-image">
      </div>

      <div class="detail-card reverse">
        <div class="detail-content">
          <h3>실시간 환율 계산기 💱</h3>
          <p>실시간 환율 정보를 바탕으로 외화와 원화를 간편하게 계산할 수 있는 서비스입니다. 원하는 국가의 통화를 선택하고 금액을 입력하면, 정확한 환산 금액을 즉시 확인할 수 있습니다. 여행 준비나 국제 송금 등 다양한 상황에서 손쉽게 환율을 계산해보세요!</p>
        </div>
        <img src="/images/service/service2.png" alt="환율 계산" class="detail-image">
      </div>

      <div class="detail-card">
        <div class="detail-content">
          <h3>스마트 은행 찾기 🏛</h3>
          <p>검색창을 통해 특정 은행을 검색하거나, 내 위치에서 찾기 버튼을 눌러 주변 금융 기관을 빠르게 확인할 수 있습니다. 지도에는 위치 정보가 표시되며, 거리순으로 정렬된 목록을 통해 가까운 은행의 상세 정보를 확인할 수 있습니다.</p>
        </div>
        <img src="/images/service/service3.png" alt="은행 검색" class="detail-image">
      </div>
    </section>

    <!-- 커뮤니티 섹션 -->
    <section class="community">
      <h2>함께 성장하는 금융 커뮤니티</h2>
      <div class="community-content">
        <p>공지사항, 추천, 질문, 자유 게시판에서<br>다양한 금융 정보를 나누어보세요 💞</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.service-info {
  font-family: 'GowunDodum-Regular', sans-serif;
  color: #73553C;
  background-color: #FFFEFB;
  width: 100%;
}

/* Hero Section */
.hero {
  display: flex;
  padding: 60px 40px;
  justify-content: center; /* 중앙 정렬로 변경 */
  align-items: center;
  background-color: #FEF0AC;
  gap: 1; /* 간격 살짝 늘림 */
  max-width: 1400px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
}

.hero-content {
  flex: 1;
  max-width: 500px; /* 콘텐츠 영역 최대 너비 제한 */
}

.hero-content h1 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 2.5rem;
  line-height: 1.4;
  color: #3D0F0E;
  margin-bottom: 15px;
}

.hero-content p {
  font-family: 'jjinbbangM', sans-serif;
  font-size: 1.1rem;
  color: #73553C;
}

.hero-image {
  width: 100%;
  max-width: 250px;
}

.hero-image img {
  width: 100%;
  height: auto;
  object-fit: contain;
}

/* Features Section */
.features,
.service-details,
.community {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section-title {
  font-family: 'JalnanFont', sans-serif;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 40px;
  color: #3D0F0E;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  padding: 0 15px;
}

.feature-item {
  text-align: center;
  padding: 25px;
  background-color: #FDE49B;
  border-radius: 15px;
  transition: transform 0.3s ease;
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.feature-item h3 {
  font-family: 'jjinbbangB', sans-serif;
  font-size: 1.3rem;
  margin-bottom: 12px;
  color: #3D0F0E;
}

/* Service Details */
.detail-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 25px auto;
  background-color: rgba(254, 240, 172, 0.1);
  border-radius: 15px;
  padding: 30px;
  gap: 30px;
  box-shadow: 0 4px 15px rgba(115, 85, 60, 0.1);
  transition: box-shadow 0.3s ease;
}

.detail-card:hover {
  box-shadow: 0 8px 25px rgba(115, 85, 60, 0.15);
}

.detail-card .detail-image {
  width: 100%;
  max-width: 200px;
  height: auto;
  object-fit: contain;
}

.detail-content {
  flex: 1;
  max-width: 500px;
}

.detail-content h3 {
  font-family: 'jjinbbangB', sans-serif;
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: #3D0F0E;
}

.detail-content p {
  font-size: 1rem;
  line-height: 1.6;
}

.detail-card.reverse {
  flex-direction: row-reverse;
  text-align: right;  /* 텍스트를 오른쪽 정렬 */
}

.detail-card.reverse .detail-content {
  margin-left: auto;  /* 오른쪽 정렬을 위한 마진 설정 */
}

/* Community Section */
.community {
  background-color: #FEF0AC;
  text-align: center;
  border-radius: 15px;
  margin: 0 auto 40px auto;
  max-width: 800px;
  padding: 40px 5px;
}

.community h2 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 2rem;
  color: #3D0F0E;
  margin-bottom: 20px;
}

.community-content p {
  font-family: 'jjinbbangM', sans-serif;
  font-size: 1.1rem;
  line-height: 1.5;
  color: #73553C;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 40px 20px;
  }

  .hero-image {
    margin: 30px auto 0;
    max-width: 200px;
  }

  .detail-card,
  .detail-card.reverse {
    flex-direction: column;
    text-align: center;
  }

  .detail-card .detail-image {
    max-width: 180px;
    margin: 15px auto;
  }

  .detail-content {
    max-width: 100%;
  }

  .detail-card.reverse .detail-content {
    margin-left: 0;  /* 모바일에서는 마진 제거 */
  }
}

</style>

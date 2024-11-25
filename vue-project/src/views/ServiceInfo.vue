<template>
  <div class="pudding-bank">
    <header class="header">
      <h1>Pudding Bank</h1>
      <p>복잡한 금융 상품도 푸딩처럼 부드럽게!</p>
    </header>
    <section class="services">
      <h2>우리의 특별한 금융 레시피</h2>
      <div class="card" v-for="(service, index) in services" :key="index">
        <h3>{{ service.title }}</h3>
        <p>{{ service.description }}</p>
      </div>
    </section>
  </div>
    <footer class="footer">
      <p>© 2024 Pudding Bank. All Rights Reserved.</p>
    </footer>
</template>

<script>
export default {
  name: "PuddingBank",
  data() {
    return {
      services: [
        {
          title: "디저트 메뉴판으로 보는 예금/적금 비교",
          description:
            "각 상품을 디저트에 비유해 직관적으로 이해할 수 있도록 구성했습니다. 예: '푸딩처럼 안정적인 정기예금'. 금리 비교표는 디저트 레시피처럼 재미있게 만나보세요!",
        },
        {
          title: "시그니처 메뉴 같은 대출 상품 비교",
          description:
            "대표 대출 상품을 시그니처 디저트처럼 강조하고, 대출 조건은 디저트 재료로 시각화했습니다. 비교 정보를 디저트 플레이팅처럼 한눈에 볼 수 있도록 제공해드립니다.",
        },
        {
          title: "MBTI처럼 재미있는 맞춤형 대출 추천",
          description:
            "재미있는 질문과 디저트 일러스트를 활용해 나만의 대출 상품을 추천합니다. 결과는 '당신의 맞춤 디저트'처럼 제시됩니다!",
        },
        {
          title: "환율 계산도 디저트처럼 쉽고 직관적으로",
          description:
            "환율 계산기를 디저트 계량 도구처럼 심플하고 직관적으로 만들었습니다. 통화별로 다른 디저트 아이콘이 재미를 더해줍니다.",
        },
        {
          title: "주변 은행 찾기, 디저트 카페처럼 쉽게",
          description:
            "지도에서 주변 은행을 디저트 카페처럼 친근하게 찾을 수 있습니다. 각 은행은 디저트 아이콘으로 표시되며 거리순, 평점순으로 정렬 가능합니다.",
        },
        {
          title: "따뜻한 커뮤니티, 디저트 카페처럼",
          description:
            "사용자 후기를 디저트 리뷰처럼, 금융 정보 공유를 레시피 공유처럼 표현했습니다. 따뜻하고 편안한 분위기의 커뮤니티를 경험하세요.",
        },
      ],
    };
  },
};
</script>

<style scoped>
/* 전체 배경 및 폰트 설정 */
.pudding-bank {
  font-family: 'JalnanFont', sans-serif;
  text-align: center;
  padding: 20px 15px;
  background-color: #fffefb;
  color: #333;
}


/* 헤더 스타일 */
.header {
  background-color: #fef0ac;
  padding: 30px 20px;
  border-radius: 10px;
  margin-bottom: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-size: 2.8rem;
  margin-bottom: 15px;
  color: #3D0F0E; 
}

.header p {
  font-size: 1.2rem;
  color: #555;
  line-height: 1.6;
}

/* 서비스 카드 섹션 */
.services {
  margin: 0 auto;
  max-width: 800px;
}

.services h2 {
  font-size: 2rem;
  color: #73553C;
  margin-bottom: 30px;
  text-align: center;
  border-bottom: 2px solid #73553C;
  display: inline-block;
  padding-bottom: 5px;
}

/* 카드 스타일 */
.card {
  background-color: #fef0ac;
  padding: 20px 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.card h3 {
  font-size: 1.2rem;
  color: #73553C;
  margin-bottom: 10px;
}

.card p {
  font-size: 1rem;
  line-height: 1.8;
  color: #555;
  font-family: 'GowunDodum-Regular', sans-serif;
}

/* 푸터 스타일 */
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

<template>
  <div class="loan-result-container">
    <!-- MBTI 결과 섹션 -->
    <div class="mbti-result-section">
    <h2 class="main-title">당신의 대출 MBTI 결과</h2>
    <div class="mbti-dessert-card">
      <!-- 왼쪽: 메인 결과 섹션 -->
      <div class="main-result">
        <div class="dessert-info">
          <h3 class="mbti-type">{{ mbtiResult.mbti_type }}</h3>
          <div class="dessert-image-container">
            <img :src="getDessertImage(mbtiResult?.mbti_type)" 
                 :alt="getDessertName(mbtiResult?.mbti_type)"
                 class="dessert-image"
                 @error="handleImageError">
          </div>
          <p class="dessert-name">{{ getDessertName(mbtiResult.mbti_type) }}</p>
          <p class="dessert-description">{{ getDessertDescription(mbtiResult.mbti_type) }}</p>
        </div>
      </div>

      <!-- 오른쪽: 성향 분석 섹션 -->
      <div class="right-section">        
        <div class="mbti-analysis">
          <h4 class="analysis-title">대출 성향 분석</h4>
          
          <div class="mbti-type-explanation">
            <div class="mbti-letter" v-for="(letter, index) in mbtiLetters" :key="index">
              <span class="letter">{{ letter.code }}</span>
              <span class="meaning">{{ letter.meaning }}</span>
            </div>
          </div>
          <div class="criteria-list">
            <ul>
              <li v-for="(criterion, index) in mbtiResult.matching_criteria.criteria" 
                  :key="index">{{ criterion }}</li>
            </ul>
          </div>

          <!-- 반대 성향 미니 카드 -->
          <div class="opposite-type-section">
            <h4>반대 성향의 디저트</h4>
            <div class="opposite-type-card">
              <div class="opposite-content">
                <p class="opposite-type">{{ getOppositeType(mbtiResult.mbti_type) }}</p>
                <p class="opposite-dessert">{{ getDessertName(getOppositeType(mbtiResult.mbti_type)) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    <!-- 추천 상품 섹션 -->
    <div class="recommendations-section">
      <h2>오늘의 추천 디저트 메뉴</h2>
      <div class="dessert-menu">
        <div v-for="(product, index) in recommendations.products" 
             :key="index" 
             class="dessert-menu-item">
          <div class="menu-header">
            <span class="dessert-icon">🍮</span>
            <h3>{{ product.product_info.kor_co_nm }}</h3>
          </div>
          
          <div class="menu-details">
            <div class="rate-info">
              <h4>디저트 레시피</h4>
              <p>베이스 금리: {{ product.rate_analysis.min_rate }}%</p>
              <p>토핑 금리: {{ product.rate_analysis.max_rate }}%</p>
              <p>평균 당도: {{ product.rate_analysis.avg_rate }}%</p>
              <p>맛 유형: {{ product.rate_analysis.rate_type }}</p>
            </div>

            <div class="product-details">
              <p>제공 용량: {{ product.product_info.loan_lmt }}</p>
              <p>주문 방법: {{ product.product_info.join_way }}</p>
            </div>

            <div v-if="product.matching_points.length > 0" class="matching-points">
              <h4>추천 포인트</h4>
              <ul>
                <li v-for="(point, pointIndex) in product.matching_points" 
                    :key="pointIndex">{{ point }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useLoanStore } from '@/stores/loan'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const store = useLoanStore()
const { mbtiResult, recommendations } = storeToRefs(store)

const getMbtiLetters = (type) => {
  const meanings = {
    'L': '전세자금대출 (Lease)',
    'M': '주택담보대출 (Mortgage)',
    'F': '고정금리 (Fixed)',
    'V': '변동금리 (Variable)',
    'P': '정기상환 (Payment)',
    'D': '수시상환 (Divide)',
    'A': '아파트 (Apartment)',
    'H': '주택/상가 (House)',
    'T': '장기 (Term)',
    'S': '단기 (Short)',
    'G': '정부보증 (Government)',
    'P': '민간보증 (Private)'
  }
  
  return type.split('').map(letter => ({
    code: letter,
    meaning: meanings[letter]
  }))
}

const handleImageError = (e) => {
  e.target.src = '/images/desserts/default.jpg'
}

const mbtiLetters = computed(() => 
  getMbtiLetters(mbtiResult.value.mbti_type)
)


// mbtiResult가 undefined일 경우를 대비한 안전장치 추가
const getDessertImage = (type) => {
  if (!type) return '/images/desserts/default.jpg'
  const dessertImages = {
    'LFSP': '/images/desserts/cupcake.jpeg',
    'LFTG': '/images/desserts/castella.jpeg',
    'MFPA': '/images/desserts/tiramisu.png',
    'MFPH': '/images/desserts/millefeuille.jpeg',
    'MFDA': '/images/desserts/brownie.jpeg',
    'MFDH': '/images/desserts/poundcake.jpeg',
    'MVPA': '/images/desserts/pudding.jpeg',
    'MVPH': '/images/desserts/cream_puff.jpeg',
    'MVDA': '/images/desserts/mousse_cake.jpeg',
    'MVDH': '/images/desserts/eclair.jpeg',
    'LFTP': '/images/desserts/rollcake.jpeg',
    'LFSG': '/images/desserts/macaroon.jpeg',
    'LVTG': '/images/desserts/jelly.jpeg',
    'LVTP': '/images/desserts/croissant.jpeg',
    'LVSG': '/images/desserts/doughnut.jpeg',
    'LVSP': '/images/desserts/tart.jpeg'
  }
  return dessertImages[type] || '/images/desserts/default.jpg'
}


const getDessertName = (type) => {
  const dessertNames = {
    'MFPA': '티라미수',
    'MFPH': '밀푀유',
    'MFDA': '브라우니',
    'MFDH': '파운드 케이크',
    'MVPA': '푸딩',
    'MVPH': '슈크림',
    'MVDA': '무스케이크',
    'MVDH': '에클레어',
    'LFSP': '컵케이크',
    'LFTG': '카스테라',
    'LFTP': '롤케이크',
    'LFSG': '마카롱',
    'LVTG': '젤리',
    'LVTP': '크로와상',
    'LVSG': '도넛',
    'LVSP': '타르트'
  }
  return dessertNames[type] || '기본 디저트'
}

const getDessertDescription = (type) => {
  const dessertDescriptions = {
    'LFSP': '화려한 토핑으로 장식된 아기자기한 컵케이크처럼, 단기 계획에 맞춰 자유롭게 선택할 수 있는 민간 보증 대출 성향을 가지고 있네요. 달콤한 크림처럼 유연하면서도, 단단한 시트처럼 안정적인 당신의 선택!',
    
    'LFTG': '오랜 시간 사랑받아온 클래식한 카스테라처럼, 정부 보증으로 더욱 믿음직한 장기 대출을 선호하시는군요. 촉촉하고 부드러운 식감처럼 안정적인 고정금리를 선호하는 당신의 성향과 찰떡궁합!',
    
    'MFPA': '정교하게 쌓아올린 티라미수처럼, 체계적이고 계획적인 당신의 대출 성향이 돋보여요. 고정금리의 안정감과 아파트의 체계적인 가치를 중시하는 모습이 마치 완벽한 레시피로 만든 디저트 같아요!',
    
    'MFPH': '수백 겹의 페이스트리가 층층이 쌓인 밀푀유처럼, 복합적인 가치를 지닌 단독주택을 선호하시네요. 정교한 계획과 안정적인 상환으로 가치를 높여가는 당신은 마치 장인정신이 깃든 디저트 같아요!',
    
    'MFDA': '겉은 단단하지만 속은 촉촉한 브라우니처럼, 고정금리의 안정감 속에서 자유로운 상환을 추구하시네요. 깊이 있는 초콜릿 맛처럼 아파트의 가치를 아는 당신!',
    
    'MFDH': '기본에 충실하면서도 다양한 변주가 가능한 파운드케이크처럼, 단독주택의 자유로운 가치를 아시네요. 고정금리의 안정감 속에서 자유로운 상환을 계획하는 당신의 선택이 멋져요!',
    
    'MVPA': '부드럽게 흔들리는 푸딩처럼, 변동금리의 유연함을 받아들이면서도 아파트의 안정성을 추구하시네요. 달콤한 카라멜 소스처럼 계획적인 상환으로 균형을 잡는 당신!',
    
    'MVPH': '바삭한 겉면과 부드러운 크림의 조화가 매력적인 슈크림처럼, 변동금리의 기회와 단독주택의 가치를 동시에 누리고 싶으신가봐요. 다양한 변주가 가능한 매력적인 선택!',
    
    'MVDA': '부드럽고 풍부한 무스케이크처럼, 변동금리의 유연함과 자유로운 상환을 선호하시네요. 고급스러운 아파트의 가치를 아는 당신의 안목이 돋보여요!',
    
    'MVDH': '길쭉한 모양에 다양한 토핑으로 변신하는 에클레어처럼, 자유롭고 유연한 대출 성향을 가지고 계시네요. 변동금리와 단독주택의 매력을 아는 당신은 트렌디한 미식가!',
    
    'LFTP': '부드럽게 말린 롤케이크처럼, 안정적인 장기 계획 속에서 민간 보증의 유연함을 추구하시네요. 고정금리의 달콤한 안정감이 크림처럼 가득해요!',
    
    'LFSG': '작고 알록달록한 마카롱처럼, 단기 계획이지만 정부 보증의 안정성을 중시하시네요. 바삭하고 달콤한 겉면처럼 고정금리의 안정감도 놓치지 않는 센스!',
    
    'LVTG': '탱글탱글한 젤리처럼, 변동금리의 유연함 속에서도 정부 보증의 안정성을 추구하시네요. 장기 거주 계획이 달콤한 과즙처럼 가득한 당신의 선택!',
    
    'LVTP': '바삭한 겹겹의 크로와상처럼, 변동금리의 기회를 놓치지 않으면서 장기적인 계획을 세우시는군요. 민간 보증의 유연함이 버터처럼 부드럽게 스며들어요!',
    
    'LVSG': '달콤한 도넛처럼 동그랗게 완성되는 당신의 단기 계획! 변동금리의 기회를 잡으면서도 정부 보증으로 안전하게 진행하시는 현명한 선택이에요!',
    
    'LVSP': '바삭한 타르트지에 다양한 필링을 담을 수 있듯이, 변동금리의 유연함과 민간 보증의 자유로움을 선호하시네요. 단기 계획이지만 달콤한 성공이 기다리고 있어요!'
  }
  return dessertDescriptions[type] || '당신만의 특별한 디저트 같은 대출 성향을 가지고 계시네요!'
}

const getOppositeType = (type) => {
  // 첫 글자가 L(전세자금)인 경우와 M(주택담보)인 경우를 구분
  const isLease = type.startsWith('L')
  
  const leaseOpposites = {
    'F': 'V', 'V': 'F',  // 금리 유형 (고정 vs 변동)
    'T': 'S', 'S': 'T',  // 기간 (장기 vs 단기)
    'G': 'P', 'P': 'G'   // 보증 유형 (정부 vs 민간)
  }
  
  const mortgageOpposites = {
    'F': 'V', 'V': 'F',  // 금리 유형 (고정 vs 변동)
    'P': 'D', 'D': 'P',  // 상환 방식 (정기 vs 수시)
    'A': 'H', 'H': 'A'   // 담보 유형 (아파트 vs 주택/상가)
  }
  
  return type
    .split('')
    .map((char, index) => {
      const opposites = isLease ? leaseOpposites : mortgageOpposites
      return opposites[char] || char
    })
    .join('')
}
</script>


<style scoped>
/* 기본 레이아웃 */
.loan-result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #fff1c9;
}

/* 메인 타이틀 */
.main-title {
  text-align: center;
  color: #73553C;
  font-size: 2.5em;
  margin-bottom: 40px;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

/* MBTI 결과 카드 */
.mbti-dessert-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 20px rgba(212, 84, 125, 0.1);
  margin: 20px 0;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 40px;
}

/* 왼쪽: 메인 결과 섹션 */
.main-result {
  padding-right: 40px;
  border-right: 2px dashed rgba(212, 84, 125, 0.2);
}

.mbti-type {
  font-size: 3em;
  color: #f5c946;
  text-align: center;
  margin-bottom: 30px;
  font-weight: 800;
}

.dessert-info {
  text-align: center;
}

.dessert-image-container {
  width: 320px;
  height: 320px;
  margin: 30px auto;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  transition: transform 0.4s ease;
}

.dessert-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.dessert-image-container:hover {
  transform: scale(1.02);
}

.dessert-name {
  font-size: 1.8em;
  color: #f5c946;
  margin: 20px 0;
  font-weight: 600;
}

.dessert-description {
  color: #666;
  line-height: 1.8;
  font-size: 1.1em;
  padding: 0 20px;
}

/* 오른쪽: 성향 분석 섹션 */
.mbti-analysis {
  background: white;
  border-radius: 15px;
  padding: 30px;
}

.analysis-title {
  color: #f5c946;
  font-size: 1.6em;
  margin-bottom: 25px;
  text-align: center;
  font-weight: 600;
}

.mbti-type-explanation {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.mbti-letter {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.mbti-letter:last-child {
  border-bottom: none;
}

.letter {
  font-weight: 700;
  color: #f5c946;
  font-size: 1.4em;
  min-width: 35px;
}

.meaning {
  color: #666;
  font-size: 1.1em;
}

/* 반대 성향 섹션 */
.opposite-type-section {
  margin-top: 30px;
  padding: 25px;
  background: #fff1c9;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(212, 84, 125, 0.08);
}

.opposite-type-section h4 {
  color: #73553C;
  font-size: 1.4em;
  font-weight: 600;
  text-align: center;
  margin-bottom: 20px;
}

.opposite-type-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(212, 84, 125, 0.1);
  transition: transform 0.3s ease;
}

.opposite-type-card:hover {
  transform: translateY(-5px);
}

.opposite-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.opposite-type {
  color: #73553C;
  font-size: 1.8em;
  font-weight: 700;
  margin-bottom: 5px;
}

.opposite-dessert {
  color: #666;
  font-size: 1.2em;
}

/* 추천 상품 섹션 */
.recommendations-section {
  margin-top: 60px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: rgba(233, 218, 4, 0.15);
}

.recommendations-section h2 {
  color: #f5c946;
  text-align: center;
  margin-bottom: 40px;
}

.dessert-menu {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.dessert-menu-item {
  background: #fff;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(233, 218, 4, 0.15);
  transition: transform 0.3s ease;
}

.dessert-menu-item:hover {
  transform: translateY(-8px);
}

.menu-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px dashed rgb(250, 234, 14);
}

.dessert-icon {
  font-size: 24px;
}

.menu-details {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.rate-info, .product-details, .matching-points {
  margin-bottom: 20px;
}

.rate-info h4, .matching-points h4 {
  color: #f5c946;
  margin-bottom: 15px;
}

.matching-points ul {
  list-style: none;
  padding: 0;
}

.matching-points li {
  padding: 8px 0;
  color: #666;
  position: relative;
  padding-left: 20px;
}

.matching-points li:before {
  content: "•";
  color: #f5c946;
  position: absolute;
  left: 0;
}

@media (max-width: 768px) {
  .mbti-dessert-card {
    grid-template-columns: 1fr;
  }
  
  .main-result {
    padding-right: 0;
    border-right: none;
    border-bottom: 2px dashed rgba(212, 84, 125, 0.2);
    padding-bottom: 40px;
  }
  
  .dessert-menu {
    grid-template-columns: 1fr;
  }
  
  .dessert-image-container {
    width: 280px;
    height: 280px;
  }

  .opposite-type-section {
    margin-top: 20px;
    padding: 20px;
  }
  
  .opposite-type {
    font-size: 1.6em;
  }
  
  .opposite-dessert {
    font-size: 1.1em;
  }
}
</style>

<template>
  <div class="loan-result-container">
    <div class="mbti-result-section">
      <h2>당신의 대출 MBTI 결과</h2>
      <div class="mbti-type">
        <h3>{{ mbtiResult.mbti_type }}</h3>
        <div class="criteria-list">
          <h4>대출 성향 분석</h4>
          <ul>
            <li v-for="(criterion, index) in mbtiResult.matching_criteria.criteria" 
                :key="index">{{ criterion }}</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="recommendations-section">
      <h2>맞춤 대출 상품 추천</h2>
      <div v-for="(product, index) in recommendations.products" 
           :key="index" 
           class="product-card">
        <h3>{{ product.product_info.kor_co_nm }} - {{ product.product_info.fin_prdt_nm }}</h3>
        
        <div class="rate-info">
          <h4>금리 정보</h4>
          <p>최저금리: {{ product.rate_analysis.min_rate }}%</p>
          <p>최고금리: {{ product.rate_analysis.max_rate }}%</p>
          <p>평균금리: {{ product.rate_analysis.avg_rate }}%</p>
          <p>금리유형: {{ product.rate_analysis.rate_type }}</p>
        </div>

        <div class="product-details">
          <p>대출한도: {{ product.product_info.loan_lmt }}</p>
          <p>가입방법: {{ product.product_info.join_way }}</p>
        </div>

        <div v-if="product.matching_points.length > 0" class="matching-points">
          <h4>매칭 포인트</h4>
          <ul>
            <li v-for="(point, pointIndex) in product.matching_points" 
                :key="pointIndex">{{ point }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useLoanStore } from '@/stores/loan'
import { storeToRefs } from 'pinia'

export default {
  name: 'LoanMBTIResultView',
  setup() {
    const store = useLoanStore()
    const { mbtiResult, recommendations } = storeToRefs(store)

    return {
      mbtiResult,
      recommendations
    }
  }
}
</script>

<style scoped>
.loan-result-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.mbti-result-section {
  margin-bottom: 40px;
  text-align: center;
}

.mbti-type {
  margin: 20px 0;
}

.criteria-list {
  margin: 20px 0;
}

.recommendations-section {
  display: grid;
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.rate-info, .product-details, .matching-points {
  margin: 15px 0;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

h3 {
  color: #666;
  margin-bottom: 15px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 8px 0;
}
</style>


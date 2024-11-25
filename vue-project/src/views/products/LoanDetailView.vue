<!-- views/LoanDetailView.vue -->
<template>
  <div class="loan-detail" v-if="product">
    <div class="detail-header">
      <h2>{{ product.fin_prdt_nm }}</h2>
      <div class="bank-info">
        <span class="bank-name">{{ product.kor_co_nm }}</span>
      </div>
    </div>

    <div class="detail-content">
      <div class="section">
        <h3>상품 기본 정보</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">가입방법</span>
            <span class="value">{{ product.join_way }}</span>
          </div>
          <div class="info-item">
            <span class="label">대출종류</span>
            <span class="value">{{ product.loan_type }}</span>
          </div>
          <div class="info-item">
            <span class="label">공시 시작일</span>
            <span class="value">{{ formatDate(product.dcls_strt_day) }}</span>
          </div>
        </div>
      </div>

      <div class="section">
        <h3>대출 옵션</h3>
        <div class="options-list">
          <div v-for="option in product.options" :key="option.id" class="option-card">
            <div class="option-header">
              <h4>금리 정보</h4>
            </div>
            <div class="option-content">
              <div class="info-row">
                <span class="label">금리구분</span>
                <span class="value">{{ option.lend_rate_type_nm }}</span>
              </div>
              <div class="info-row">
                <span class="label">금리범위</span>
                <span class="value">{{ option.lend_rate_min }}% ~ {{ option.lend_rate_max }}%</span>
              </div>
              <div class="info-row">
                <span class="label">대출한도</span>
                <span class="value">{{ formatAmount(option.loan_lmt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="section" v-if="product.loan_detail">
        <h3>상세 설명</h3>
        <div class="detail-text" v-html="product.loan_detail"></div>
      </div>
    </div>
  </div>
  <div v-else class="loading">
    데이터를 불러오는 중...
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoanDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      product: null,
      loading: true
    }
  },
  methods: {
    formatAmount(amount) {
      return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW'
      }).format(amount)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date)
    },
    async fetchLoanDetail() {
      this.loading = true
      try {
        const route = this.$route.name === 'mortgage-detail' ? 'mortgage' : 'lease'
        const response = await axios.get(`/api/v1/products/${route}/${this.id}/`)
        this.product = response.data
      } catch (error) {
        console.error('상품 상세 정보 조회 실패:', error)
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    this.fetchLoanDetail()
  }
}
</script>

<style scoped>
.loan-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.detail-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.detail-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.8rem;
}

.bank-info {
  margin-top: 10px;
}

.bank-name {
  color: #666;
  font-size: 1.1rem;
}

.section {
  margin-bottom: 30px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.4rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.options-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.option-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

.option-header {
  margin-bottom: 15px;
}

.option-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  font-weight: 500;
  color: #333;
}

.detail-text {
  line-height: 1.6;
  color: #444;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #666;
}
</style>
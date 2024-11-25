<!-- components/LoanCard.vue -->
<template>
  <div class="loan-card" @click="$emit('click')">
    <div class="loan-header">
      <h3>{{ product.fin_prdt_nm }}</h3>
      <span class="bank-name">{{ product.kor_co_nm }}</span>
    </div>
    
    <div class="loan-options">
      <div v-for="option in product.options" :key="option.id" class="option-item">
        <div class="rate-info">
          <span class="label">금리</span>
          <span class="value">{{ option.lend_rate_min }}% ~ {{ option.lend_rate_max }}%</span>
        </div>
        <div class="limit-info">
          <span class="label">한도</span>
          <span class="value">{{ formatAmount(option.loan_lmt) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoanCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatAmount(amount) {
      return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW'
      }).format(amount)
    }
  }
}
</script>

<style scoped>
.loan-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.loan-card:hover {
  transform: translateY(-2px);
}

.loan-header {
  margin-bottom: 16px;
}

.loan-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
}

.bank-name {
  color: #666;
  font-size: 0.9rem;
  display: block;
  margin-top: 4px;
}

.loan-options {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.option-item:last-child {
  border-bottom: none;
}

.rate-info, .limit-info {
  display: flex;
  gap: 8px;
  align-items: center;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  font-weight: 600;
  color: #333;
}
</style>
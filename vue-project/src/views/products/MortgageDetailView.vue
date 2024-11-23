<!-- views/MortgageDetailView.vue (주택담보대출 상세보기) -->
<template>
  <div v-if="loading" class="loading">
    로딩중...
  </div>
  <div v-else-if="error" class="error">
    {{ error }}
  </div>
  <div v-else-if="loan" class="loan-detail">
    <div class="loan-header">
      <h2>{{ loan.fin_prdt_nm }}</h2>
      <span class="loan-type">{{ loan.loan_type }}</span>
    </div>

    <div class="loan-info-grid">
      <div class="info-section basic-info">
        <h3>기본 정보</h3>
        <table>
          <tbody>
            <tr>
              <th>금융회사</th>
              <td>{{ loan.kor_co_nm }}</td>
            </tr>
            <tr>
              <th>대출한도</th>
              <td>{{ loan.loan_lmt }}</td>
            </tr>
            <tr>
              <th>신청방법</th>
              <td>{{ loan.join_way }}</td>
            </tr>
            <tr>
              <th>공시 시작일</th>
              <td>{{ formatDate(loan.dcls_strt_day) }}</td>
            </tr>
            <tr>
              <th>공시 종료일</th>
              <td>{{ formatDate(loan.dcls_end_day) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="info-section fees">
        <h3>부대비용 정보</h3>
        <div class="fee-details">
          <p class="label">대출부대비용</p>
          <p class="content">{{ loan.loan_inci_expn }}</p>
          <p class="label">중도상환수수료</p>
          <p class="content">{{ loan.erly_rpay_fee }}</p>
          <p class="label">연체이자율</p>
          <p class="content">{{ loan.dly_rate }}</p>
        </div>
      </div>
    </div>

    <div class="options-section">
      <h3>금리 정보</h3>
      <div class="options-grid">
        <div v-for="(group, key) in groupedOptions" :key="key" class="option-group">
          <h4>{{ getMortgageTypeLabel(key) }}</h4>
          <table>
            <thead>
              <tr>
                <th>상환방식</th>
                <th>금리유형</th>
                <th>최저금리</th>
                <th>최고금리</th>
                <th>평균금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in group" :key="`${option.rpay_type}-${option.lend_rate_type}`">
                <td>{{ option.rpay_type_nm }}</td>
                <td>{{ option.lend_rate_type_nm }}</td>
                <td>{{ option.lend_rate_min }}%</td>
                <td>{{ option.lend_rate_max }}%</td>
                <td>{{ option.lend_rate_avg ? `${option.lend_rate_avg}%` : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const loan = ref(null)
const loading = ref(true)
const error = ref(null)

const groupedOptions = computed(() => {
  if (!loan.value?.options) return {}
  return loan.value.options.reduce((acc, option) => {
    const key = option.mrtg_type
    if (!acc[key]) acc[key] = []
    // 중복 제거를 위한 키 생성
    const uniqueKey = `${option.rpay_type}-${option.lend_rate_type}`
    if (!acc[key].find(opt => 
      `${opt.rpay_type}-${opt.lend_rate_type}` === uniqueKey
    )) {
      acc[key].push(option)
    }
    return acc
  }, {})
})

const getMortgageTypeLabel = (type) => {
  const types = {
    'A': '아파트',
    'B': '주택',
    'C': '오피스텔'
  }
  return types[type] || type
}

const fetchLoanDetail = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/products/mortgage/${route.params.id}`
    })
    loan.value = {
      ...response.data,
      loan_type: '주택담보대출'
    }
  } catch (err) {
    console.error('Error fetching loan:', err)
    error.value = '대출 상품 정보를 불러오는데 실패했습니다.'
    router.push({ name: 'loan-comparison' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchLoanDetail()
})

// MortgageDetailView.vue의 script 부분에 추가
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return `${dateString.slice(0, 4)}-${dateString.slice(4, 6)}-${dateString.slice(6, 8)}`
}
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 2rem;
}

.error {
  color: red;
  text-align: center;
  padding: 2rem;
}

.loan-detail {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.loan-header {
  margin-bottom: 24px;
  border-bottom: 2px solid #333;
  padding-bottom: 16px;
}

.loan-header h2 {
  margin: 0;
  display: inline-block;
}

.loan-type {
  margin-left: 16px;
  padding: 4px 12px;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
}

.loan-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.info-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.info-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  border: 1px solid #dee2e6;
  text-align: left;
}

th {
  background: #f1f3f5;
  width: 30%;
}

.fee-details .label {
  font-weight: bold;
  margin-bottom: 4px;
  color: #495057;
}

.fee-details .content {
  margin-bottom: 16px;
  white-space: pre-line;
}

.options-grid {
  display: grid;
  gap: 24px;
  margin-top: 16px;
}

.option-group {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.option-group h4 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}
</style>

<template>
  <div class="loan-comparison">
    <div class="header-section">
      <h2>대출상품 비교</h2>
      <button class="recommendation-button" @click="goToRecommendation">
        나에게 맞는 대출 상품 찾기!
      </button>
    </div>
    <div class="filter-section">
      <loan-filter 
        @filter-change="handleFilterChange" 
        :loan-types="['주택담보대출', '전세자금대출']"
      />
    </div>

    <div v-if="loading" class="loading">데이터를 불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="comparison-section">
      <loan-comparison-table 
        :mortgage-loans="mortgageLoans"
        :lease-loans="leaseLoans"
        :filters="filters"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import LoanFilter from '@/components/loan/LoanFilter.vue'
import LoanComparisonTable from '@/components/loan/LoanComparisonTable.vue'
import { useLoanStore } from '@/stores/loan'


const router = useRouter()
const loanStore = useLoanStore()

// store의 상태를 반응형으로 가져오기
const { mortgageLoans, leaseLoans, loading, error } = storeToRefs(loanStore)

// 필터 상태 관리
const filters = ref({
  loanType: '',
  rateType: '',
  repayType: '',
  sortField: '',
  sortOrder: 'asc'
})

// 필터 변경 핸들러
const handleFilterChange = (newFilters) => {
  filters.value = {
    ...filters.value,
    ...newFilters
  }
}

// 추천 페이지 이동
const goToRecommendation = () => {
  router.push({ name: 'LoanMBTITest' })
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  await loanStore.getMortgageLoans();
  await loanStore.getLeaseLoans();
});
</script>
<style scoped>
.loan-comparison {
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: red;
  padding: 20px;
  text-align: center;
}

.comparison-section {
  margin-top: 20px;
}


.header-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.recommendation-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.recommendation-button:hover {
  background-color: #45a049;
}

</style>

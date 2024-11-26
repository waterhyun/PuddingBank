<template>
  <div class="loan-comparison">
    <!-- 필터 -->
    <div class="filter-sidebar">
      <div class="sticky-container">
        <loan-filter
          @filter-change="handleFilterChange"
          @filter-reset="resetFilters"
          :loan-types="['주택담보대출', '전세자금대출']"
        />
        <button class="recommendation-button" @click="goToRecommendation">
          나에게 맞는 대출 상품 찾기!
        </button>
      </div>
    </div>

    <!-- 콘텐츠 영역 -->
    <div class="content-section">
      <div v-if="loading" class="loading">데이터를 불러오는 중...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <loan-comparison-table
          :mortgage-loans="mortgageLoans"
          :lease-loans="mortgageLoans"
          :filters="filters"
        />
      </div>
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

// 필터 초기화 핸들러
const resetFilters = () => {
  filters.value = {
    loanType: '',
    rateType: '',
    repayType: '',
    sortField: '',
    sortOrder: 'asc'
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
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #fffefb;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filter-sidebar {
  width: 400px;
}

.sticky-container {
  position: sticky;
  top: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 양쪽 정렬 */
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-radius: 10px;
}

.recommendation-button {
  margin-top: 20px; /* 버튼 위의 여백 추가 */
  padding: 20px 50px; /* 버튼 크기 조정 */
  background-color: #73553C;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
  transition: background-color 0.2s ease;
  font-family: 'GowunDodum-Regular', sans-serif;
  font-size: 1rem;
}

.recommendation-button:hover {
  background-color: #FEF0AC;
}

.content-section {
  flex: 1;
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 1.1rem;
}

.error {
  color: red;
}

@media (max-width: 768px) {
  .loan-comparison {
    flex-direction: column;
    gap: 15px;
  }

  .filter-sidebar {
    width: 100%;
    max-width: none;
  }

  .content-section {
    width: 100%;
  }
}

</style>
<template>
  <div class="comparison-table">
    <table>
      <thead>
        <tr>
          <th>금융사</th>
          <th>상품명</th>
          <th>대출종류</th>
          <th>금리유형</th>
          <th class="sortable" @click="sortBy('minRate')">
            최저금리
            <span class="sort-icon">
              {{ getSortIcon('minRate') }}
            </span>
          </th>
          <th class="sortable" @click="sortBy('maxRate')">
            최고금리
            <span class="sort-icon">
              {{ getSortIcon('maxRate') }}
            </span>
          </th>
          <th>대출한도</th>
          <th>상세보기</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in filteredAndSortedLoans" :key="loan.uniqueId">
          <td>{{ loan.kor_co_nm }}</td>
          <td>{{ loan.fin_prdt_nm }}</td>
          <td>{{ loan.loan_type }}</td>
          <td>{{ getLoanRateType(loan) }}</td>
          <td>{{ getMinRate(loan) }}%</td>
          <td>{{ getMaxRate(loan) }}%</td>
          <td>{{ loan.loan_lmt }}</td>
          <td>
            <button @click="showDetail(loan)">상세보기</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  mortgageLoans: {
    type: Array,
    default: () => []
  },
  leaseLoans: {
    type: Array,
    default: () => []
  },
  filters: {
    type: Object,
    default: () => ({})
  }
})

const router = useRouter()
const currentSort = ref('')
const currentSortDir = ref('asc')

const combinedLoans = computed(() => {
  const mortgageWithType = props.mortgageLoans.map(loan => ({
    ...loan,
    loan_type: '주택담보대출',
    // id: loan.options[0]?.loan_id // 숫자 ID만 저장
    // 고유한 ID 생성: 대출 종류 + loan_id
    uniqueId: `mortgage_${loan.options[0]?.loan_id}`,
    // 원래 숫자 ID도 보존
    numericId: loan.options[0]?.loan_id
  }))
  const leaseWithType = props.leaseLoans.map(loan => ({
    ...loan,
    loan_type: '전세자금대출',
    // id: loan.options[0]?.loan_id // 숫자 ID만 저장
    // 고유한 ID 생성: 대출 종류 + loan_id
    uniqueId: `lease_${loan.options[0]?.loan_id}`,
    // 원래 숫자 ID도 보존
    numericId: loan.options[0]?.loan_id
  }))
  return [...mortgageWithType, ...leaseWithType]
})

const filteredAndSortedLoans = computed(() => {
  let result = [...combinedLoans.value]

  // 필터링
  if (props.filters.loanType) {
    result = result.filter(loan => loan.loan_type === props.filters.loanType)
  }

  if (props.filters.rateType) {
    result = result.filter(loan => 
      loan.options.some(opt => opt.lend_rate_type === props.filters.rateType)
    )
  }

  if (props.filters.repayType) {
    result = result.filter(loan => 
      loan.options.some(opt => opt.rpay_type === props.filters.repayType)
    )
  }

  // 정렬
  if (currentSort.value) {
    result.sort((a, b) => {
      let aValue, bValue
      
      if (currentSort.value === 'minRate') {
        // getMinRate 함수가 이미 숫자를 반환하므로 직접 사용
        aValue = Number(getMinRate(a))
        bValue = Number(getMinRate(b))
      } else if (currentSort.value === 'maxRate') {
        // getMaxRate 함수가 이미 숫자를 반환하므로 직접 사용
        aValue = Number(getMaxRate(a))
        bValue = Number(getMaxRate(b))
      }

      // NaN 처리
      if (isNaN(aValue)) return 1
      if (isNaN(bValue)) return -1
      if (isNaN(aValue) && isNaN(bValue)) return 0
      
      // 정렬 방향에 따른 비교
      let modifier = currentSortDir.value === 'asc' ? 1 : -1
      return (aValue - bValue) * modifier
    })
  }

  return result
})

const getLoanRateType = (loan) => {
  if (!loan.options || loan.options.length === 0) return '-'
  const types = new Set(loan.options.map(opt => opt.lend_rate_type))
  return Array.from(types).map(type => 
    type === 'F' ? '고정금리' : '변동금리'
  ).join(', ')
}

const getMinRate = (loan) => {
  if (!loan.options || loan.options.length === 0) return '-'
  return Math.min(...loan.options.map(opt => opt.lend_rate_min))
}

const getMaxRate = (loan) => {
  if (!loan.options || loan.options.length === 0) return '-'
  return Math.max(...loan.options.map(opt => opt.lend_rate_max))
}

// 표시용 금리 포맷팅 함수 추가
const formatRate = (rate) => {
  return typeof rate === 'number' ? rate.toFixed(2) + '%' : rate
}

const sortBy = (key) => {
  if (currentSort.value === key) {
    currentSortDir.value = currentSortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    currentSort.value = key
    currentSortDir.value = 'asc'
  }
}

const getSortIcon = (key) => {
  if (currentSort.value !== key) return '⇅'
  return currentSortDir.value === 'asc' ? '↑' : '↓'
}

const showDetail = (loan) => {
  const routeName = loan.loan_type === '주택담보대출' ? 'mortgage-detail' : 'lease-detail'
  router.push({
    name: routeName,
    params: { id: loan.numericId }
  })
}
</script>

<style scoped>
.comparison-table {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  background-color: #e9ecef;
}

.sort-icon {
  margin-left: 4px;
  font-size: 0.8em;
}

tr:hover {
  background-color: #f9f9f9;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

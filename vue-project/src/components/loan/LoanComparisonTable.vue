<template>
  <div class="comparison-table-wrapper">
    <div class="comparison-table ">
      <h1 class="table-title">대출 상품 비교</h1>
      <table>
        <thead>
          <tr>
            <th>금융사</th>
            <th>상품명</th>
            <th>대출종류</th>
            <th>금리유형</th>
            <th>
              <div class="sortable" @click="sortBy('minRate')">
                최저금리
                <span class="sort-icon">{{ getSortIcon('minRate') }}</span>
              </div>
            </th>
            <th>
              <div class="sortable" @click="sortBy('maxRate')">
                최고금리
                <span class="sort-icon">{{ getSortIcon('maxRate') }}</span>
              </div>
            </th>
            <th>대출한도</th>
            <th>상세보기</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="loan in filteredAndSortedLoans"
            :key="loan.uniqueId"
            class="clickable-row"
          >
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
/* 테이블 외곽 스타일 */
.comparison-table-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px; /* 양쪽 패딩 줄임 */
  background-color: #fef0ac63;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(134, 136, 109, 0.212);
}

/* 테이블 컨테이너 */
.comparison-table {
  width: 100%; /* 부모 요소의 전체 너비를 사용 */
  /* max-width: 1200px; 최대 너비 제한을 적절히 설정 */
  overflow-x: auto; /* 화면이 작을 경우 스크롤 가능 */
}

/* 테이블 스타일 */
table {
  width: 100%; /* 테이블이 부모 요소의 너비를 모두 사용 */
  border-collapse: collapse;
  background-color: #fff;
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 테이블 그림자 */
}

/* 테이블 제목 */
.table-title {
  font-family: "JalnanFont", sans-serif;
  font-size: 1.5rem;
  color: #3d0f0e;
  text-align: center;
  margin-bottom: 20px;
}

/* 테이블 헤더 스타일 */
thead th {
  background-color: #73553c;
  color: #fff;
  padding: 15px;
  text-align: center;
  font-family: "GowunDodum-Regular", sans-serif;
  font-size: 0.95rem;
  white-space: nowrap;
  position: relative;
  z-index: 1; /* 테이블 헤더 우선 순위 */
}


/* 테이블 헤더의 둥근 모서리 */
thead th:first-child {
  border-top-left-radius: 12px; /* 좌측 상단 둥근 모서리 */
}

thead th:last-child {
  border-top-right-radius: 12px; /* 우측 상단 둥근 모서리 */
}

/* 테이블 본문 스타일 */
tbody td {
  padding: 12px 10px;
  text-align: center;
  font-size: 0.9rem;
  font-family: "GowunDodum-Regular", sans-serif;
  color: #3D0F0E; /* 텍스트 색상 */
  border-bottom: 1px solid #dbdad6;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트를 "..."로 표시 */
}

/* 테이블 본문의 둥근 모서리 */
tbody tr:last-child td:first-child {
  border-bottom-left-radius: 12px; /* 좌측 하단 둥근 모서리 */
}

tbody tr:last-child td:last-child {
  border-bottom-right-radius: 12px; /* 우측 하단 둥근 모서리 */
}

/* 마우스 오버 효과 */
tbody tr:hover {
  background-color: #f9f9f9;
}

/* 클릭 가능한 행 스타일 */
.clickable-row {
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.clickable-row:hover {
  background-color: #fef0ac;
}

/* 정렬 가능한 헤더 */
.sortable {
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px; /* 텍스트와 아이콘 사이 간격 */
}

.sortable span.sort-icon {
  font-size: 0.8rem;
  line-height: 1;
}

/* 버튼 스타일 */
button {
  padding: 0.5rem 1rem;
  background-color: #fef0ac;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: "GowunDodum-Regular", sans-serif;
}

button:hover {
  background-color: #e0c06d;
}

</style>


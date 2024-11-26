<template>
  <div class="loan-detail-container">
    <!-- X 버튼 -->
    <div class="close-button" @click="goBack">✕</div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">로딩중...</div>

    <!-- Error State -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Loan Details -->
    <div v-else class="loan-detail">
      <!-- Header Section -->
      <div class="loan-header">
        <span class="loan-type">{{ loan.loan_type }}</span>
        <h1>{{ loan.fin_prdt_nm }}</h1>
      </div>

      <!-- Basic Information Section -->
      <h2>기본 정보</h2>
      <div class="info-section basic-info">
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

      <!-- Fee Information Section -->
      <h2>부대비용 정보</h2>
      <div class="info-section fees">
        <div class="fee-details">
          <div class="fee-item">
            <p class="label">🍨 대출부대비용</p>
            <p class="content">{{ loan.loan_inci_expn || '해당 없음' }}</p>
          </div>
          <div class="fee-item">
            <p class="label">🍭 중도상환수수료</p>
            <p class="content">{{ loan.erly_rpay_fee || '해당 없음' }}</p>
          </div>
          <div class="fee-item">
            <p class="label">🍰 연체이자율</p>
            <p class="content">{{ loan.dly_rate || '해당 없음' }}</p>
          </div>
        </div>
      </div>

      <!-- Interest Rate Options Section -->
      <div class="options-section">
        <h2>금리 정보</h2>
        <div class="option-card">
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
              <tr
                v-for="option in groupedOptions"
                :key="`${option.rpay_type}-${option.lend_rate_type}`"
              >
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
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const loan = ref(null);
const loading = ref(true);
const error = ref(null);

const goBack = () => {
  window.history.back(); // 이전 페이지로 이동
};

const groupedOptions = computed(() => {
  if (!loan.value?.options) return [];
  const uniqueOptions = new Map();

  loan.value.options.forEach((option) => {
    const key = `${option.rpay_type}-${option.lend_rate_type}`;
    if (!uniqueOptions.has(key)) {
      uniqueOptions.set(key, option);
    }
  });

  return Array.from(uniqueOptions.values());
});

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return `${dateString.slice(0, 4)}-${dateString.slice(4, 6)}-${dateString.slice(6, 8)}`;
};

const fetchLoanDetail = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/products/lease/${route.params.id}`
    );
    loan.value = {
      ...response.data,
      loan_type: '전세자금대출',
    };
  } catch (err) {
    error.value = '대출 상품 정보를 불러오는데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchLoanDetail();
});
</script>

<style scoped>
/* Common Container */
.loan-detail-container {
  max-width: 1100px;
  margin: 20px auto;
  padding: 50px;
  background-color: #fffefb;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'JalnanFont', sans-serif;
  position: relative;
}

/* X 버튼 */
.close-button {
  position: absolute;
  top: 20px; /* loan-detail-container 내부 상단에서 20px */
  right: 20px; /* loan-detail-container 내부 우측에서 20px */
  font-size: 1.5rem;
  font-weight: bold;
  color: #73553c;
  cursor: pointer;
  background-color: transparent;
  border: none;
  z-index: 1000; /* 다른 요소 위에 표시 */
  padding: 5px;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #e74c3c;
}

/* Header Section */
.loan-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #73553c;
}

.loan-header h1 {
  font-size: 2rem;
  color: #000000;
}

.loan-detail h2 {
  font-size: 1.5rem;
  color: #3d0f0e;
  margin-bottom: 16px;
  font-family: 'JalnanFont', sans-serif;
}

.loan-type {
  display: inline-block; /* 인라인 블록으로 설정 */
  font-size: 1.2rem; /* 텍스트 크기 약간 증가 */
  max-width: 350px; /* 최대 너비 확대 */
  color: #fff; /* 텍스트 색상 */
  padding: 6px 12px; /* 내부 여백 증가 */
  background-color: #73553c; /* 진한 갈색 배경 */
  border-radius: 20px; /* 둥근 버튼 스타일 */
  font-family: 'JalnanFont', sans-serif; /* 폰트 유지 */
  text-align: center; /* 텍스트 중앙 정렬 */
  letter-spacing: 2px; /* 글자 간격 설정 (1px) */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  margin-top: 10px; /* 상단 여백 추가 */
  margin-bottom: 10px; /* 하단 여백 추가 */
  word-break: keep-all; /* 단어가 깨지지 않도록 설정 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트를 '...'로 표시 */
}

/* Sections */
.info-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fffceb;
  border-color: #fec84e;
  border-radius: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.basic-info td {
  border: 1px solid #ddd;
}

.options-section {
  margin-top: 30px;
}

.option-card {
  background-color: #fff;
  border: 1px solid #73553c;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: 'GowunDodum-Regular', sans-serif;
}

.option-card h3 {
  font-size: 1.2rem;
  color: #73553c;
}


.fee-item {
  font-size: 1.2rem;
  color: #000000;
  margin-bottom: 16px;
  font-family: 'GowunDodum-Regular', sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  font-family: 'GowunDodum-Regular', sans-serif;
}

th,
td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #73553c;
  color: white;
}

th:first-child {
  width: 30%; /* 첫 번째 열 넓이 */
}

td {
  background-color: white;
}

.options-section h2 {
  font-size: 1.5rem;
  color: #3d0f0e;
  margin-bottom: 16px;
  font-family: 'JalnanFont', sans-serif;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.option-card {
  background-color: #fff;
  border: 1px solid #73553c;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: 'GowunDodum-Regular', sans-serif;
}

.option-card h3 {
  font-size: 1.2rem;
  color: #73553c;
}

.loading,
.error {
  text-align: center;
  font-size: 1.2rem;
  color: #73553c;
  padding: 20px;
}
</style>

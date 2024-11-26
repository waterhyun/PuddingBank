<template>
  <div class="loan-detail-container">
    <!-- X 버튼 -->
    <div class="close-button" @click="goBack">✕</div>

    <!-- 로딩 중 -->
    <div v-if="loading" class="loading">로딩중...</div>

    <!-- 오류 메시지 -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- 대출 상세 정보 -->
    <div v-else-if="loan" class="loan-detail">
      <!-- 상품 제목 섹션 -->
      <div class="loan-header">
        <span class="loan-type">{{ loan.loan_type }}</span> 
        <h1>{{ loan.fin_prdt_nm }}</h1>
      </div>

      <!-- 기본 정보 -->
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

      <!-- 부대비용 정보 -->
      <h2>부대비용 정보</h2>
      <div class="info-section fees">
        <div class="fee-details">
          <div class="fee-item">
            <p class="label">🍨 대출부대비용</p>
            <p class="content">{{ loan.loan_inci_expn || "해당 없음" }}</p>
          </div>
          <div class="fee-item">
            <br>
            <p class="label">🍭 중도상환수수료</p>
            <p class="content">{{ loan.erly_rpay_fee || "해당 없음" }}</p>
          </div>
          <div class="fee-item">
            <br>
            <p class="label">🍰 연체이자율</p>
            <p class="content">{{ loan.dly_rate || "해당 없음" }}</p>
          </div>
        </div>
      </div>

      <!-- 금리 옵션 -->
      <div class="options-section">
        <h2>금리 정보</h2>
        <div class="options-grid">
          <div
            v-for="(group, key) in groupedOptions"
            :key="key"
            class="option-card"
          >
            <h3>{{ getMortgageTypeLabel(key) }}</h3>
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
                  v-for="option in group"
                  :key="`${option.rpay_type}-${option.lend_rate_type}`"
                >
                  <td>{{ option.rpay_type_nm }}</td>
                  <td>{{ option.lend_rate_type_nm }}</td>
                  <td>{{ option.lend_rate_min }}%</td>
                  <td>{{ option.lend_rate_max }}%</td>
                  <td>{{ option.lend_rate_avg ? `${option.lend_rate_avg}%` : "-" }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const loan = ref(null);
const loading = ref(true);
const error = ref(null);

const goBack = () => {
  window.history.back(); // 이전 페이지로 이동
};

const groupedOptions = computed(() => {
  if (!loan.value?.options) return {};
  return loan.value.options.reduce((acc, option) => {
    const key = option.mrtg_type;
    if (!acc[key]) acc[key] = [];
    acc[key].push(option);
    return acc;
  }, {});
});

const getMortgageTypeLabel = (type) => {
  const types = {
    A: "아파트",
    B: "주택",
    C: "오피스텔",
    E: "아파트 외",
  };
  return types[type] || type;
};

const fetchLoanDetail = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/products/mortgage/${route.params.id}`
    );
    loan.value = {
      ...response.data,
      loan_type: '주택담보대출'
    }
  } catch (err) {
    error.value = "대출 정보를 불러오지 못했습니다.";
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return `${dateString.slice(0, 4)}-${dateString.slice(4, 6)}-${dateString.slice(6, 8)}`;
};

onMounted(() => {
  fetchLoanDetail();
});
</script>

<style scoped>
/* 전체 컨테이너 */
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

/* 헤더 섹션 */
.loan-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #73553c;
}

.loan-header h1 {
  font-size: 2rem;
  color: #000000;
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

.loan-detail h2 {
  font-size: 1.5rem;
  color: #3d0f0e;
  margin-bottom: 16px;
  font-family: 'JalnanFont', sans-serif;
}

.basic-info td {
  border: 1px solid #ddd;
}

/* 섹션 스타일 */
.info-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fffceb;
  border-color: #fec84e;
  border-radius: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
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
  text-align: center;
  padding: 12px;
  /* border: 1px solid #b4b2a0; */
  border-bottom: 1px solid #ddd;
  background-color: #fff;
}

th {
  background-color: #73553c;
  color: #fff;
}

th:first-child {
  width: 30%; /* 첫 번째 열 넓이 */
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

<template>
  <div class="currency-calculator">
    <h1>환율 계산기</h1>
    <p>데이터 기준 시간: <strong>{{ store.exchanges.update_date }}</strong></p>

    <div class="calculator">
      <!-- 국가 선택 -->
      <div class="input-group">
        <label for="currency-select">국가 선택 </label>
        <select v-model.trim="selectedCountry">
          <option disabled value="">국가를 선택하세요</option>
          <option v-for="exchange in sortedExchanges" 
          :key="exchange.id" 
          :value="exchange.cur_nm">
            {{ exchange.cur_nm }}
          </option>
        </select>
      </div>

      <!-- 외화 금액 -->
      <br>
      <div class="input-group">
        <label for="dollar-amount">외화 금액 입력  </label>
        <input
        type="number"
        v-model.number="dollar_amount"
        placeholder="외화를 입력해주세요."
        id="amount-input"
        min="0"
        />
        <button @click="dollarTowon()">외화를 원화로 환전하기</button>
      </div>

      <!-- 원화 금액 -->
      <br>
      <div class="input-group">
        <label for="won-amount">원화 금액 입력  </label>
        <input
          type="number"
          v-model.number.trim="won_amount"
          placeholder="원화를 입력해주세요."
          id="amount-input"
          min="0"
        />
        <button @click="wonTodollar()">원화를 외화로 환전하기</button>
      </div>


      <!-- 결과 -->
      <div v-if="result_dollar !== 0" class="exchange-result">
        <div class="card">
          <p class="country">대한민국 원화 : <strong>{{ formatNumber(won_amount) }}</strong></p>
          <div class="arrow">
            <span>▼</span>
          </div>
          <p class="country">{{ selectedCountry }} : <strong>{{ result_dollar }}</strong></p>
        </div>
      </div>

      <div v-if="result_won !== 0" class="exchange-result">
        <div class="card">
          <p class="country">{{ selectedCountry }} : <strong>{{ dollar_amount }}</strong></p>
          <div class="arrow">
            <span>▼</span>
          </div>
          <p class="country">대한민국 원화 : <strong>{{ formatNumber(result_won) }}</strong></p>
        </div>
      </div>


      <!-- 설명 -->
      <footer class="note">
        <p>* 현지, 인도네시아 루피아는 100 단위, 나머지는 모두 1 단위</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
// import { RouterLink } from 'vue-router';
// import ArticleList from '@/components/ArticleList.vue';
// import { useArticleStore } from '../stores/articles';
import { onMounted } from 'vue';
import { useExchangeStore } from '@/stores/exchanges';
import { ref, computed } from 'vue';
const selectedCountry = ref("")
const dollar_amount = ref(0)
const won_amount = ref(0)
const result_won = ref(0)
const result_dollar = ref(0)

const store = useExchangeStore()

// 서버에서 기준 시간(searchdate) 가져오기


// 가나다 순으로 정렬된 데이터를 제공하는 computed 속성
const sortedExchanges = computed(() => {
  return store.exchanges.slice().sort((a, b) => {
    return a.cur_nm.localeCompare(b.cur_nm, "ko");
  });
});

// 숫자를 천 단위 쉼표로 포맷팅하는 함수
const formatNumber = (value) => {
  if (!value) return "0";
  return new Intl.NumberFormat("ko-KR").format(value);
};

// 외화 → 원화
const dollarTowon  = function() {
  // 입력값이 없을 때 경고창 추가
  if (!selectedCountry.value && (dollar_amount.value === null || dollar_amount.value <= 0)) {
    alert("국가와 외화 금액을 모두 입력해주세요.");
    return;
  }

  if (!selectedCountry.value) {
    alert("국가를 선택해주세요.");
    return;
  }

  if (dollar_amount.value === null || dollar_amount.value <= 0) {
    alert("외화 금액을 0보다 큰 값을 입력해주세요.");
    return;
  }

  const data = store.exchanges.find((item) => item.cur_nm === selectedCountry.value);
  // 유효하지 않은 국가 선택 시 경고창 추가
  if (!data) {
    alert("선택된 국가의 데이터가 없습니다.");
    return;
  }

  if (!data) {
    console.error("선택된 국가의 데이터가 없습니다.");
    return;
  }
  
  if (data.cur_nm == '일본 옌'){
    result_won.value = dollar_amount*(data.ttb/100)
  } else {
    result_won.value = dollar_amount*(data.ttb)
  }
  result_dollar.value = 0;
}

// 원화 → 외화
const wonTodollar  = function() {
  // 입력값이 없을 때 경고창 추가
  if (!selectedCountry.value && (won_amount.value === null || won_amount.value <= 0)) {
    alert("국가와 원화 금액을 모두 입력해주세요.");
    return;
  }

  if (!selectedCountry.value) {
    alert("국가를 선택해주세요.");
    return;
  }

  if (won_amount.value === null || won_amount.value <= 0) {
    alert("원화 금액을 0보다 큰 값을 입력해주세요.");
    return;
  }


  const data = store.exchanges.find((item) => item.cur_nm === selectedCountry.value);
  // 유효하지 않은 국가 선택 시 경고창 추가
  if (!data) {
    alert("선택된 국가의 데이터가 없습니다.");
    return;
  }
  
  if (data.cur_nm == '일본 옌'){
    result_dollar.value = (won_amount/(data.tts/100)).toFixed(4)
  } else {
    result_dollar.value = (won_amount/(data.tts)).toFixed(4)
  } 
  result_won.value = 0;
}


onMounted(() => {
  store.getExchanges();
  // fetchExchangeData();
})


</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.currency-calculator {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

/* 헤더 스타일 */
.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 2rem;
  color: #007bff;
  margin: 0;
}

/* 입력 그룹 스타일 */
.input-group {
  margin: 20px 0;
}

.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 1rem;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.input-group button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.input-group button:hover {
  background-color: #0056b3;
}

/* 결과 그룹 스타일 */
.result-group {
  margin-top: 30px;
}

.exchange-result {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.exchange-result .card {
  margin: 10px 0;
}

.exchange-result .country {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 10px 0;
}

.exchange-result .arrow {
  font-size: 2rem;
  color: #007bff;
  margin: 10px 0;
}

.exchange-result strong {
  color: #007bff;
}

/* 설명 스타일 */
.note {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
  margin-top: 30px;
}
</style>
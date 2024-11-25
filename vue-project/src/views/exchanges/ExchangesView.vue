<template>
  <div class="currency-calculator">
    <h1>환율 계산기</h1>
    <p>데이터 기준 시간: <strong>{{ store.exchanges.update_date }}</strong></p>

    <div class="calculator">
      <div class="input-section">
        <!-- 국가 선택 -->
        <div class="input-group">
          <label>국가 선택</label>
          <select v-model.trim="selectedCountry">
            <option disabled value="">국가를 선택하세요</option>
            <option v-for="exchange in sortedExchanges" 
            :key="exchange.id" 
            :value="exchange.cur_nm">
              {{ exchange.cur_nm }}
            </option>
          </select>
        </div>

        <!-- 환율 입력 영역 -->
        <div class="conversion-inputs">
          <!-- 외화 금액 -->
          <div class="input-group">
            <label>외화 금액</label>
            <div class="input-wrapper">
              <input
                type="number"
                v-model.number="dollar_amount"
                placeholder="외화를 입력해주세요"
                min="0"
              />
              <span class="currency-label">{{ selectedCountry }}</span>
            </div>
          </div>

          <!-- 원화 금액 -->
          <div class="input-group">
            <label>원화 금액</label>
            <div class="input-wrapper">
              <input
                type="number"
                v-model.number.trim="won_amount"
                placeholder="원화를 입력해주세요"
                min="0"
              />
              <span class="currency-label">대한민국 원</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 결과 섹션 -->
      <div class="result-section">
        <!-- 현재 환율 정보 -->
        <div class="current-rate" v-if="selectedCountry">
          <p>현재 환율</p>
          <div class="rate-info">
            <span>1 {{ selectedCountry }} = {{ getCurrentRate() }} 원</span>
          </div>
        </div>

        <div class="exchange-result">
          <p class="result-text" v-if="won_amount">
            <span class="amount">{{ formatNumber(won_amount) }} 원</span>
            <span class="equals">=</span>
            <strong>{{ result_dollar || 0 }}</strong>
            <span class="currency">{{ selectedCountry }}</span>
          </p>
          <p class="result-text" v-else-if="dollar_amount">
            <span class="amount">{{ dollar_amount }} {{ selectedCountry }}</span>
            <span class="equals">=</span>
            <strong>{{ formatNumber(result_won || 0) }}</strong>
            <span class="currency">원</span>
          </p>
          <p class="result-text" v-else>
            <span class="amount">0 원</span>
            <span class="equals">=</span>
            <strong>0</strong>
            <span class="currency">{{ selectedCountry }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- 설명 -->
    <footer class="note">
      <p>* 현지, 인도네시아 루피아는 100 단위, 나머지는 모두 1 단위</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useExchangeStore } from '@/stores/exchange'

const store = useExchangeStore()
const selectedCountry = ref("미국 달러")
const dollar_amount = ref("")
const won_amount = ref("")
const result_won = ref(0)
const result_dollar = ref(0)

// 가나다 순으로 정렬된 데이터
const sortedExchanges = computed(() => {
  return store.exchanges.slice().sort((a, b) => {
    return a.cur_nm.localeCompare(b.cur_nm, "ko")
  })
})

// 숫자 포맷팅
const formatNumber = (value) => {
  if (!value) return "0"
  return new Intl.NumberFormat("ko-KR").format(value)
}

// 현재 환율 정보 가져오기
const getCurrentRate = () => {
  const data = store.exchanges.find((item) => item.cur_nm === selectedCountry.value)
  if (!data) return "0"
  return formatNumber(data.cur_nm === '일본 옌' ? data.tts/100 : data.tts)
}

// 외화 → 원화 변환
const dollarTowon = () => {
  if (!selectedCountry.value || !dollar_amount.value) return
  
  const data = store.exchanges.find((item) => item.cur_nm === selectedCountry.value)
  if (!data) return
  
  result_won.value = data.cur_nm === '일본 옌' 
    ? dollar_amount.value * (data.ttb/100)
    : dollar_amount.value * data.ttb
  result_dollar.value = 0
}

// 원화 → 외화 변환
const wonTodollar = () => {
  if (!selectedCountry.value || !won_amount.value) return
  
  const data = store.exchanges.find((item) => item.cur_nm === selectedCountry.value)
  if (!data) return
  
  result_dollar.value = data.cur_nm === '일본 옌'
    ? (won_amount.value/(data.tts/100)).toFixed(4)
    : (won_amount.value/data.tts).toFixed(4)
  result_won.value = 0
}

// 실시간 계산을 위한 감시자
watch([dollar_amount, selectedCountry], ([newDollarAmount, newCountry]) => {
  if (newDollarAmount) {
    dollarTowon()
    won_amount.value = ""
  }
})

watch([won_amount, selectedCountry], ([newWonAmount, newCountry]) => {
  if (newWonAmount) {
    wonTodollar()
    dollar_amount.value = ""
  }
})

onMounted(async () => {
  try {
    await store.getExchanges()
    selectedCountry.value = "미국 달러"
    console.log('Store loaded:', store.exchanges)
  } catch (error) {
    console.error('데이터 처리 중 에러 발생:', error)
  }
})
</script>

<style scoped>
.currency-calculator {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2.5rem;
  background-color: #fffefb;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(115, 85, 60, 0.15);
}

h1 {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

p {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  text-align: center;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.calculator {
  display: flex;
  gap: 2.5rem;
  margin: 0 auto;
  padding: 2rem;
  background: #FFFEFB;
  border-radius: 15px;
  border: 3px solid #FDE49B;
}


select,
input {
  width: 100%;
  padding: 0.6rem 0.8rem; /* 패딩 축소 */
  border: 2px solid #FDE49B;
  border-radius: 12px;
  font-family: 'GowunDodum-Regular';
  font-size: 0.9rem; /* 폰트 크기 축소 */
  background-color: #FFFEFB;
  color: #73553C;
  transition: all 0.2s ease;
}



.currency-label {
  position: absolute;
  right: 1rem;
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.85rem; /* 폰트 크기 축소 */
  padding: 0 0.5rem;
  background-color: #FFFEFB;
  z-index: 1;
}

.input-group label {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.9rem; /* 1rem에서 0.9rem으로 줄임 */
  font-weight: bold;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* 0.8rem에서 0.5rem으로 줄임 */
}

.conversion-inputs {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* 1.5rem에서 1rem으로 줄임 */
}

/* 입력 섹션 */
.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.input-wrapper {
  position: relative;
  background-color: transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
}




/* 결과 섹션 */
.result-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.current-rate {
  background-color: #FEF0AC;
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid #FDE49B;
  text-align: center;
}

.current-rate p {
  font-family: 'JalnanFont';
  color: #73553C;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.rate-info {
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  font-size: 1.2rem;
  font-weight: bold;
}

.exchange-result {
  flex: 1;
  background-color: #FEF0AC;
  border-radius: 12px;
  padding: 2rem;
  border: 2px solid #FDE49B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  color: #73553C;
  font-family: 'GowunDodum-Regular';
  margin: 0;
}

.result-text .amount {
  font-size: 1.2rem;
}

.result-text .equals {
  color: #73553C;
  font-size: 1.4rem;
  margin: 0.3rem 0;
}

.result-text strong {
  color: #3D0F0E;
  font-weight: bold;
  font-size: 2rem;
}

.result-text .currency {
  font-size: 1.1rem;
  color: #73553C;
}

.note p {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 0.85rem;
  text-align: center;
  margin: 0; /* margin을 0으로 초기화 */
}

.note {
  margin-top: 2rem;
  padding: 1.2rem; /* padding으로 내부 여백 통일 */
  background-color: #FEF0AC;
  border-radius: 12px;
  border: 2px solid #FDE49B;
}

input:focus,
select:focus {
  outline: none;
  border-color: #73553C;
  box-shadow: 0 0 0 3px rgba(115, 85, 60, 0.1);
}

@media (max-width: 768px) {
  .currency-calculator {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .calculator {
    flex-direction: column;
    gap: 2rem;
    padding: 1.5rem;
  }
  
  .currency-label {
    position: static;
    display: block;
    text-align: right;
    margin-top: 0.5rem;
    transform: none;
  }
  
  .input-wrapper {
    padding: 0.8rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }

  .current-rate {
    padding: 1.2rem;
  }
  
  .current-rate p {
    font-size: 1rem;
    margin-bottom: 0.8rem;
  }
  
  .rate-info {
    font-size: 1.1rem;
  }
  
  .result-text {
    font-size: 1.1rem;
  }
  
  .result-text strong {
    font-size: 1.6rem;
  }
}
</style>
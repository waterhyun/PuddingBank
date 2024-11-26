<template>
  <div class="currency-calculator">
    <h1>환율 계산기</h1>
    <div class="update-info">
      <div class="update-info-container">
        <div class="base-date">
          <p>데이터 기준 시간: <strong>{{ updateDate }}</strong></p>
        </div>
        <div class="update-status">
          <p v-if="store.lastUpdateTime">
            마지막 업데이트: {{ formatLastUpdate(store.lastUpdateTime) }}
          </p>
          <p class="update-notice">* 매일 오전 11시에 환율 정보가 갱신됩니다</p>
          <p v-if="store.isLoading" class="loading-text">데이터 업데이트 중...</p>
        </div>
      </div>
    </div>

    <div class="calculator">
      <div class="input-section">
        <div class="input-group">
          <label>국가 선택</label>
          <select v-model.trim="selectedCountry">
            <option disabled value="">국가를 선택하세요</option>
            <option 
              v-for="exchange in sortedExchanges" 
              :key="exchange.id" 
              :value="exchange.cur_nm"
            >
              {{ exchange.cur_nm }} ({{ exchange.cur_unit }})
            </option>
          </select>
        </div>

        <div class="conversion-inputs">
          <div class="input-group">
            <label>외화 금액</label>
            <div class="input-wrapper">
              <input
                type="number"
                v-model.number="dollar_amount"
                placeholder="외화를 입력해주세요"
                min="0"
                step="any"
                @input="dollarTowon"
              />
              <span class="currency-label">{{ selectedCountry }}</span>
            </div>
          </div>

          <div class="input-group">
            <label>원화 금액</label>
            <div class="input-wrapper">
              <input
                type="number"
                v-model.number.trim="won_amount"
                placeholder="원화를 입력해주세요"
                min="0"
                step="any"
                @input="wonTodollar"
              />
              <span class="currency-label">대한민국 원</span>
            </div>
          </div>
        </div>
      </div>

      <div class="result-section">
        <div class="current-rate" v-if="selectedCountry && currentRate">
          <p>현재 환율</p>
          <div class="rate-info">
            <span>1 {{ selectedCountry }} = {{ currentRate }} 원</span>
            <small v-if="selectedCountry === '일본 옌' || selectedCountry === '인도네시아 루피아'" class="unit-notice">
              (100{{ selectedCountry === '일본 옌' ? '엔' : '루피아' }} 기준)
            </small>
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

    <footer class="note">
      <p>* 일본 엔화(100엔), 인도네시아 루피아(100루피아) 기준으로 환산됩니다</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useExchangeStore } from '@/stores/exchange'

const store = useExchangeStore()
const selectedCountry = ref("미국 달러")
const dollar_amount = ref("")
const won_amount = ref("")
const result_won = ref(0)
const result_dollar = ref(0)

const UPDATE_INTERVAL = 5 * 60 * 1000 // 5분

// 날짜와 국가명으로 정렬된 환율 데이터
const sortedExchanges = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  
  const filtered = store.exchanges
    .filter(exchange => exchange.update_date.includes(today))
    .sort((a, b) => {
      // 날짜 내림차순 정렬
      const dateA = new Date(a.update_date)
      const dateB = new Date(b.update_date)
      const dateDiff = dateB - dateA
      
      // 날짜가 같으면 국가명으로 정렬
      if (dateDiff === 0) {
        return a.cur_nm.localeCompare(b.cur_nm, "ko")
      }
      return dateDiff
    })
  return filtered
})
// 최신 업데이트 날짜
const updateDate = computed(() => {
  const latestData = sortedExchanges.value[0]
  if (!latestData) return ''
  return new Date(latestData.update_date).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// 현재 선택된 통화의 환율
const currentRate = computed(() => {
  const data = sortedExchanges.value.find(item => item.cur_nm === selectedCountry.value)
  if (!data) return "0"
  return formatNumber(data.cur_nm === '일본 옌' ? data.tts/100 : data.tts)
})

const formatNumber = (value) => {
  if (!value) return "0"
  return new Intl.NumberFormat("ko-KR").format(value)
}

const formatLastUpdate = (date) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// 외화 → 원화 변환
const dollarTowon = () => {
  if (!selectedCountry.value || !dollar_amount.value) return
  
  const data = sortedExchanges.value.find(item => item.cur_nm === selectedCountry.value)
  if (!data) return
  
  result_won.value = data.cur_nm === '일본 옌' 
    ? dollar_amount.value * (data.ttb/100)
    : dollar_amount.value * data.ttb
  result_dollar.value = 0
}

// 원화 → 외화 변환
const wonTodollar = () => {
  if (!selectedCountry.value || !won_amount.value) return
  
  const data = sortedExchanges.value.find(item => item.cur_nm === selectedCountry.value)
  if (!data) return
  
  result_dollar.value = data.cur_nm === '일본 옌'
    ? (won_amount.value/(data.tts/100)).toFixed(4)
    : (won_amount.value/data.tts).toFixed(4)
  result_won.value = 0
}

// 데이터 새로고침
const refreshData = async () => {
  try {
    const now = new Date()
    const hours = now.getHours()
    
    if (hours >= 11) {
      await store.updateExchanges()
      await store.getExchanges()
    }
  } catch (error) {
    console.error('환율 데이터 갱신 실패:', error)
  }
}

// 자동 업데이트 설정
const setupAutoUpdate = () => {
  refreshData()
  
  const checkAndUpdate = () => {
    const now = new Date()
    const nextHour = new Date(now)
    nextHour.setHours(nextHour.getHours() + 1, 0, 0, 0)
    const delay = nextHour - now
    
    setTimeout(() => {
      refreshData()
      checkAndUpdate()
    }, delay)
  }
  
  checkAndUpdate()
}

// 입력값 변경 감지
watch([dollar_amount, selectedCountry], ([newDollarAmount]) => {
  if (newDollarAmount) {
    dollarTowon()
    won_amount.value = ""
  }
})

watch([won_amount, selectedCountry], ([newWonAmount]) => {
  if (newWonAmount) {
    wonTodollar()
    dollar_amount.value = ""
  }
})

// 탭 활성화 감지
const handleVisibilityChange = () => {
  if (document.visibilityState === 'visible') {
    refreshData()
  }
}

// 컴포넌트 마운트
onMounted(async () => {
  try {
    await store.getExchanges()
    selectedCountry.value = "미국 달러"
    setupAutoUpdate()
    document.addEventListener('visibilitychange', handleVisibilityChange)
  } catch (error) {
    console.error('환율 데이터 로드 실패:', error)
  }
})

// 컴포넌트 언마운트
onUnmounted(() => {
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})
</script>

<style scoped>
@font-face {
  font-family: 'JalnanFont';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_four@1.2/JalnanOTF00.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'GowunDodum-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.currency-calculator {
  max-width: 1400px;
  margin: 24px auto;
  padding: 32px;
  background-color: #fffefb;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(115, 85, 60, 0.12);
}

h1 {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 16px;
  font-size: 32px;
  line-height: 1.4;
}

p {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  text-align: center;
  font-size: 16px;
  margin-bottom: 16px;
}

.calculator {
  display: flex;
  gap: 32px;
  margin: 0 auto;
  padding: 32px;
  background: #FFFEFB;
  border-radius: 16px;
  border: 3px solid #FDE49B;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #FDE49B;
  border-radius: 12px;
  font-family: 'GowunDodum-Regular';
  font-size: 16px;
  background-color: #FFFEFB;
  color: #73553C;
  transition: all 0.2s ease;
  height: 48px;
}

select {
  width: 100%;
  padding: 12px 16px;
  padding-right: 32px; /* 오른쪽 여백 추가 */
  border: 2px solid #FDE49B;
  border-radius: 12px;
  font-family: 'GowunDodum-Regular';
  font-size: 16px;
  background-color: #FFFEFB;
  color: #73553C;
  transition: all 0.2s ease;
  height: 48px;
  appearance: none; /* 기본 화살표 제거 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2373553C' d='M6 8.825L1.175 4 2.238 2.938 6 6.7l3.763-3.762L10.825 4z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

select:focus {
  outline: none;
  border-color: #73553C;
  box-shadow: 0 0 0 3px rgba(115, 85, 60, 0.1);
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 16px;
  font-weight: 600;
}

.input-wrapper {
  position: relative;
  background-color: transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.currency-label {
  position: absolute;
  right: 16px;
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 14px;
  padding: 0 8px;
  background-color: #FFFEFB;
}

.result-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.current-rate {
  background-color: #FEF0AC;
  border-radius: 12px;
  padding: 24px;
  border: 2px solid #FDE49B;
  text-align: center;
}

.current-rate p {
  font-family: 'JalnanFont';
  color: #73553C;
  font-size: 18px;
  margin-bottom: 16px;
}

.rate-info {
  font-family: 'GowunDodum-Regular';
  color: #3D0F0E;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.exchange-result {
  flex: 1;
  background-color: #FEF0AC;
  border-radius: 12px;
  padding: 32px;
  border: 2px solid #FDE49B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  color: #73553C;
  font-family: 'GowunDodum-Regular';
  margin: 0;
  line-height: 1.4;
}

.result-text .amount {
  font-size: 20px;
}

.result-text .equals {
  color: #73553C;
  font-size: 24px;
  margin: 8px 0;
}

.result-text strong {
  color: #3D0F0E;
  font-weight: 700;
  font-size: 32px;
}

.result-text .currency {
  font-size: 18px;
  color: #73553C;
}

.note {
  margin-top: 32px;
  padding: 16px;
  background-color: #FEF0AC;
  border-radius: 12px;
  border: 2px solid #FDE49B;
}

.note p {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  font-size: 14px;
  text-align: center;
  margin: 0;
}

input:focus {
  outline: none;
  border-color: #73553C;
  box-shadow: 0 0 0 3px rgba(115, 85, 60, 0.1);
}

.update-info-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;  /* 변경: center에서 flex-end로 */
  padding: 16px;
  padding-bottom: 0px;
  background: #FFFEFB;
  border-radius: 8px;
}

.base-date {
  font-family: 'GowunDodum-Regular';
  color: #73553C;
  display: flex;
  align-items: flex-start;
  line-height: 1.4;
  text-align: left;
}

.update-status {
  text-align: right;
  color: #73553C;
  display: flex;
  flex-direction: column;
  gap: 4px;
  line-height: 1.4;
  text-align: right;
  margin-bottom: 10px;
}

.update-status p {
  margin: 0;
  text-align: right;
}

.update-notice {
  font-size: 0.9em;
  opacity: 0.8;
  text-align: right;
}

.loading-text {
  color: #FDE49B;
  font-weight: bold;
}



@media (max-width: 1440px) {
  .currency-calculator {
    margin: 16px;
    padding: 24px;
  }
  
  .calculator {
    padding: 24px;
    gap: 24px;
  }

  h1 {
    font-size: 28px;
  }

  .current-rate,
  .exchange-result {
    padding: 20px;
  }
}

@media (max-width: 1024px) {
  .currency-calculator {
    margin: 12px;
    padding: 20px;
  }

  .calculator {
    padding: 20px;
    gap: 20px;
  }

  .input-section,
  .result-section {
    gap: 20px;
  }

  .rate-info {
    font-size: 18px;
  }

  .result-text strong {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .calculator {
    flex-direction: column;
    gap: 24px;
  }

  .input-section,
  .result-section {
    width: 100%;
  }

  .input-wrapper {
    flex-direction: column;
  }

  .currency-label {
    position: static;
    text-align: right;
    margin-top: 8px;
    padding: 4px 0;
  }

  .current-rate,
  .exchange-result {
    padding: 16px;
  }

  .result-text {
    font-size: 16px;
  }

  .result-text strong {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .currency-calculator {
    margin: 8px;
    padding: 16px;
    border-radius: 16px;
  }

  h1 {
    font-size: 22px;
    margin-bottom: 12px;
  }

  p {
    font-size: 14px;
    margin-bottom: 24px;
  }

  .calculator {
    padding: 16px;
    gap: 16px;
  }

  .input-section,
  .result-section {
    gap: 16px;
  }

  .input-group {
    gap: 6px;
  }

  .input-group label {
    font-size: 14px;
  }

  input,
  select {
    height: 42px;
    font-size: 14px;
    padding: 10px 14px;
  }

  .currency-label {
    font-size: 12px;
  }

  .current-rate {
    padding: 14px;
  }

  .current-rate p {
    font-size: 16px;
    margin-bottom: 12px;
  }

  .rate-info {
    font-size: 16px;
  }

  .exchange-result {
    padding: 16px;
  }

  .result-text {
    font-size: 14px;
  }

  .result-text .amount {
    font-size: 16px;
  }

  .result-text .equals {
    font-size: 20px;
    margin: 6px 0;
  }

  .result-text strong {
    font-size: 22px;
  }

  .result-text .currency {
    font-size: 14px;
  }

  .note {
    margin-top: 24px;
    padding: 12px;
  }

  .note p {
    font-size: 12px;
  }
}

@media (max-width: 360px) {
  .currency-calculator {
    margin: 6px;
    padding: 12px;
  }

  h1 {
    font-size: 20px;
  }

  .calculator {
    padding: 12px;
    gap: 12px;
  }

  input,
  select {
    height: 38px;
    font-size: 13px;
  }

  .result-text strong {
    font-size: 20px;
  }
}
</style>

<!-- views/loans/LoanMBTITestView.vue -->
<template>
  <div class="mbti-test">
    <!-- 진행 상태 표시 -->
    <div class="progress-bar">
      <div class="progress" :style="{ width: `${(currentStep/totalSteps)*100}%` }"></div>
      <span>{{ currentStep }}/{{ totalSteps }}</span>
    </div>

    <!-- 질문 섹션 -->
    <div v-if="!isCompleted" class="question-section">
      <div class="questions-container">
        <transition name="fade" mode="out-in">
          <div :key="currentStep" class="question-group">
            <template v-for="(question, index) in currentQuestions" :key="index">
              <div class="question-item">
                <h3>{{ question }}</h3>
                <div class="answer-buttons">
                  <button
                    v-for="(label, value) in answerOptions"
                    :key="value"
                    :class="{ selected: isAnswerSelected(getCurrentQuestionId(index), value) }"
                    @click="selectAnswer(getCurrentQuestionId(index), parseInt(value))"
                  >
                    {{ label }}
                  </button>
                </div>
              </div>
            </template>
          </div>
        </transition>
      </div>

      <!-- 네비게이션 버튼 -->
      <div class="navigation-buttons">
        <button 
          class="nav-button prev" 
          @click="previousStep" 
          v-if="currentStep > 1"
          :disabled="isLoading"
        >
          이전
        </button>
        <button 
          class="nav-button next" 
          @click="nextStep"
          v-if="!isLastStep"
          :disabled="!canProceed || isLoading"
        >
          다음
        </button>
        <button 
          class="nav-button submit"
          @click="submitTest"
          v-if="isLastStep"
          :disabled="!canProceed || isLoading"
        >
          결과 보기
        </button>
      </div>
    </div>

    <!-- 로딩 인디케이터 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>결과를 분석중입니다...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="showError" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useLoanStore } from '@/stores/loan'

export default {
  name: 'LoanMBTITest',
  
  data() {
    return {
      currentStep: 1,
      totalSteps: 4,
      answers: {},
      isLoading: false,
      isCompleted: false,
      errorMessage: '',
      showError: false,
      answerOptions: {
        1: '동의하지 않음',
        2: '보통',
        3: '동의함'
      },
      questionSets: {
        initial: [
          "내 소유의 집을 마련하는 것이 목표이다",
          "당장 거주할 집이 필요한 상황이다",
          "전세 보증금 마련이 우선이다"
        ],
        fv: [
          "금리가 변동될 수 있다는 생각만으로도 불안하다",
          "원금이 조금 더 들더라도 고정금리가 좋다",
          "시장 금리가 떨어질 수 있는 기회는 포기하고 싶지 않다"
        ],
        pd: [
          "매달 고정적으로 갚아나가는 것이 편하다",
          "대출 상환 계획은 처음부터 명확히 세우고 싶다",
          "목돈이 생기면 수시로 상환하고 싶다"
        ],
        ah: [
          "아파트의 안정성이 가장 중요하다",
          "관리비를 내더라도 체계적인 관리가 필요하다",
          "단독주택이나 상가의 투자가치가 더 매력적이다"
        ],
        ts: [
          "2년 이상 한 곳에 거주할 계획이다",
          "주거비용의 안정성이 가장 중요하다",
          "필요하면 언제든 이사할 수 있어야 한다"
        ],
        gp: [
          "보증료를 내더라도 안전한 상품이 좋다",
          "정부 지원 상품을 이용하고 싶다",
          "절차가 복잡해도 안전한게 중요하다"
        ]
      }
    }
  },

  computed: {
    isLastStep() {
      return this.currentStep === this.totalSteps;
    },
    
    currentQuestions() {
      return this.questionSets[this.currentQuestionType] || [];
    },
    
    currentQuestionType() {
      if (this.currentStep === 1) return 'initial';
      if (this.currentStep === 2) return 'fv';
      
      const mortgageScore = this.answers['initial_q1'] || 0;
      const leaseScore = this.answers['initial_q3'] || 0;
      
      if (mortgageScore > leaseScore) {
        return this.currentStep === 3 ? 'pd' : 'ah';
      } else {
        return this.currentStep === 3 ? 'ts' : 'gp';
      }
    },
    
    canProceed() {
      return this.isValidAnswers && this.getCurrentStepQuestions().every(
        (_, index) => this.answers[this.getCurrentQuestionId(index)]
      );
    },

    isValidAnswers() {
      const requiredQuestions = this.getCurrentStepQuestions();
      return requiredQuestions.every((_, index) => {
        const questionId = this.getCurrentQuestionId(index);
        const answer = this.answers[questionId];
        return Number.isInteger(answer) && answer >= 1 && answer <= 3;
      });
    }
  },

  methods: {
    getCurrentStepQuestions() {
      return this.questionSets[this.currentQuestionType] || [];
    },

    getCurrentQuestionId(index) {
      return `${this.currentQuestionType}_q${index + 1}`;
    },

    isAnswerSelected(questionId, value) {
      return this.answers[questionId] === parseInt(value);
    },

    selectAnswer(questionId, value) {
      this.answers[questionId] = parseInt(value);
    },

    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    nextStep() {
      if (this.canProceed && this.currentStep < this.totalSteps) {
        this.currentStep++;
      }
    },

    formatAnswersForSubmission() {
      const formattedAnswers = {};
      Object.entries(this.answers).forEach(([key, value]) => {
        formattedAnswers[key] = Math.min(Math.max(parseInt(value), 1), 3);
      });
      return formattedAnswers;
    },

    getCsrfToken() {
      return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    },

    async submitTest() {
      if (!this.canProceed || this.isLoading) return;
      this.isLoading = true;
      this.showError = false;

      try {
        console.log(this.formatAnswersForSubmission())
        const response = await axios.post('/api/v1/products/mbti/recommendation/', {
          answers: this.formatAnswersForSubmission()
        }, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken()
          }
        });

        const store = useLoanStore()
        store.setLoanResult(response.data)
        console.log(response.data)
        this.$router.push({ name: 'LoanMBTIResult' })
      } catch (error) {
        this.handleError(error);
      } finally {
        this.isLoading = false;
      }
    },

    handleError(error) {
      let message = '오류가 발생했습니다.';
      
      if (error.response) {
        const { data, status } = error.response;
        if (status === 400) {
          message = data.message || '입력값이 올바르지 않습니다.';
        } else if (status === 401) {
          message = '로그인이 필요합니다.';
        }
      }
      
      this.errorMessage = message;
      this.showError = true;
    }
  }
}
</script>

<style scoped>
.mbti-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.progress-bar {
  position: relative;
  height: 10px;
  background: #eee;
  border-radius: 5px;
  margin-bottom: 30px;
}

.progress {
  position: absolute;
  height: 100%;
  background: #4CAF50;
  border-radius: 5px;
  transition: width 0.3s ease;
}

.question-section {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.question-item {
  margin-bottom: 30px;
}

.answer-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.answer-buttons button {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.answer-buttons button.selected {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.nav-button {
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  margin-top: 10px;
  padding: 10px;
  background: #ffebee;
  border-radius: 4px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>

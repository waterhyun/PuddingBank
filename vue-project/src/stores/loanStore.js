// stores/loanStore.js
import { defineStore } from 'pinia'

export const useLoanStore = defineStore('loan', {
  state: () => ({
    mbtiResult: null,
    recommendations: null
  }),
  
  actions: {
    setLoanResult(data) {
      this.mbtiResult = data.mbti_result
      this.recommendations = data.recommendations
    }
  }
})

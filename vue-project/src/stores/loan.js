// export const useLoanStore = defineStore('loan', {
//   state: () => ({
//     mbtiResult: null,
//     recommendations: null
//   }),
  
//   actions: {
//     setLoanResult(data) {
//       this.mbtiResult = data.mbti_result
//       this.recommendations = data.recommendations
//     }
//   }
// })
import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useLoanStore = defineStore('loan', () => {
  // state
  const mbtiResult = ref(null)
  const recommendations = ref(null)
  const mortgageLoans = ref([])
  const leaseLoans = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    loanType: '',
    minRate: null,
    maxRate: null
  })

  // actions
  const setLoanResult = (data) => {
    mbtiResult.value = data.mbti_result
    recommendations.value = data.recommendations
  }

  const getMortgageLoans = async () => {
    loading.value = true
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/products/mortgage/'
      })
      mortgageLoans.value = response.data
    } catch (err) {
      error.value = err
      console.error('주택담보대출 정보 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }
  
  const getLeaseLoans = async () => {
    loading.value = true
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/products/lease/'
      })
      leaseLoans.value = response.data
    } catch (err) {
      error.value = err
      console.error('전세자금대출 정보 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }
    

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  // getters
  const filteredMortgageLoans = computed(() => {
    return mortgageLoans.value.filter(loan => {
      if (filters.value.loanType && filters.value.loanType !== '주택담보대출') return false
      if (filters.value.minRate && Math.min(...loan.options.map(opt => opt.lend_rate_min)) < filters.value.minRate) return false
      if (filters.value.maxRate && Math.max(...loan.options.map(opt => opt.lend_rate_max)) > filters.value.maxRate) return false
      return true
    })
  })
  
  const filteredLeaseLoans = computed(() => {
    return leaseLoans.value.filter(loan => {
      if (filters.value.loanType && filters.value.loanType !== '전세자금대출') return false
      if (filters.value.minRate && Math.min(...loan.options.map(opt => opt.lend_rate_min)) < filters.value.minRate) return false
      if (filters.value.maxRate && Math.max(...loan.options.map(opt => opt.lend_rate_max)) > filters.value.maxRate) return false
      return true
    })
  })

  return {
    // state
    mbtiResult,
    recommendations,
    mortgageLoans,
    leaseLoans,
    loading,
    error,
    filters,
    // actions
    setLoanResult,
    getMortgageLoans,
    getLeaseLoans,
    updateFilters,
    // getters
    filteredMortgageLoans,
    filteredLeaseLoans
  }
})

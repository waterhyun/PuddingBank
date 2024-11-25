<!-- LoanProductsView.vue -->
<template>
  <div class="loan-products">
    <div class="tab-buttons">
      <button 
        :class="{ active: activeTab === 'mortgage' }"
        @click="activeTab = 'mortgage'"
      >
        주택담보대출
      </button>
      <button 
        :class="{ active: activeTab === 'lease' }"
        @click="activeTab = 'lease'"
      >
        전세자금대출
      </button>
    </div>

    <div class="product-list">
      <loan-card
        v-for="product in displayProducts"
        :key="product.fin_prdt_cd"
        :product="product"
        @click="showDetail(product)"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LoanCard from './components/LoanCard.vue'

export default {
  name: 'LoanProducts',
  components: {
    LoanCard
  },
  data() {
    return {
      mortgageLoans: [],
      leaseLoans: [],
      activeTab: 'mortgage',
      loading: false
    }
  },
  computed: {
    displayProducts() {
      return this.activeTab === 'mortgage' ? this.mortgageLoans : this.leaseLoans
    }
  },
  methods: {
    async fetchLoans() {
      this.loading = true
      try {
        const [mortgageResponse, leaseResponse] = await Promise.all([
          axios.get('/api/v1/products/mortgage/'),  // v1 추가
          axios.get('/api/v1/products/lease/')      // v1 추가
        ])
        this.mortgageLoans = mortgageResponse.data
        this.leaseLoans = leaseResponse.data
      } catch (error) {
        console.error('대출 상품 조회 실패:', error)
      } finally {
        this.loading = false
      }
    },
    showDetail(product) {
      const route = this.activeTab === 'mortgage' ? 'mortgage' : 'lease'
      this.$router.push(`/api/v1/products/${route}/${product.fin_prdt_cd}/`)
    }
  },
  created() {
    this.fetchLoans()
  }
}
</script>
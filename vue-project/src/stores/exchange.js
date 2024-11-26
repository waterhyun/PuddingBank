// import axios from 'axios'
// import { ref, computed } from 'vue'
// import { defineStore } from 'pinia'
// // import { useRouter } from 'vue-router'

// export const useExchangeStore = defineStore('exchanges', () => {
//   const exchanges = ref([])
//   // const router = useRouter()
//   const getExchanges = function () {
//     axios({
//       method: 'get',
//       url: 'http://127.0.0.1:8000/api/v1/exchanges/'
//     })
//     .then(res => {
//       // console.log(res.data)
//       exchanges.value = res.data
//     })
//   }

//   const postExchanges = function () {
//     axios({
//       method: 'post',
//       url: 'http://127.0.0.1:8000/api/v1/exchanges/'
//     })
//     .then(res => {
//       console.log('POST 성공:', res.data);
//     })
//   }

//   return { exchanges, getExchanges, postExchanges }
// })

import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useExchangeStore = defineStore('exchanges', () => {
  const exchanges = ref([])
  const isLoading = ref(false)
  const lastUpdateTime = ref(null)

  const getExchanges = async function () {
    try {
      isLoading.value = true
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/exchanges/'
      })
      exchanges.value = response.data
      lastUpdateTime.value = new Date()
    } catch (error) {
      console.error('환율 데이터 조회 실패:', error)
    } finally {
      isLoading.value = false
    }
  }

  const updateExchanges = async function () {
    try {
      const response = await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/v1/exchanges/'
      })
      console.log('환율 데이터 업데이트 성공:', response.data)
      // 업데이트 후 새로운 데이터 조회
      await getExchanges()
    } catch (error) {
      console.error('환율 데이터 업데이트 실패:', error)
    }
  }

  // 자동 업데이트 설정 (매 시간마다)
  const startAutoUpdate = () => {
    // 초기 데이터 로드
    updateExchanges()
    
    // 매 시간마다 업데이트
    setInterval(() => {
      const now = new Date()
      // 오전 11시 이전에만 업데이트 실행 (API 스펙에 맞춤)
      if (now.getHours() < 11) {
        updateExchanges()
      }
    }, 3600000) // 1시간(3600000ms) 간격
  }

  return { 
    exchanges, 
    isLoading, 
    lastUpdateTime, 
    getExchanges, 
    updateExchanges,
    startAutoUpdate 
  }
})

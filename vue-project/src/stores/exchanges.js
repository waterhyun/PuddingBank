import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
// import { useRouter } from 'vue-router'

export const useExchangeStore = defineStore('exchanges', () => {
  const exchanges = ref([])
  // const router = useRouter()
  const getExchanges = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/exchanges/'
    })
    .then(res => {
      // console.log(res.data)
      exchanges.value = res.data
    })
  }

  return { exchanges, getExchanges }
})
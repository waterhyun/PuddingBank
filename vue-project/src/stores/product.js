import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useProductStore = defineStore('product', () => {
  const depositproducts = ref([])
  const depositproduct = ref([])
  const savingproducts = ref([])
  const savingproduct = ref([])
  const router = useRouter()

  // 전체 예금 상품 조회
  const getDepositProducts = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/products/deposits/'
    })
    .then(res => {
      console.log(res.data)
      depositproducts.value = res.data
    })
    .catch((err) => {
      console.error('API 요청 실패:', err); // 오류 메시지 출력
    });
  }

  // 단일 예금 상품 조회
  const getDepositProduct = function(product_id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/products/deposits/${product_id}/`,
    }).then(res => {
      depositproduct.value = res.data;
    })
  }

  // 전체 적금 상품 조회
  const getSavingProducts = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/products/savings/'
    })
    .then(res => {
      // console.log(res.data)
      savingproducts.value = res.data
    })
    .catch((err) => {
      console.error('API 요청 실패:', err); // 오류 메시지 출력
    });
  }

  // 단일 적금 상품 조회
  const getSavingProduct = function(product_id) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/products/savings/${product_id}/`,
    }).then(res => {
      savingproduct.value = res.data;
    })
  }


  return { depositproducts, depositproduct, getDepositProducts, getDepositProduct,
           savingproducts, savingproduct, getSavingProducts, getSavingProduct
   }
})
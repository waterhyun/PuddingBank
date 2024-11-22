<template>
  <div class="product-detail">
    <h1 class="detail-title">{{ type === "saving" ? "적금 상세 정보" : "예금 상세 정보" }}</h1>
    <div class="detail-container">
      <!-- 기본 정보 섹션 -->
      <div class="basic-info">
        <p><strong>상품명:</strong> {{ product?.fin_prdt_nm }}</p>
        <p><strong>은행명:</strong> {{ product?.kor_co_nm }}</p>
        <p><strong>특이사항:</strong> {{ product?.etc_note || "없음" }}</p>
      </div>

      <!-- 찜하기 버튼 -->
      <div class="wishlist-actions">
        <i
          class="fas fa-heart wishlist-icon"
          :class="{ added: isWishlisted }"
          @click="toggleWishlist"
        ></i>
      </div>
      <!-- 찜하기 버튼 끝 -->

      <!-- 옵션 정보 섹션 -->
      <div class="options-info">
        <h2>상품 옵션</h2>
        <table>
          <thead>
            <tr>
              <th>기간(개월)</th>
              <th>기본 금리(%)</th>
              <th>우대 금리(%)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="option in product?.options || []" :key="option.save_trm">
              <td>{{ option.save_trm }}</td>
              <td>{{ option.intr_rate }}</td>
              <td>{{ option.intr_rate2 || "-" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, computed } from "vue";
import { useProductStore } from "@/stores/product";
import axios from "axios"; 
import { useAuthStore } from "@/stores/auth";

const authstore = useAuthStore()
const route = useRoute();
const type = route.params.type; // 상품 유형 ("saving" 또는 "deposit")
const id = parseInt(route.params.id); // 상품 ID
const isWishlisted = ref(false); // 찜 여부 상태
const store = useProductStore();


// 상품 데이터 가져오기
onMounted(() => {
  if (type === "saving") {
    store.getSavingProduct(id); // 적금 상품 데이터 로드
  } else {
    store.getDepositProduct(id); // 예금 상품 데이터 로드
  }

  // 초기 찜 상태 확인
  checkWishlistStatus();
});

// 컴퓨티드 속성으로 스토어에서 데이터 가져오기
const product = computed(() => {
  return type === "saving" ? store.savingproduct : store.depositproduct;
});

// 찜 상태 확인 함수
async function checkWishlistStatus() {
  try {
    const response = await axios.get(`/products/wishlist/status/${type}/${id}/`);
    isWishlisted.value = response.data.is_wishlisted;
  } catch (error) {
    console.error("찜 상태 확인 중 오류 발생:", error);
  }
}

const func_name = function () {
  axios({
    method: 'post',
    url: '/products/wishlist/remove/${type}/${id}/',
    headers: {
      Authorization: `Token ${authstore.token}`
    }
  })
    .then((res) => {
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 찜하기/취소 토글 함수
async function toggleWishlist() {
  try {
    if (isWishlisted.value) {
      // 찜 취소 요청
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/api/v1/products/wishlist/remove/${type}/${id}/`,
        headers: {
          Authorization: `Token ${authstore.token}`
        }
      })
        .then((res) => {
          console.log(res)
        })
        .catch((err) => {
          console.log(err)
        })
      isWishlisted.value = false;
    } else {
      // 찜 추가 요청
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/api/v1/products/wishlist/add/${type}/${id}/`,
        headers: {
          Authorization: `Token ${authstore.token}`
        }
      })
        .then((res) => {
          console.log(res)
        })
        .catch((err) => {
          console.log(err)
        })
      isWishlisted.value = true;
    }
  } catch (error) {
    console.log("type:", type); // saving 또는 deposit이어야 함
    console.log("id:", id);     // 상품 ID
    console.error("찜 상태 변경 중 오류 발생:", error);
  }
}
</script>

<style scoped>
.product-detail {
  margin: 20px auto;
  padding: 20px;
  max-width: 800px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.detail-title {
  text-align: center;
  font-size: 1.8rem;
  color: #0046b3;
  margin-bottom: 20px;
}

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 기본 정보 섹션 */
.basic-info p {
  font-size: 1rem;
  color: #333;
  margin: 5px 0;
}

.basic-info strong {
  color: #0046b3;
}

/* 옵션 정보 섹션 */
.options-info {
  margin-top: 20px;
}

.options-info h2 {
  font-size: 1.5rem;
  color: #0046b3;
  margin-bottom: 10px;
}

/* 테이블 스타일 */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 5px;
  overflow: hidden;
}

thead {
  background-color: #0046b3;
  color: #fff;
}

th,
td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  font-size: 0.9rem;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

/* 찜하기 버튼 스타일 */
.wishlist-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.wishlist-icon {
  font-size: 2.5rem; /* 하트 크기 */
  color: #ccc; /* 기본 하트 색상 */
  cursor: pointer;
  transition: color 0.3s ease;
}

.wishlist-icon.added {
  color: #e74c3c; /* 찜한 상태에서의 빨간색 하트 */
}

</style>
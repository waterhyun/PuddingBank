<template>
  <div class="product-detail-view">
    <!-- X 버튼 -->
    <div class="close-button" @click="goBack">✕</div>

    <!-- 예금/적금 상세 정보 -->
    <div class="product-header">
      <h5 class="product-type">{{ type === "saving" ? "적금 상품" : "예금 상품" }}</h5>
      <h1 class="product-name">{{ product?.fin_prdt_nm }}</h1>
    </div>
    <br>
    <h2>기본 정보</h2>
    <div class="filter-sidebar">
      <div class="basic-info">
        <p><strong>은행명</strong></p>
        <div class="detail-content">{{ product?.kor_co_nm }}</div>
        <br>
        <p><strong>특이사항</strong></p>
        <div class="detail-content">{{ product?.etc_note || "없음" }}</div>
      </div>

      <!-- 찜하기 버튼 -->
      <div class="wishlist-actions">
        <i
          class="fas fa-heart wishlist-icon"
          :class="{ added: isWishlisted }"
          @click="toggleWishlist"
        ></i>
        <p>찜하기</p>
      </div>
    </div>
    <br>
    <!-- 상품 옵션 정보 -->
    <h2>상품 옵션</h2>
    <div class="options-container">
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
</template>

<script setup>
import { useRoute } from "vue-router";
import { ref, onMounted, computed } from "vue";
import { useProductStore } from "@/stores/product";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const authstore = useAuthStore();
const route = useRoute();
const type = route.params.type;
const id = parseInt(route.params.id);
const isWishlisted = ref(false);
const store = useProductStore();

const goBack = () => {
  window.history.back(); // 이전 페이지로 이동
};

onMounted(() => {
  if (type === "saving") {
    store.getSavingProduct(id);
  } else {
    store.getDepositProduct(id);
  }
  checkWishlistStatus();
});

const product = computed(() => {
  return type === "saving" ? store.savingproduct : store.depositproduct;
});

async function checkWishlistStatus() {
  try {
    const response = await axios.get(`/products/wishlist/status/${type}/${id}/`);
    isWishlisted.value = response.data.is_wishlisted;
  } catch (error) {
    console.error("찜 상태 확인 중 오류 발생:", error);
  }
}

async function toggleWishlist() {
  try {
    if (isWishlisted.value) {
      await axios.delete(
        `http://127.0.0.1:8000/api/v1/products/wishlist/remove/${type}/${id}/`,
        { headers: { Authorization: `Token ${authstore.token}` } }
      );
      isWishlisted.value = false;
    } else {
      await axios.post(
        `http://127.0.0.1:8000/api/v1/products/wishlist/add/${type}/${id}/`,
        {},
        { headers: { Authorization: `Token ${authstore.token}` } }
      );
      isWishlisted.value = true;
    }
  } catch (error) {
    console.error("찜 상태 변경 중 오류 발생:", error);
  }
}
</script>

<style scoped>
/* 전체 컨테이너 */
.product-detail-view {
  position: relative;
  max-width: 1100px;
  margin: 20px auto;
  padding: 50px;
  background-color: #fffefb;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: "JalnanFont", sans-serif;
}


/* X 버튼 */
.close-button {
  position: absolute;
  top: 20px;
  right: 20px; 
  font-size: 1.5rem;
  font-weight: bold;
  color: #73553c;
  cursor: pointer;
  background-color: transparent;
  border: none;
  z-index: 1000; /* 다른 요소 위에 표시 */
  padding: 5px;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #e74c3c;
}


/* 헤더 섹션 */
.product-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #73553c;
}

.product-header h1 {
  font-size: 2rem;
  color: #000000;
}

/* 상품 정보 섹션 */
.filter-sidebar {
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fffceb;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative; 
}

.product-type {
  display: inline-block; /* 인라인 블록으로 설정 */
  font-size: 1.2rem; /* 텍스트 크기 약간 증가 */
  max-width: 350px; /* 최대 너비 확대 */
  color: #fff; /* 텍스트 색상 */
  padding: 6px 12px; /* 내부 여백 증가 */
  background-color: #73553c; /* 진한 갈색 배경 */
  border-radius: 20px; /* 둥근 버튼 스타일 */
  font-family: 'JalnanFont', sans-serif; /* 폰트 유지 */
  text-align: center; /* 텍스트 중앙 정렬 */
  letter-spacing: 2px; /* 글자 간격 설정 (1px) */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  margin-top: 10px; /* 상단 여백 추가 */
  margin-bottom: 10px; /* 하단 여백 추가 */
  word-break: keep-all; /* 단어가 깨지지 않도록 설정 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트를 '...'로 표시 */
}

.product-name {
  font-size: 1.5rem;
  color: #3d0f0e;
  margin-bottom: 20px;
}

.product-detail-view h2 {
  font-size: 1.5rem;
  color: #3d0f0e;
  margin-bottom: 16px;
  font-family: 'JalnanFont', sans-serif;
}

.basic-info p {
  margin: 10px 0;
  font-size: 1.3rem;
  color: #3d0f0e;
}

.detail-content {
  font-family: "GowunDodum-Regular", sans-serif;
  color: #000000;
  font-size: 1.3rem;
}

/* 찜하기 버튼 */
.wishlist-actions {
  position: absolute; /* 부모 컨테이너 기준으로 절대 위치 */
  top: 20px; /* 상단에서 20px */
  right: 20px; /* 오른쪽에서 20px */
  text-align: center;
}

.wishlist-icon {
  font-size: 1.8rem;
  color: #ddd;
  cursor: pointer;
  transition: color 0.3s;
  padding: 10px;
}

.wishlist-icon.added {
  color: #e74c3c;
}

.wishlist-actions p {
  margin: 5px 0;
  font-size: 1rem;
  color: #73553c;
}

/* 상품 옵션 섹션 */
.options-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #73553c;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  background-color: #73553c;
  color: white;
  padding: 10px;
  font-family: "GowunDodum-Regular", sans-serif;
}

tbody td {
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  font-family: "GowunDodum-Regular", sans-serif;
}

tbody tr:hover {
  background-color: #fef0ac;
}

/* 반응형 */
@media (max-width: 768px) {
  .product-detail-view {
    padding: 15px;
  }
  .filter-sidebar,
  .options-container {
    padding: 15px;
  }
  table {
    font-size: 0.9rem;
  }
}
</style>

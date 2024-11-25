<template>
  <div class="product-detail-view">
    <!-- 예금/적금 상세 정보 -->
    <div class="filter-sidebar">
      <h5>{{ type === "saving" ? "적금 상품" : "예금 상품" }}</h5>
      <h3> {{ product?.fin_prdt_nm }} </h3>
      <div class="basic-info">
        <!-- <p><strong>상품명:</strong> {{ product?.fin_prdt_nm }}</p> -->
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
        <p>찜하기</p>
      </div>
    </div>

    <!-- 상품 옵션 정보 -->
    <div class="options-container">
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
/* 전체 레이아웃 */
.product-detail-view {
  display: flex;
  flex-direction: column; /* 위아래 배치 */
  gap: 20px;
  padding: 20px;
  width: 100%; /* 전체 화면에 맞추기 */
  box-sizing: border-box; /* 여백 포함 */
  margin: 0 auto; /* 중앙 정렬 */
  background-color: #fff7f0; /* 푸딩-1 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-x: hidden; /* 가로로 콘텐츠가 넘치지 않도록 설정 */
}

/* 상세 정보(상단) */
.filter-sidebar {
  padding: 15px;
  width: 100%; /* 기본적으로 전체 너비 사용 */
  max-width: 900px; /* 최대 너비 제한 */
  margin: 0 auto; /* 중앙 정렬 */
  background-color: #FEF0AC; /* 푸딩-2 */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  position: relative;
}

/* 상세 정보 제목 */
.filter-sidebar h5 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1rem; /* 크기를 조금 키움 */
  color: #73553C; /* 푸딩-3 */
  margin-bottom: 15px;
}

/* 상품명 */
.filter-sidebar h3 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.5 rem; /* 크기를 조금 키움 */
  color: #3D0F0E; /* 푸딩-3 */
  margin-bottom: 15px;
}


/* 상세 정보 텍스트 */
.filter-sidebar p {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1rem; /* 텍스트 크기 확대 */
  color: #3D0F0E; /* 푸딩-5 */
  margin-bottom: 15px;
}

/* 찜하기 버튼 */
.wishlist-actions {
  position: absolute; /* 부모 요소(filter-sidebar)를 기준으로 위치 설정 */
  bottom: 15px; /* 아래에서 15px 떨어짐 */
  right: 15px; /* 오른쪽에서 15px 떨어짐 */
  display: flex;
  align-items: center; /* 세로 중앙 정렬 */
  gap: 10px; /* 하트와 글씨 사이 간격 */
}

.wishlist-icon {
  font-size: 1.5rem; /* 아이콘 크기 확대 */
  color: #ffffff;
  cursor: pointer;
  transition: color 0.3s ease;
}

.wishlist-icon.added {
  color: #e74c3c;
}

.wishlist-actions p {
  font-size: 0.8rem; /* 글씨 크기 */
  color: #73553C; /* 텍스트 색상 */
  font-family: 'JalnanFont', sans-serif; /* 텍스트 폰트 */
  margin: 0;
}

/* 상품 옵션(하단) */
.options-container {
  padding: 15px;
  width: 100%; /* 기본적으로 전체 너비 사용 */
  max-width: 900px; /* 최대 너비 제한 */
  margin: 0 auto; /* 중앙 정렬 */
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

/* 상품 옵션 제목 */
.options-container h2 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.5rem;
  color: #73553C;
  margin-bottom: 15px;
}

/* 테이블 스타일 */
table {
  width: 100%; /* 테이블이 섹션 안에서 전체 너비를 차지 */
  border-collapse: collapse;
  background-color: #fff;
  overflow-x: auto; /* 테이블 내용이 길어질 경우 스크롤 가능 */
}

thead th {
  background-color: #73553C; /* 푸딩-3 */
  color: #fff;
  padding: 10px;
  text-align: center;
  font-size: 1rem; /* 텍스트 크기 확대 */
  font-family: 'GowunDodum-Regular', sans-serif;
}

tbody td {
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #DBDAD6; /* 푸딩-4 */
  font-family: 'GowunDodum-Regular', sans-serif;
}

tbody tr:hover {
  background-color: #FEF0AC; /* 푸딩-1 */
}

/* 반응형 */
@media (max-width: 1024px) {
  .filter-sidebar,
  .options-container {
    max-width: 95%; /* 화면 너비에 맞춰 조정 */
  }
}

@media (max-width: 768px) {
  .product-detail-view {
    padding: 15px;
    max-width: 100%; /* 모바일 화면에서는 양쪽 여백 제거 */
  }

  .filter-sidebar,
  .options-container {
    padding: 10px;
    max-width: 100%; /* 모바일에서도 콘텐츠가 전체 화면을 활용 */
  }

  table {
    font-size: 0.9rem; /* 작은 화면에서는 폰트 크기 축소 */
  }

  .wishlist-icon {
    font-size: 2rem; /* 찜하기 버튼 크기 축소 */
  }
}


</style>
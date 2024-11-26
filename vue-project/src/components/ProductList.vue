<template>
  <div class="product-table">
    <h1 class="table-title">
      {{ isSavingProduct ? "적금 상품 정보" : "예금 상품 정보" }}
    </h1>
    <table>
      <thead>
        <tr>
          <th>은행명</th>
          <th>상품명</th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
        </tr>
      </thead>
      <tbody>
        <router-link
          v-for="product in products"
          :key="product.id"
          tag="tr"
          :to="{
            name: 'ProductDetail',
            params: {
              type: isSavingProduct ? 'saving' : 'deposit',
              id: product.id,
            },
          }"
          class="clickable-row"
        >
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ getInterestRate(product, 6) }}</td>
          <td>{{ getInterestRate(product, 12) }}</td>
          <td>{{ getInterestRate(product, 24) }}</td>
          <td>{{ getInterestRate(product, 36) }}</td>
        </router-link>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  products: {
    type: Array,
    required: true,
    default: () => [], // 기본값으로 빈 배열 설정
  },
  isSavingProduct: {
    type: Boolean,
    required: true,
  },
});


// 특정 상품에서 save_trm에 따라 금리를 가져오는 메서드
function getInterestRate(product, term) {
  const option = product.options.find((opt) => opt.save_trm === term);
  return option ? option.intr_rate : "-";
}
</script>

<style scoped>
/* 전체 테이블 영역 */
.product-table {
  margin: 20px 0;
  padding: 20px;
  background-color: #fef0ac63; /* 푸딩-1 */
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(134, 136, 109, 0.212);
  overflow-x: auto; /* 테이블이 화면을 넘어가지 않도록 스크롤 추가 */
}

/* 제목 스타일 */
.table-title {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.5rem;
  color: #3D0F0E; /* 푸딩-5 */
  margin-bottom: 20px;
  text-align: center;
}

/* 테이블 스타일 */
table {
  width: 100%;
  table-layout: fixed; /* 각 열의 너비를 균등하게 */
  border-collapse: collapse;
  font-family: 'GowunDodum-Regular', sans-serif;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

thead th {
  background-color: #73553C; /* 푸딩-3 */
  color: #FFFFFF; /* 흰색 */
  padding: 15px;
  text-align: center;
  font-size: 0.95rem;
  white-space: nowrap;
}

tbody tr {
  border-bottom: 1px solid #DBDAD6; /* 푸딩-4 */
  transition: background-color 0.2s ease;
}

tbody tr:nth-child(even) {
  background-color: #FDE49B; /* 푸딩-2 */
}

tbody tr:hover {
  background-color: #FEF0AC; /* 푸딩-1 */
}

/* 클릭 가능한 행 */
.clickable-row {
  display: table-row; /* Router-link를 table-row로 설정 */
  text-decoration: none; /* 기본 링크 스타일 제거 */
  color: inherit; /* 텍스트 색상 유지 */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.clickable-row:hover {
  background-color: #fef0ac;
}

td {
  padding: 12px 10px;
  text-align: center;
  font-size: 0.9rem;
  color: #3D0F0E; /* 푸딩-5 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트를 "..."로 표시 */
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .table-title {
    font-size: 1.2rem;
  }

  table {
    font-size: 0.85rem;
  }

  th,
  td {
    padding: 8px;
  }

  .product-table {
    overflow-x: auto; /* 화면 크기 제한 시 스크롤 가능 */
  }
}

</style>


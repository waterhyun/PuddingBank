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
/* 테이블 스타일 */
table {
  width: 100%;
  table-layout: fixed; /* 각 열의 너비를 균등하게 */
  border-collapse: collapse;
  font-family: Arial, sans-serif;
  background-color: #fff;
  border-radius: 5px;
  overflow: hidden;
}

thead th {
  background-color: #0046b3;
  color: #fff;
  padding: 12px 10px;
  text-align: center;
  font-size: 0.9em;
  white-space: nowrap;
}

tbody tr {
  border-bottom: 1px solid #ddd;
  transition: background-color 0.2s;
}

.clickable-row {
  display: table-row; /* Router-link를 table-row로 설정 */
  text-decoration: none; /* 기본 링크 스타일 제거 */
  color: inherit; /* 텍스트 색상 유지 */
}

.clickable-row:hover {
  background-color: #f1f1f1;
}

td {
  padding: 12px 10px;
  text-align: center;
  font-size: 0.9em;
  white-space: nowrap;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  table {
    font-size: 0.8em;
  }

  th,
  td {
    padding: 10px;
  }
}
</style>



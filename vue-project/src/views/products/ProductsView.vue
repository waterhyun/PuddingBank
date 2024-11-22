<template>
  <div class="products-view">
    <!-- 필터 영역 -->
    <div class="filter-sidebar">
      <h3>
       {{ isSavingProduct ? "적금 상품 정보" : "예금 상품 정보" }}
      </h3>
      <p>검색조건을 입력하세요.</p>
      <div class="filter-item">
        <label for="bank">은행명을 선택하세요.</label>
        <select v-model="selectedBank" @change="applyFilters">
          <option value="">전체</option>
          <option v-for="bank in bankNames" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <label for="saveTerm">예치기간(개월)을 선택하세요.</label>
        <select v-model="selectedSaveTerm" @change="applyFilters">
          <option value="">전체</option>
          <option v-for="term in fixedSaveTerms" :key="term" :value="term">
            {{ term }}개월
          </option>
        </select>
      </div>
      <button @click="resetFilters">초기화</button>
    </div>

    <!-- 탭 -->
    <div class="tabs-container">
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'deposit' }"
          @click="setTab('deposit')"
        >
          정기예금
        </button>
        <button
          :class="{ active: activeTab === 'saving' }"
          @click="setTab('saving')"
        >
          적금
        </button>
      </div>
      <!-- 상품 리스트 -->
      <div class="tab-content">
        <div v-if="activeTab === 'deposit'">
          <ProductList
            :products="filteredDepositProducts"
            :isSavingProduct="false"
          />
        </div>
        <div v-else-if="activeTab === 'saving'">
          <ProductList
            :products="filteredSavingProducts"
            :isSavingProduct="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ProductList from "@/components/ProductList.vue";
import { onMounted, ref, computed } from "vue";
import { useProductStore } from "@/stores/product";

// Pinia 스토어
const store = useProductStore();

// 필터 상태
const selectedBank = ref("");
const selectedSaveTerm = ref("");
const activeTab = ref("deposit");
const isSavingProduct = computed(() => activeTab.value === "saving");

// 고정된 저장 기간 목록
const fixedSaveTerms = [6, 12, 24, 36];

// 탭 전환 함수
const setTab = (tab) => {
  activeTab.value = tab;
};

// 필터링된 정기예금 상품
const filteredDepositProducts = computed(() => {
  return store.depositproducts.filter((product) => {
    const matchesBank =
      selectedBank.value === "" || product.kor_co_nm === selectedBank.value;
    const matchesSaveTerm =
      selectedSaveTerm.value === "" ||
      product.options.some((opt) => opt.save_trm === Number(selectedSaveTerm.value));
    return matchesBank && matchesSaveTerm;
  });
});

// 필터링된 적금 상품
const filteredSavingProducts = computed(() => {
  return store.savingproducts.filter((product) => {
    const matchesBank =
      selectedBank.value === "" || product.kor_co_nm === selectedBank.value;
    const matchesSaveTerm =
      selectedSaveTerm.value === "" ||
      product.options.some((opt) => opt.save_trm === Number(selectedSaveTerm.value));
    return matchesBank && matchesSaveTerm;
  });
});

// 은행명 옵션 계산
const bankNames = computed(() =>
  [...new Set([...store.depositproducts, ...store.savingproducts].map((item) => item.kor_co_nm))]
);

// 필터 초기화
const resetFilters = () => {
  selectedBank.value = "";
  selectedSaveTerm.value = "";
};

// 데이터 로드
onMounted(async () => {
  await store.getDepositProducts();
  await store.getSavingProducts();
});
</script>

<style scoped>
/* 전체 레이아웃 */
.products-view {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #f7f8fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  align-items: flex-start; /* 필터와 콘텐츠의 세로 정렬을 상단으로 설정 */
}

/* 필터 영역 스타일 */
.filter-sidebar {
  position: sticky; /* 스크롤에 따라 이동 */
  top: 20px; /* 화면 상단에서 20px 간격 */
  width: 20%;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  height: auto; /* 콘텐츠 높이에 맞춤 */
  display: flex;
  flex-direction: column;
  gap: 10px; /* 항목 간 간격 */
}

/* 필터 제목 */
.filter-sidebar h3 {
  font-size: 1rem;
  margin-bottom: 5px;
  color: #333;
}

/* 필터 라벨 */
.filter-item label {
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 5px;
}

/* 드롭다운 메뉴 */
.filter-item select {
  width: 100%;
  padding: 8px;
  font-size: 0.85rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* 초기화 버튼 */
.filter-sidebar button {
  padding: 8px;
  font-size: 0.9rem;
  background-color: #0056b3;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.filter-sidebar button:hover {
  background-color: #003d80;
}

/* 탭 스타일 */
.tabs-container {
  width: 70%;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs button {
  flex: 1;
  padding: 10px 15px;
  font-size: 1rem;
  color: #0056b3;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tabs button.active {
  font-weight: bold;
  color: #0056b3;
  border-bottom: 2px solid #0056b3;
}

.tabs button:hover {
  color: #003d80;
}

.tab-content h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

/* 반응형 */
@media (max-width: 768px) {
  .products-view {
    flex-direction: column;
  }

  .filter-sidebar {
    width: 100%;
  }

  .tabs-container {
    width: 100%;
  }
}

</style>

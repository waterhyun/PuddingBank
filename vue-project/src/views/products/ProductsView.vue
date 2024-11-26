<template>
  <div class="products-view">
    <!-- 필터 영역 -->
    <div class="filter-sidebar">
      <h3>
       {{ isSavingProduct ? "적금 상품 검색" : "예금 상품 검색" }}
      </h3>
      <!-- <p>검색조건을 입력하세요.</p> -->
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
  background-color: #fffefb; 
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  align-items: flex-start; /* 필터와 콘텐츠의 세로 정렬을 상단으로 설정 */
}

/* 필터 영역 스타일 */
.filter-sidebar {
  position: sticky;
  top: 20px;
  width: 20%;
  padding: 15px;
  background-color: #FEF0AC;  /* 푸딩-2 */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 검색 조건 텍스트 스타일 */
.filter-sidebar p {
  font-family: 'JalnanFont', sans-serif;
  font-size: 0.95rem;
  color: #3D0F0E; /* 푸딩-5 */
  margin-bottom: 15px;
}
/* 필터 제목 */
.filter-sidebar h3 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #73553C; /* 푸딩-3 */
}

/* 필터 라벨 */
.filter-item label {
  font-family: 'JalnanFont', sans-serif;
  font-size: 0.9rem;
  color: #3D0F0E; /* 푸딩-5 */
  margin-bottom: 5px;
}

/* 드롭다운 메뉴 */
.filter-item select {
  font-family: 'JalnanFont', sans-serif;
  width: 100%;
  padding: 8px;
  font-size: 0.9rem;
  border: 1px solid #DBDAD6; /* 푸딩-4 */
  border-radius: 5px;
  background-color: #FFFFFF;
}

/* 초기화 버튼 */
.filter-sidebar button {
  padding: 10px;
  font-family: 'JalnanFont', sans-serif;
  font-size: 1rem;
  background-color: #3D0F0E; /* 푸딩-5 */
  color: #FFFFFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-sidebar button:hover {
  background-color: #73553C; /* 푸딩-3 */
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
  font-family: 'JalnanFont', sans-serif;
  font-size: 1rem;
  color: #73553C; /* 푸딩-5 */
  background-color: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tabs button.active {
  font-family: 'JalnanFont', sans-serif;
  font-weight: bold;
  color: #3D0F0E; /* 푸딩-5 */
  border-bottom: 2px solid #3D0F0E;
}

.tabs button:hover {
  color: #73553C; /* 푸딩-3 */
}

.tab-content h2 {
  margin-bottom: 20px;
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.5rem;
  color: #73553C; /* 푸딩-3 */
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

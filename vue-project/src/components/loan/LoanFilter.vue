<template>
  <div class="filter-sidebar">
    <h3>대출 조건 검색</h3>
    <div class="filter-item">
      <label>대출 종류를 선택하세요.</label>
      <select @change="updateFilter('loanType', $event.target.value)">
        <option value="">전체</option>
        <option v-for="type in loanTypes" :key="type" :value="type">
          {{ type }}
        </option>
      </select>
    </div>

    <div class="filter-item">
      <label>금리 유형을 선택하세요.</label>
      <select @change="updateFilter('rateType', $event.target.value)">
        <option value="">전체</option>
        <option value="F">고정금리</option>
        <option value="C">변동금리</option>
      </select>
    </div>

    <div class="filter-item">
      <label>상환 방식을 선택하세요.</label>
      <select @change="updateFilter('repayType', $event.target.value)">
        <option value="">전체</option>
        <option value="D">분할상환</option>
        <option value="S">만기일시상환</option>
      </select>
    </div>
    <button @click="$emit('filter-reset')">초기화</button>
  </div>
</template>

<script setup>
const props = defineProps({
  loanTypes: {
    type: Array,
    required: true,
  },
});
const emit = defineEmits(["filter-change", "filter-reset"]);

const updateFilter = (key, value) => {
  emit("filter-change", { [key]: value });
};
</script>

<style scoped>
.filter-sidebar {
  position: sticky;
  top: 20px;
  width: 250px; /* 고정 너비로 설정 */
  max-width: 100%; /* 반응형 지원 */
  padding: 15px;
  background-color: #FEF0AC;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.filter-sidebar h3 {
  font-family: 'JalnanFont', sans-serif;
  font-size: 1.2rem;
  color: #73553C;
}

.filter-sidebar p {
  font-family: 'JalnanFont', sans-serif;
  font-size: 0.95rem;
  color: #3D0F0E;
}

.filter-item label {
  font-family: 'JalnanFont', sans-serif;
  font-size: 0.9rem;
  color: #3D0F0E;
  margin-bottom: 5px;
}

.filter-item select {
  font-family: 'JalnanFont', sans-serif;
  width: 100%;
  padding: 8px;
  font-size: 0.9rem;
  border: 1px solid #DBDAD6;
  border-radius: 5px;
  background-color: #FFFFFF;
}

.filter-sidebar button {
  padding: 10px;
  font-family: 'JalnanFont', sans-serif;
  font-size: 1rem;
  background-color: #3D0F0E;
  color: #FFFFFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-sidebar button:hover {
  background-color: #73553C;
}
</style>

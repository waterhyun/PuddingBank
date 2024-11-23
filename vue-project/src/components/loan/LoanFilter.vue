<template>
  <div class="filter-controls">
    <div class="filter-group">
      <label>대출 종류:</label>
      <select @change="updateFilter('loanType', $event.target.value)">
        <option value="">전체</option>
        <option v-for="type in loanTypes" :key="type" :value="type">
          {{ type }}
        </option>
      </select>
    </div>

    <div class="filter-group">
      <label>금리 유형:</label>
      <select @change="updateFilter('rateType', $event.target.value)">
        <option value="">전체</option>
        <option value="F">고정금리</option>
        <option value="C">변동금리</option>
      </select>
    </div>

    <div class="filter-group">
      <label>상환 방식:</label>
      <select @change="updateFilter('repayType', $event.target.value)">
        <option value="">전체</option>
        <option value="D">분할상환</option>
        <option value="S">만기일시상환</option>
      </select>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  loanTypes: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['filter-change'])

const updateFilter = (key, value) => {
  emit('filter-change', { [key]: value })
}
</script>

<style scoped>
.filter-controls {
  display: flex;
  gap: 20px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

label {
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
}

select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ced4da;
  background-color: white;
  font-size: 14px;
  min-width: 120px;
  cursor: pointer;
}

select:hover {
  border-color: #adb5bd;
}

select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

@media (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
    gap: 12px;
  }

  .filter-group {
    width: 100%;
  }

  select {
    width: 100%;
  }
}
</style>

<!-- src/components/forms/FoodLogForm.vue -->
<template>
    <div class="food-log-form">
      <div class="form-header">
        <h2>添加饮食记录</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
  
      <form @submit.prevent="handleSubmit">
        <div class="form-grid">
          <div class="form-group full-width">
            <label for="date">日期</label>
            <input 
              type="date" 
              id="date" 
              v-model="form.date"
              :max="today"
              required
              class="styled-input"
            >
          </div>
  
          <div class="form-group full-width">
            <label for="meal">餐次</label>
            <select 
              id="meal" 
              v-model="form.meal" 
              required
              class="styled-select"
            >
              <option value="" disabled>请选择餐次</option>
              <option value="1">早餐</option>
              <option value="2">午餐</option>
              <option value="3">晚餐</option>
              <option value="4">加餐</option>
            </select>
          </div>
  
          <div class="form-group full-width">
            <label for="foodItem">食物名称</label>
            <input 
              type="text" 
              id="foodItem" 
              v-model="form.foodItem"
              required
              placeholder="请输入食物名称"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="calories">
              卡路里
              <span class="unit">(kcal)</span>
            </label>
            <input 
              type="number" 
              id="calories" 
              v-model="form.calories"
              min="0"
              required
              placeholder="0"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="protein">
              蛋白质
              <span class="unit">(g)</span>
            </label>
            <input 
              type="number" 
              id="protein" 
              v-model="form.protein"
              min="0"
              required
              placeholder="0"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="carbs">
              碳水
              <span class="unit">(g)</span>
            </label>
            <input 
              type="number" 
              id="carbs" 
              v-model="form.carbs"
              min="0"
              required
              placeholder="0"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="fats">
              脂肪
              <span class="unit">(g)</span>
            </label>
            <input 
              type="number" 
              id="fats" 
              v-model="form.fats"
              min="0"
              required
              placeholder="0"
              class="styled-input"
            >
          </div>

        <div class="form-group">
          <label for="fiber">
            膳食纤维
            <span class="unit">(g)</span>
          </label>
          <input 
            type="number" 
            id="fiber" 
            v-model="form.fiber"
            min="0"
            required
            placeholder="0"
            class="styled-input"
          >
        </div>
        </div>
  
        <div class="form-actions">
          <button 
            type="button" 
            class="cancel-btn"
            @click="$emit('close')"
          >
            取消
          </button>
          <button 
            type="submit" 
            class="submit-btn"
            :disabled="loading"
          >
            {{ loading ? '提交中...' : '提交' }}
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref, computed } from 'vue'
  
  const emit = defineEmits(['submit', 'close'])
  const loading = ref(false)
  
  const today = computed(() => {
    return new Date().toISOString().split('T')[0]
  })
  
  const form = reactive({
    date: today.value,
    meal: '',
    foodItem: '',
    calories: '',
    protein: '',
    carbs: '',
    fats: '',
    fiber: ''
  })
  
  const handleSubmit = async () => {
  loading.value = true
  try {
    await emit('submit', { 
      date: form.date,
      meal: form.meal,
      food_item: form.foodItem, 
      calories: form.calories,
      protein: form.protein,
      carbs: form.carbs,
      fats: form.fats,
      fiber: form.fiber || 0
    })
    emit('close')
  } finally {
    loading.value = false
  }
}

  </script>
  
  <style scoped>
  .food-log-form {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    width: 100%;
    max-width: 600px;
  }
  
  .form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
  }
  
  .form-header h2 {
    color: #2c3e50;
    font-size: 1.5rem;
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #666;
    cursor: pointer;
    padding: 0.5rem;
    line-height: 1;
  }
  
  .close-btn:hover {
    color: #333;
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-group.full-width {
    grid-column: 1 / -1;
  }
  
  label {
    color: #4a5568;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  .unit {
    color: #718096;
    font-size: 0.875rem;
    font-weight: normal;
  }
  
  .styled-input,
  .styled-select {
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;
  }
  
  .styled-input:focus,
  .styled-select:focus {
    border-color: #4CAF50;
    outline: none;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  }
  
  .styled-input::placeholder {
    color: #a0aec0;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .submit-btn,
  .cancel-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .submit-btn {
    background: #4CAF50;
    color: white;
    border: none;
  }
  
  .submit-btn:hover {
    background: #45a049;
  }
  
  .submit-btn:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
  
  .cancel-btn {
    background: white;
    color: #4a5568;
    border: 2px solid #e2e8f0;
  }
  
  .cancel-btn:hover {
    background: #f8fafc;
    border-color: #cbd5e0;
  }
  
  /* 响应式设计 */
  @media (max-width: 640px) {
    .form-grid {
      grid-template-columns: 1fr;
    }
    
    .food-log-form {
      padding: 1rem;
    }
    
    .form-actions {
      flex-direction: column-reverse;
    }
    
    .submit-btn,
    .cancel-btn {
      width: 100%;
    }
  }
  </style>
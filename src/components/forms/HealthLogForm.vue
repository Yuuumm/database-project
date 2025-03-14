<template>
    <div class="health-log-form">
      <div class="form-header">
        <h2>记录健康日志</h2>
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
  
          <div class="form-group">
            <label for="weight">
              体重
              <span class="unit">(kg)</span>
            </label>
            <input 
              type="number" 
              id="weight" 
              v-model="form.weight"
              min="0"
              step="0.1"
              required
              placeholder="0.0"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="mood">情绪状态</label>
            <select 
              id="mood" 
              v-model="form.mood" 
              class="styled-select"
            >
              <option value="">--请选择--</option>
              <option value="excellent">非常好</option>
              <option value="good">良好</option>
              <option value="normal">一般</option>
              <option value="bad">不佳</option>
              <option value="terrible">很差</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="sleepStart">
              入睡时间
            </label>
            <input 
              type="time" 
              id="sleepStart" 
              v-model="form.sleepStart"
              class="styled-input"
            >
          </div>
  
          <div class="form-group">
            <label for="sleepEnd">
              起床时间
            </label>
            <input 
              type="time" 
              id="sleepEnd" 
              v-model="form.sleepEnd"
              class="styled-input"
            >
          </div>
  
          <div class="form-group full-width">
            <label for="notes">备注</label>
            <textarea
              id="notes"
              v-model="form.notes"
              placeholder="记录今天的其他健康信息..."
              class="styled-textarea"
            ></textarea>
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
  import { reactive, ref, computed, watch } from 'vue'
  
  const emit = defineEmits(['submit', 'close'])
  const loading = ref(false)
  
  const today = computed(() => {
    return new Date().toISOString().split('T')[0]
  })
  
  const form = reactive({
    date: today.value,
    weight: '',
    mood: '',
    sleepStart: '',
    sleepEnd: '',
    notes: ''
  })
  
  // 计算睡眠时长
  const calculateSleepHours = () => {
    if (!form.sleepStart || !form.sleepEnd) return null
    
    let startTime = new Date(`2000-01-01T${form.sleepStart}:00`)
    let endTime = new Date(`2000-01-01T${form.sleepEnd}:00`)
    
    // 处理跨天的情况
    if (endTime < startTime) {
      endTime = new Date(`2000-01-02T${form.sleepEnd}:00`)
    }
    
    const diff = (endTime - startTime) / (1000 * 60 * 60)
    return parseFloat(diff.toFixed(1))
  }
  
  const handleSubmit = async () => {
  loading.value = true
  try {
    const sleepHours = calculateSleepHours()
    
    const formData = {
      date: form.date,
      weight: parseFloat(form.weight),
      mood: form.mood,
      sleep_start: form.sleepStart,
      sleep_end: form.sleepEnd,
      sleep_hours: sleepHours,
      notes: form.notes
    }
    
    console.log('Submitting health log:', formData) // 添加日志
    await emit('submit', formData)
    emit('close')
  } catch (error) {
    console.error('提交健康日志失败:', error)
    alert('提交失败，请重试')
  } finally {
    loading.value = false
  }
}
  </script>
  
  <style scoped>
  .health-log-form {
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
  .styled-select,
  .styled-textarea {
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;
  }
  
  .styled-textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  .styled-input:focus,
  .styled-select:focus,
  .styled-textarea:focus {
    border-color: #4CAF50;
    outline: none;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
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
  
  .cancel-btn {
    background: white;
    color: #4a5568;
    border: 2px solid #e2e8f0;
  }
  
  @media (max-width: 640px) {
    .form-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>
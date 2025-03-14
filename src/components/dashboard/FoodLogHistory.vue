<!-- src/components/dashboard/FoodLogHistory.vue -->
<template>
    <div class="food-log-history">
      <div class="history-header">
        <h2>饮食记录历史</h2>
        <div class="date-filter">
          <input 
            type="date" 
            v-model="startDate"
            :max="today"
          >
          <span>至</span>
          <input 
            type="date" 
            v-model="endDate"
            :max="today"
          >
          <button @click="loadHistory">查询</button>
        </div>
      </div>
  
      <div class="history-content">
        <div v-if="loading" class="loading">
          加载中...
        </div>
  
        <div v-else-if="!historyLogs.length" class="no-data">
          该时间段内暂无记录
        </div>
  
        <div v-else class="history-table">
          <table>
            <thead>
              <tr>
                <th>日期</th>
                <th>餐次</th>
                <th>食物</th>
                <th>卡路里(kcal)</th>
                <th>蛋白质(g)</th>
                <th>碳水(g)</th>
                <th>脂肪(g)</th>
                <th>膳食纤维(g)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in historyLogs" :key="log.id">
                <td>{{ formatDate(log.date) }}</td>
                <td>{{ getMealName(log.meal) }}</td>
                <td>{{ log.food_item }}</td>
                <td>{{ log.calories || 0}}</td>
                <td>{{ log.protein || 0}}</td>
                <td>{{ log.carbs || 0}}</td>
                <td>{{ log.fats || 0}}</td>
                <td>{{ log.fiber || 0}}</td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- 统计摘要 -->
        <div v-if="historyLogs.length" class="history-summary">
          <h3>时间段统计</h3>
          <div class="summary-grid">
            <div class="summary-item">
              <span class="label">平均卡路里</span>
              <span class="value">{{ averages.calories }} kcal</span>
            </div>
            <div class="summary-item">
              <span class="label">平均蛋白质</span>
              <span class="value">{{ averages.protein }} g</span>
            </div>
            <div class="summary-item">
              <span class="label">平均碳水</span>
              <span class="value">{{ averages.carbs }} g</span>
            </div>
            <div class="summary-item">
              <span class="label">平均脂肪</span>
              <span class="value">{{ averages.fats }} g</span>
            </div>
            <div class="summary-item">
              <span class="label">平均膳食纤维</span>
              <span class="value">{{ averages.fiber }} g</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useFoodLogStore } from '@/stores/foodLog'
  
  const foodLogStore = useFoodLogStore()
  const loading = ref(false)
  const historyLogs = ref([])
  
  // 获取今天的日期
  const today = computed(() => new Date().toISOString().split('T')[0])
  
  // 默认显示最近7天的记录
  const startDate = ref(
    new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  )
  const endDate = ref(today.value)
  
  // 计算平均值
  const averages = computed(() => {
    if (!historyLogs.value.length) return { calories: 0, protein: 0, carbs: 0, fats: 0 }
    
    const sum = historyLogs.value.reduce((acc, log) => ({
      calories: acc.calories + Number(log.calories),
      protein: acc.protein + Number(log.protein),
      carbs: acc.carbs + Number(log.carbs),
      fats: acc.fats + Number(log.fats),
      fiber: acc.fiber + Number(log.fiber)
    }), { calories: 0, protein: 0, carbs: 0, fats: 0, fiber: 0 })

  
    const count = historyLogs.value.length
    
    return {
      calories: (sum.calories / count).toFixed(1),
      protein: (sum.protein / count).toFixed(1),
      carbs: (sum.carbs / count).toFixed(1),
      fats: (sum.fats / count).toFixed(1),
      fiber: (sum.fiber / count).toFixed(1)
    }
  })
  
  // 加载历史记录
  async function loadHistory() {
    if (!startDate.value || !endDate.value) {
      alert('请选择日期范围')
      return
    }
  
    loading.value = true
    try {
      historyLogs.value = await foodLogStore.getLogsByDateRange(
        startDate.value,
        endDate.value
      )
    } catch (error) {
      console.error('加载历史记录失败:', error)
      alert('加载历史记录失败')
    } finally {
      loading.value = false
    }
  }
  
  // 格式化日期
  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('zh-CN')
  }
  
  // 获取餐次名称
  function getMealName(meal) {
    const meals = {
      '1': '早餐',
      '2': '午餐',
      '3': '晚餐',
      '4': '加餐'
    }
    return meals[meal] || meal
  }
  
  // 组件加载时自动加载数据
  loadHistory()
  </script>
  
  <style scoped>
  .food-log-history {
    padding: 1rem;
  }
  
  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .date-filter {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }
  
  .date-filter input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .date-filter button {
    padding: 0.5rem 1rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .history-table {
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  th {
    background: #f8f9fa;
    font-weight: 600;
  }
  
  .loading, .no-data {
    text-align: center;
    padding: 2rem;
    color: #666;
  }
  
  .history-summary {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1.5rem;
  }
  
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .summary-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: white;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .summary-item .label {
    color: #666;
    margin-bottom: 0.5rem;
  }
  
  .summary-item .value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2c3e50;
  }
  </style>
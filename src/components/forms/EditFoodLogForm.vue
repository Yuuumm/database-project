<template>
    <div class="edit-food-log-form">
      <div class="form-header">
        <h2>修改饮食记录</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
  
      <div v-if="loading" class="loading">
        加载中...
      </div>
      
      <div v-else-if="!foodLogs.length" class="no-data">
        今日暂无记录
      </div>
      
      <div v-else>
        <div class="food-log-list">
          <div 
            v-for="log in foodLogs" 
            :key="log.id" 
            class="food-log-item"
            :class="{ 'selected': selectedLog && selectedLog.id === log.id }"
            @click="selectLog(log)"
          >
            <div class="food-info">
              <div class="food-name">{{ log.food_item }}</div>
              <div class="food-details">
                {{ getMealName(log.meal) }} · {{ log.calories }} 卡路里
              </div>
            </div>
            <div class="food-actions">
              <button 
                class="delete-btn" 
                @click.stop="confirmDelete(log.id)"
                title="删除"
              >
                &times;
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="selectedLog" class="edit-form">
          <h3>编辑记录</h3>
          
          <form @submit.prevent="handleUpdate">
            <div class="form-grid">
              <div class="form-group">
                <label for="editMeal">餐次</label>
                <select 
                  id="editMeal" 
                  v-model="editForm.meal" 
                  required
                  class="styled-select"
                >
                  <option value="1">早餐</option>
                  <option value="2">午餐</option>
                  <option value="3">晚餐</option>
                  <option value="4">加餐</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="editFoodItem">食物名称</label>
                <input 
                  type="text" 
                  id="editFoodItem" 
                  v-model="editForm.foodItem"
                  required
                  class="styled-input"
                >
              </div>
              
              <div class="form-group">
                <label for="editCalories">卡路里 (kcal)</label>
                <input 
                  type="number" 
                  id="editCalories" 
                  v-model="editForm.calories"
                  min="0"
                  required
                  class="styled-input"
                >
              </div>
              
              <div class="form-group">
                <label for="editProtein">蛋白质 (g)</label>
                <input 
                  type="number" 
                  id="editProtein" 
                  v-model="editForm.protein"
                  min="0"
                  required
                  class="styled-input"
                >
              </div>
              
              <div class="form-group">
                <label for="editCarbs">碳水化合物 (g)</label>
                <input 
                  type="number" 
                  id="editCarbs" 
                  v-model="editForm.carbs"
                  min="0"
                  required
                  class="styled-input"
                >
              </div>
              
              <div class="form-group">
                <label for="editFats">脂肪 (g)</label>
                <input 
                  type="number" 
                  id="editFats" 
                  v-model="editForm.fats"
                  min="0"
                  required
                  class="styled-input"
                >
              </div>
              
              <div class="form-group">
                <label for="editFiber">膳食纤维 (g)</label>
                <input 
                  type="number" 
                  id="editFiber" 
                  v-model="editForm.fiber"
                  min="0"
                  required
                  class="styled-input"
                >
              </div>
            </div>
            
            <div class="form-actions">
              <button 
                type="button" 
                class="cancel-btn"
                @click="cancelEdit"
              >
                取消
              </button>
              <button 
                type="submit" 
                class="update-btn"
                :disabled="updating"
              >
                {{ updating ? '更新中...' : '更新' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'
  
  const emit = defineEmits(['close', 'refresh'])
  const userStore = useUserStore()
  const loading = ref(false)
  const updating = ref(false)
  const foodLogs = ref([])
  const selectedLog = ref(null)
  
  // 编辑表单数据
  const editForm = reactive({
    meal: '',
    foodItem: '',
    calories: '',
    protein: '',
    carbs: '',
    fats: '',
    fiber: ''
  })
  
  // 获取今天的日期
  const today = new Date().toISOString().split('T')[0]
  
  // 加载今日食物日志
  const loadTodayFoodLogs = async () => {
    if (!userStore.userId) return
    
    loading.value = true
    try {
      const response = await axios.get(
        `http://localhost:5000/query_food_log?user_id=${userStore.userId}&date=${today}`
      )
      foodLogs.value = response.data.food_logs || []
    } catch (error) {
      console.error('获取食物日志失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 选择要编辑的日志
  const selectLog = (log) => {
    selectedLog.value = log
    editForm.meal = log.meal
    editForm.foodItem = log.food_item
    editForm.calories = log.calories
    editForm.protein = log.protein
    editForm.carbs = log.carbs
    editForm.fats = log.fats
    editForm.fiber = log.fiber || 0
  }
  
  // 取消编辑
  const cancelEdit = () => {
    selectedLog.value = null
  }
  
  // 确认删除
  const confirmDelete = async (id) => {
    if (!confirm('确定要删除这条记录吗？')) return
    
    try {
      await axios.delete(`http://localhost:5000/delete_food_log/${id}`)
      await loadTodayFoodLogs() // 重新加载数据
      selectedLog.value = null
      emit('refresh') // 通知父组件刷新数据
    } catch (error) {
      console.error('删除食物日志失败:', error)
      alert('删除失败，请重试')
    }
  }
  
  // 更新记录
  const handleUpdate = async () => {
    if (!selectedLog.value) return
    
    updating.value = true
    try {
      // 使用PUT方法更新记录
      await axios.put(`http://localhost:5000/update_food_log/${selectedLog.value.id}`, {
        meal: editForm.meal,
        food_item: editForm.foodItem,
        calories: parseFloat(editForm.calories),
        protein: parseFloat(editForm.protein),
        carbs: parseFloat(editForm.carbs),
        fats: parseFloat(editForm.fats),
        fiber: parseFloat(editForm.fiber || 0)
      })
      
      await loadTodayFoodLogs() // 重新加载数据
      selectedLog.value = null
      emit('refresh') // 通知父组件刷新数据
    } catch (error) {
      console.error('更新食物日志失败:', error)
      alert('更新失败，请重试')
    } finally {
      updating.value = false
    }
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
  
  onMounted(() => {
    loadTodayFoodLogs()
  })
  </script>
  
  <style scoped>
  .edit-food-log-form {
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
  
  .loading, .no-data {
    text-align: center;
    padding: 2rem 0;
    color: #666;
  }
  
  .food-log-list {
    max-height: 200px;
    overflow-y: auto;
    margin-bottom: 1.5rem;
    border: 1px solid #eee;
    border-radius: 8px;
  }
  
  .food-log-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .food-log-item:last-child {
    border-bottom: none;
  }
  
  .food-log-item:hover {
    background-color: #f9f9f9;
  }
  
  .food-log-item.selected {
    background-color: #e6f7e6;
    border-left: 3px solid #4CAF50;
  }
  
  .food-info {
    flex: 1;
  }
  
  .food-name {
    font-weight: 500;
    color: #2c3e50;
  }
  
  .food-details {
    font-size: 0.875rem;
    color: #666;
    margin-top: 0.25rem;
  }
  
  .food-actions {
    display: flex;
    align-items: center;
  }
  
  .delete-btn {
    background: none;
    border: none;
    color: #dc3545;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0.25rem;
  }
  
  .edit-form {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #eee;
  }
  
  .edit-form h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #2c3e50;
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
  
  .styled-input,
  .styled-select {
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    width: 100%;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
  }
  
  .update-btn,
  .cancel-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
  }
  
  .update-btn {
    background: #4CAF50;
    color: white;
    border: none;
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
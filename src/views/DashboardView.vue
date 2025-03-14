<template>
  <div class="dashboard-page">
    <AppHeader />
    
    <div class="container">
      <h1 class="page-title">仪表盘</h1>
      
      <!-- 用户统计信息 -->
      <div class="stats-grid">
        <UserStats :stats="userStats" />
        <HealthLogCard />
      </div>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button @click="showFoodLogForm = true" class="add-log-btn">
          添加饮食记录
        </button>
        <button @click="showEditFoodLogForm = true" class="edit-log-btn">
          修改饮食记录
        </button>
      </div>
      
      <!-- 今日饮食记录 -->
      <div class="food-log-section">
        <h2>今日饮食记录</h2>
        <div class="food-log-actions">
          <button @click="refreshFoodLogs" class="refresh-btn">刷新</button>
          <button @click="showFoodLogForm = true" class="add-btn">添加记录</button>
        </div>
        
        <div v-if="loadingFoodLogs" class="loading">
          加载中...
        </div>
        
        <div v-else-if="!todayFoodLogs.length" class="no-data">
          今日暂无饮食记录
        </div>
        
        <div v-else class="food-log-table">
          <table>
            <thead>
              <tr>
                <th>餐次</th>
                <th>食物</th>
                <th>卡路里(kcal)</th>
                <th>蛋白质(g)</th>
                <th>碳水(g)</th>
                <th>脂肪(g)</th>
                <th>膳食纤维(g)</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in todayFoodLogs" :key="log.id">
                <td>{{ getMealName(log.meal) }}</td>
                <td>{{ log.food_item }}</td>
                <td>{{ log.calories }}</td>
                <td>{{ log.protein }}</td>
                <td>{{ log.carbs }}</td>
                <td>{{ log.fats }}</td>
                <td>{{ log.fiber || 0 }}</td>
                <td>
                  <button @click="deleteFoodLog(log.id)" class="delete-btn">删除</button>
                </td>
              </tr>
              <tr class="total-row">
                <td colspan="2">总计</td>
                <td>{{ totalNutrients.calories }}</td>
                <td>{{ totalNutrients.protein }}</td>
                <td>{{ totalNutrients.carbs }}</td>
                <td>{{ totalNutrients.fats }}</td>
                <td>{{ totalNutrients.fiber }}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 数据可视化 -->
      <div class="data-visualization-section">
        <h2>数据可视化</h2>
        <div class="charts-grid">
          <NutrientDistributionChart :data="todayFoodLogs" />
          <WeeklyCaloriesChart />
        </div>
      </div>
    </div>
    
    <!-- 添加饮食记录弹窗 -->
    <Modal v-if="showFoodLogForm" @close="showFoodLogForm = false">
      <FoodLogForm @submit="handleAddFoodLog" @close="showFoodLogForm = false" />
    </Modal>
    
    <!-- 修改饮食记录弹窗 -->
    <Modal v-if="showEditFoodLogForm" @close="showEditFoodLogForm = false">
      <EditFoodLogForm @refresh="refreshData" @close="showEditFoodLogForm = false" />
    </Modal>
    
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import Modal from '@/components/common/Modal.vue'
import UserStats from '@/components/dashboard/UserStats.vue'
import HealthLogCard from '@/components/dashboard/HealthLogCard.vue'
import FoodLogForm from '@/components/forms/FoodLogForm.vue'
import EditFoodLogForm from '@/components/forms/EditFoodLogForm.vue'
import NutrientDistributionChart from '@/components/visualization/NutrientDistributionChart.vue'
import WeeklyCaloriesChart from '@/components/visualization/WeeklyCaloriesChart.vue'

const userStore = useUserStore()
const userId = computed(() => userStore.userId)
const userStats = ref({
  targetCalories: 0,
  consumedCalories: 0,
  bmi: 0,
  weight: 0,
  previousWeight: 0
})

const showFoodLogForm = ref(false)
const showEditFoodLogForm = ref(false)
const loadingFoodLogs = ref(false)
const todayFoodLogs = ref([])

// 获取今天的日期
const today = new Date().toISOString().split('T')[0]

// 计算营养素总和
const totalNutrients = computed(() => {
  return todayFoodLogs.value.reduce((total, log) => {
    return {
      calories: total.calories + Number(log.calories),
      protein: total.protein + Number(log.protein),
      carbs: total.carbs + Number(log.carbs),
      fats: total.fats + Number(log.fats),
      fiber: total.fiber + Number(log.fiber || 0)
    }
  }, { calories: 0, protein: 0, carbs: 0, fats: 0, fiber: 0 })
})

// 获取用户统计数据
const fetchUserStats = async () => {
  try {
    // 获取目标卡路里和BMI等信息
    const intakeResponse = await axios.get(`http://localhost:5000/user_intake/${userId.value}`)
    
    userStats.value = {
      targetCalories: intakeResponse.data.target_calories,
      consumedCalories: totalNutrients.value.calories,
      bmi: intakeResponse.data.bmi,
      weight: intakeResponse.data.weight,
      previousWeight: intakeResponse.data.weight // 暂时设为相同值
    }
  } catch (error) {
    console.error('获取用户统计数据失败:', error)
  }
}

// 获取今日饮食记录
const fetchTodayFoodLogs = async () => {
  if (!userId.value) return
  
  loadingFoodLogs.value = true
  try {
    const response = await axios.get(
      `http://localhost:5000/query_food_log?user_id=${userId.value}&date=${today}`
    )
    todayFoodLogs.value = response.data.food_logs || []
  } catch (error) {
    console.error('获取今日饮食记录失败:', error)
  } finally {
    loadingFoodLogs.value = false
  }
}

// 添加饮食记录
const handleAddFoodLog = async (formData) => {
  try {
    await axios.post('http://localhost:5000/add_food_log', {
      user_id: userId.value,
      ...formData
    })
    refreshData()
  } catch (error) {
    console.error('添加饮食记录失败:', error)
    alert('添加饮食记录失败: ' + (error.response?.data?.message || error.message))
  }
}

// 删除饮食记录
const deleteFoodLog = async (logId) => {
  if (!confirm('确定要删除这条记录吗？')) return
  
  try {
    await axios.delete(`http://localhost:5000/delete_food_log/${logId}`)
    refreshData()
  } catch (error) {
    console.error('删除饮食记录失败:', error)
    alert('删除失败，请重试')
  }
}

// 刷新今日饮食记录
const refreshFoodLogs = async () => {
  await fetchTodayFoodLogs()
}

// 刷新所有数据
const refreshData = async () => {
  await fetchTodayFoodLogs()
  await fetchUserStats()
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

// 组件挂载时获取数据
onMounted(() => {
  if (userId.value) {
    refreshData()
  }
})
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background-color: #f9f9f9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-title {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.add-log-btn, .edit-log-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.add-log-btn {
  background: #4CAF50;
  color: white;
}

.edit-log-btn {
  background: #f0f0f0;
  color: #333;
}

.food-log-section, .data-visualization-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.food-log-section h2, .data-visualization-section h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.food-log-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.refresh-btn, .add-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
}

.refresh-btn {
  background: #f0f0f0;
  color: #333;
}

.add-btn {
  background: #4CAF50;
  color: white;
}

.food-log-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
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

.total-row {
  font-weight: 600;
  background-color: #f5f5f5;
}

.delete-btn {
  padding: 0.25rem 0.5rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
}

.loading, .no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .stats-grid, .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
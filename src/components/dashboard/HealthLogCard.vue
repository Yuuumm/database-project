<template>
    <div class="health-log-card">
      <div class="card-header">
        <h4>健康日志</h4>
        <button @click="showForm" class="add-btn">记录</button>
      </div>
      
      <div v-if="loading" class="loading">
        加载中...
      </div>
      
      <div v-else-if="!todayLog" class="no-data">
        今日暂无记录
      </div>
      
      <div v-else class="log-data">
        <div class="log-item">
          <span class="label">体重</span>
          <span class="value">{{ todayLog.weight }} kg</span>
        </div>
        
        <div v-if="todayLog.mood" class="log-item">
          <span class="label">情绪</span>
          <span class="value">{{ getMoodText(todayLog.mood) }}</span>
        </div>
        
        <div v-if="todayLog.sleep_hours" class="log-item">
          <span class="label">睡眠时长</span>
          <span class="value">{{ todayLog.sleep_hours }} 小时</span>
        </div>
        
        <div v-if="todayLog.sleep_start && todayLog.sleep_end" class="log-item">
          <span class="label">睡眠时段</span>
          <span class="value">{{ formatTime(todayLog.sleep_start) }} - {{ formatTime(todayLog.sleep_end) }}</span>
        </div>
      </div>
    </div>
    
    <Modal v-if="showHealthLogForm" @close="showHealthLogForm = false">
      <HealthLogForm 
        @submit="handleAddHealthLog" 
        @close="showHealthLogForm = false" 
      />
    </Modal>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'
  import Modal from '@/components/common/Modal.vue'
  import HealthLogForm from '@/components/forms/HealthLogForm.vue'
  import axios from 'axios'
  
  const userStore = useUserStore()
  const loading = ref(false)
  const todayLog = ref(null)
  const showHealthLogForm = ref(false)
  
  // 获取今天的日期
  const today = new Date().toISOString().split('T')[0]
  
  // 加载今日健康日志
  const loadTodayLog = async () => {
    if (!userStore.userId) return
    
    loading.value = true
    try {
      const response = await axios.get(`http://localhost:5000/get_health_log?user_id=${userStore.userId}&date=${today}`)
      todayLog.value = response.data.health_log
    } catch (error) {
      console.error('获取健康日志失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 提交健康日志
  const handleAddHealthLog = async (formData) => {
    try {
      await axios.post('http://localhost:5000/add_health_log', {
        user_id: userStore.userId,
        ...formData
      })
      await loadTodayLog() // 重新加载数据
    } catch (error) {
      console.error('添加健康日志失败:', error)
      alert('添加健康日志失败，请重试')
    }
  }
  
  // 显示表单
  const showForm = () => {
    showHealthLogForm.value = true
  }
  
  // 格式化情绪文本
  const getMoodText = (mood) => {
    const moodMap = {
      'excellent': '非常好',
      'good': '良好',
      'normal': '一般',
      'bad': '不佳',
      'terrible': '很差'
    }
    return moodMap[mood] || mood
  }
  
  // 格式化时间
  const formatTime = (timeStr) => {
    const [hours, minutes] = timeStr.split(':')
    return `${hours}:${minutes}`
  }
  
  onMounted(() => {
    loadTodayLog()
  })
  </script>
  
  <style scoped>
  .health-log-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .card-header h4 {
    color: #2c3e50;
    margin: 0;
  }
  
  .add-btn {
    padding: 0.25rem 0.75rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.875rem;
    cursor: pointer;
  }
  
  .log-data {
    display: grid;
    gap: 0.75rem;
  }
  
  .log-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .log-item .label {
    color: #666;
  }
  
  .log-item .value {
    font-weight: 500;
    color: #2c3e50;
  }
  
  .loading, .no-data {
    text-align: center;
    padding: 1.5rem 0;
    color: #666;
  }
  </style>
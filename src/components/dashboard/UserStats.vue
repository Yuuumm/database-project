<!-- src/components/dashboard/UserStats.vue -->
<template>
    <div class="user-stats">
      <div class="stat-card">
        <h4>每日目标摄入</h4>
        <div class="stat-value">{{ stats.targetCalories }} kcal</div>
      <div class="stat-progress">
        <div 
          class="progress-bar" 
          :style="{ width: `${caloriesProgress}%` }"
          :class="{ 'over': caloriesProgress > 100 }"
        ></div>
      </div>
      <div class="stat-detail">
        已摄入: {{ stats.consumedCalories }} kcal
      </div>
    </div>
  
  
      <div class="stat-card">
        <h4>BMI 指数</h4>
        <div class="stat-value">{{ stats.bmi }}</div>
        <div class="bmi-status">{{ bmiStatus }}</div>
      </div>
  
      <div class="stat-card">
        <h4>体重记录</h4>
        <div class="stat-value">{{ stats.weight }} kg</div>
        <!-- 移除体重趋势显示 -->
        <!-- <div class="weight-trend">
          <span :class="weightTrendClass">
            {{ weightTrendText }}
          </span>
        </div> -->
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    stats: {
      type: Object,
      required: true,
      default: () => ({
        targetCalories: 0,
        consumedCalories: 0,
        bmi: 0,
        weight: 0,
        previousWeight: 0
      })
    }
  })
  
// 计算卡路里进度
const caloriesProgress = computed(() => {
  if (!props.stats.targetCalories) return 0
  return Math.min(
    (props.stats.consumedCalories / props.stats.targetCalories) * 100,
    100
  )
})
  
  const bmiStatus = computed(() => {
    const bmi = props.stats.bmi
    if (bmi < 18.5) return '体重偏低'
    if (bmi < 24) return '体重正常'
    if (bmi < 28) return '体重偏高'
    return '肥胖'
  })
  
  const weightTrendClass = computed(() => {
    const diff = props.stats.weight - props.stats.previousWeight
    if (diff > 0) return 'trend-up'
    if (diff < 0) return 'trend-down'
    return 'trend-stable'
  })
  
  const weightTrendText = computed(() => {
    const diff = props.stats.weight - props.stats.previousWeight
    if (diff === 0) return '体重稳定'
    return `${Math.abs(diff)} kg ${diff > 0 ? '增加' : '减少'}`
  })
  </script>
  
  <style scoped>
  .user-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
  }
  
  .stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #2c3e50;
    margin: 0.5rem 0;
  }
  
  .stat-progress {
    height: 8px;
    background: #eee;
    border-radius: 4px;
    margin: 0.5rem 0;
  }
  
  .progress-bar {
    height: 100%;
    background: #4CAF50;
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  
  .progress-bar.over {
    background: #dc3545;
  }
  
  .stat-detail {
    font-size: 0.9rem;
    color: #666;
  }
  
  .bmi-status {
    color: #666;
    font-size: 0.9rem;
  }
  
  .weight-trend {
    font-size: 0.9rem;
  }
  
  .trend-up {
    color: #dc3545;
  }
  
  .trend-down {
    color: #28a745;
  }
  
  .trend-stable {
    color: #666;
  }
  </style>
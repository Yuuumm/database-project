<template>
    <div class="chart-container">
      <h3>近7天卡路里摄入</h3>
      <div v-if="loading" class="loading">
        加载中...
      </div>
      <div v-else-if="!hasData" class="no-data">
        暂无数据
      </div>
      <div v-else ref="chartContainer" class="chart"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
  import * as echarts from 'echarts/core'
  import { BarChart } from 'echarts/charts'
  import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    TransformComponent
  } from 'echarts/components'
  import { CanvasRenderer } from 'echarts/renderers'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'
  
  // 注册必须的组件
  echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    TransformComponent,
    BarChart,
    CanvasRenderer
  ])
  
  const chartContainer = ref(null)
  let chart = null
  const userStore = useUserStore()
  const loading = ref(false)
  const caloriesData = ref([])
  
  // 是否有数据
  const hasData = computed(() => caloriesData.value.some(item => item.value > 0))
  
  // 获取过去7天的日期
  const getLast7Days = () => {
    const dates = []
    for (let i = 6; i >= 0; i--) {
      const d = new Date()
      d.setDate(d.getDate() - i)
      dates.push(d.toISOString().split('T')[0])
    }
    return dates
  }
  
  // 获取过去7天的卡路里摄入
  const fetchWeeklyCalories = async () => {
    if (!userStore.userId) return
    
    loading.value = true
    try {
      const dates = getLast7Days()
      const results = []
      
      // 获取每天的数据
      for (const date of dates) {
        try {
          const response = await axios.get(
            `http://localhost:5000/query_food_log?user_id=${userStore.userId}&date=${date}`
          )
          
          const logs = response.data.food_logs || []
          const totalCalories = logs.reduce((sum, log) => sum + Number(log.calories), 0)
          
          // 格式化日期为更易读的格式
          const displayDate = new Date(date).toLocaleDateString('zh-CN', { 
            month: 'numeric', 
            day: 'numeric'
          })
          
          results.push({
            date: displayDate,
            value: totalCalories
          })
        } catch (error) {
          console.error(`获取${date}的数据失败:`, error)
          results.push({
            date: new Date(date).toLocaleDateString('zh-CN', { 
              month: 'numeric', 
              day: 'numeric'
            }),
            value: 0
          })
        }
      }
      
      caloriesData.value = results
      updateChart()
    } catch (error) {
      console.error('获取每周卡路里数据失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 初始化图表
  const initChart = () => {
    if (chartContainer.value) {
      chart = echarts.init(chartContainer.value)
      updateChart()
    }
  }
  
  // 更新图表数据
  const updateChart = () => {
    if (!chart) return

    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: '{b}: {c} kcal'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: caloriesData.value.map(item => item.date),
        axisTick: {
          alignWithLabel: true
        }
      },
      yAxis: {
        type: 'value',
        name: '卡路里 (kcal)',
        nameLocation: 'end'
      },
      series: [
        {
          name: '卡路里摄入',
          type: 'bar',
          barWidth: '60%',
          data: caloriesData.value.map(item => item.value),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#2378f7' },
                { offset: 0.7, color: '#2378f7' },
                { offset: 1, color: '#83bff6' }
              ])
            }
          }
        }
      ]
    }

    chart.setOption(option)
  }
  
  // 处理窗口大小改变
  const handleResize = () => {
    if (chart) {
      chart.resize()
    }
  }
  
  onMounted(() => {
    fetchWeeklyCalories().then(() => {
      initChart()
    })
    window.addEventListener('resize', handleResize)
  })
  
  onBeforeUnmount(() => {
    if (chart) {
      chart.dispose()
      chart = null
    }
    window.removeEventListener('resize', handleResize)
  })
  </script>
  
  <style scoped>
  .chart-container {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    height: 100%;
  }
  
  h3 {
    text-align: center;
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 1rem;
  }
  
  .chart {
    height: 300px;
  }
  
  .loading, .no-data {
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #666;
  }
  </style>
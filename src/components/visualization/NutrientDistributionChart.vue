<template>
    <div class="chart-container">
      <h3>今日营养素分布</h3>
      <div v-if="!data.length" class="no-data">
        暂无数据
      </div>
      <div v-else ref="chartContainer" class="chart"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue'
  import * as echarts from 'echarts/core'
  import { PieChart } from 'echarts/charts'
  import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent
  } from 'echarts/components'
  import { CanvasRenderer } from 'echarts/renderers'
  
  // 注册必须的组件
  echarts.use([
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    PieChart,
    CanvasRenderer
  ])
  
  const props = defineProps({
    data: {
      type: Array,
      default: () => []
    }
  })
  
  const chartContainer = ref(null)
  let chart = null
  
  // 计算各营养素的总量
  const nutrients = computed(() => {
    if (!props.data.length) return []
  
    const totals = props.data.reduce((acc, item) => {
      return {
        protein: (acc.protein || 0) + Number(item.protein),
        carbs: (acc.carbs || 0) + Number(item.carbs),
        fats: (acc.fats || 0) + Number(item.fats),
        fiber: (acc.fiber || 0) + Number(item.fiber || 0)
      }
    }, {})
  
    // 转换为饼图所需的数据格式
    return [
      { value: totals.protein, name: '蛋白质' },
      { value: totals.carbs, name: '碳水化合物' },
      { value: totals.fats, name: '脂肪' },
      { value: totals.fiber, name: '膳食纤维' }
    ]
  })
  
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
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c}g ({d}%)'
      },
      legend: {
        orient: 'horizontal',
        bottom: 0,
        data: nutrients.value.map(item => item.name)
      },
      series: [
        {
          name: '营养素',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: nutrients.value,
          color: ['#91cc75', '#fac858', '#ee6666', '#73c0de']
        }
      ]
    }
  
    chart.setOption(option)
  }
  
  // 监听数据变化，更新图表
  watch(() => props.data, () => {
    if (chart) {
      updateChart()
    }
  }, { deep: true })
  
  // 处理窗口大小改变
  const handleResize = () => {
    if (chart) {
      chart.resize()
    }
  }
  
  onMounted(() => {
    initChart()
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
  
  .no-data {
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #666;
  }
  </style>
<!-- src/components/tables/FoodLogTable.vue -->
<template>
    <div class="food-log-table">
      <div class="table-header">
        <h3>{{ title }}</h3>
        <div class="table-actions" v-if="showActions">
          <button @click="$emit('refresh')">刷新</button>
          <button @click="$emit('add')">添加记录</button>
        </div>
      </div>
  
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>餐次</th>
              <th>食物</th>
              <th>卡路里(kcal)</th>
              <th>蛋白质(g)</th>
              <th>碳水(g)</th>
              <th>脂肪(g)</th>
              <th v-if="showActions">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!foodLogs || foodLogs.length === 0">
              <td colspan="7" class="no-data">暂无记录</td>
            </tr>
            <tr v-for="log in foodLogs" :key="log.id">
              <td>{{ getMealName(log.meal) }}</td>
              <td>{{ log.food_item }}</td>
              <td>{{ log.calories }}</td>
              <td>{{ log.protein }}</td>
              <td>{{ log.carbs }}</td>
              <td>{{ log.fats }}</td>
              <td v-if="showActions" class="actions">
                <button 
                  class="delete-btn" 
                  @click="$emit('delete', log.id)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
          <tfoot v-if="showTotal && foodLogs.length > 0">
            <tr>
              <td colspan="2">总计</td>
              <td>{{ totals.calories }}</td>
              <td>{{ totals.protein }}</td>
              <td>{{ totals.carbs }}</td>
              <td>{{ totals.fats }}</td>
              <td v-if="showActions"></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    foodLogs: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: '饮食记录'
    },
    showActions: {
      type: Boolean,
      default: true
    },
    showTotal: {
      type: Boolean,
      default: true
    }
  })
  
  defineEmits(['delete', 'refresh', 'add'])
  
  const getMealName = (meal) => {
    const meals = {
      '1': '早餐',
      '2': '午餐',
      '3': '晚餐',
      '4': '加餐'
    }
    return meals[meal] || meal
  }
  
  const totals = computed(() => {
    return props.foodLogs.reduce((acc, log) => {
      return {
        calories: acc.calories + Number(log.calories),
        protein: acc.protein + Number(log.protein),
        carbs: acc.carbs + Number(log.carbs),
        fats: acc.fats + Number(log.fats)
      }
    }, { calories: 0, protein: 0, carbs: 0, fats: 0 })
  })
  </script>
  
  <style scoped>
  .food-log-table {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1rem;
    margin: 1rem 0;
  }
  
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .table-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .table-responsive {
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: center;
    border-bottom: 1px solid #eee;
  }
  
  th {
    background: #f8f9fa;
    font-weight: 600;
  }
  
  .no-data {
    text-align: center;
    color: #666;
    padding: 2rem;
  }
  
  .actions {
    white-space: nowrap;
  }
  
  .delete-btn {
    padding: 0.25rem 0.5rem;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .delete-btn:hover {
    background: #c82333;
  }
  
  tfoot td {
    font-weight: 600;
    background: #f8f9fa;
  }
  </style>
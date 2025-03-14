// src/stores/foodLog.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'

const API_URL = 'http://127.0.0.1:5000'

// 创建axios实例
const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export const useFoodLogStore = defineStore('foodLog', {
  state: () => ({
    todayLogs: [],
    historyLogs: {},
    loading: false
  }),

  getters: {
    getTodayTotal: (state) => {
      return state.todayLogs.reduce((acc, log) => {
        return {
          calories: acc.calories + Number(log.calories),
          protein: acc.protein + Number(log.protein),
          carbs: acc.carbs + Number(log.carbs),
          fats: acc.fats + Number(log.fats)
        }
      }, { calories: 0, protein: 0, carbs: 0, fats: 0 })
    }
  },

  actions: {
    async getTodayLogs() {
      const userStore = useUserStore()
      const today = new Date().toISOString().split('T')[0]
      
      try {
        const response = await axiosInstance.get(
          `/query_food_log?user_id=${userStore.userId}&date=${today}`
        )
        this.todayLogs = response.data.food_logs
        return this.todayLogs
      } catch (error) {
        console.error('获取今日饮食记录失败:', error)
        return []
      }
    },

    async getLogsByDate(date) {
      const userStore = useUserStore()
      
      try {
        const response = await axiosInstance.get(
          `/query_food_log?user_id=${userStore.userId}&date=${date}`
        )
        this.historyLogs[date] = response.data.food_logs
        return response.data.food_logs
      } catch (error) {
        console.error('获取饮食记录失败:', error)
        return []
      }
    },

    async addFoodLog(foodLog) {
      const userStore = useUserStore()
      
      try {
        const response = await axiosInstance.post('/add_food_log', {
          user_id: userStore.userId,
          date: new Date().toISOString().split('T')[0],  // 确保日期格式正确
          ...foodLog
        })
        
        // 刷新今日记录
        await this.getTodayLogs()
        return response.data
      } catch (error) {
        console.error('添加饮食记录失败:', error.response || error)
        throw new Error(error.response?.data?.message || '网络错误，请稍后重试')
      }
    },

    async deleteFoodLog(logId) {
      try {
        const response = await axiosInstance.delete(`/delete_food_log/${logId}`)
        await this.getTodayLogs()
        return response.data
      } catch (error) {
        throw new Error(error.response?.data?.message || '删除饮食记录失败')
      }
    },
    
    async addHealthLog(healthLog) {
      const userStore = useUserStore()
      
      try {
        const response = await axiosInstance.post(`/add_health_log`, {
          user_id: userStore.userId,
          date: new Date().toISOString().split('T')[0],
          ...healthLog
        })
        return response.data
      } catch (error) {
        console.error('添加健康日志失败:', error.response || error)
        throw new Error(error.response?.data?.message || '网络错误，请稍后重试')
      }
    }
  }
})
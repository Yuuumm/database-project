// src/stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000'

const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export const useUserStore = defineStore('user', {
  state: () => ({
    userId: localStorage.getItem('user_id') || null,
    userInfo: null,
    isLoggedIn: !!localStorage.getItem('user_id'),
    userData: null,
    loading: false,
    error: null
  }),

  getters: {
    getUserId: (state) => state.userId,
    getUserInfo: (state) => state.userInfo
  },

  actions: {
    async login({ username, password }) {
      try {
        const response = await axiosInstance.post('/login', {
          username,
          password
        })
        
        this.userId = response.data.user_id
        this.isLoggedIn = true
        localStorage.setItem('user_id', this.userId)
        
        await this.fetchUserInfo()
        return response.data
      } catch (error) {
        throw new Error(error.response?.data?.message || '登录失败')
      }
    },

    async register(userData) {
      try {
        const response = await axiosInstance.post(`${API_URL}/register`, userData)
        return response.data
      } catch (error) {
        throw new Error(error.response?.data?.message || '注册失败')
      }
    },

    async fetchUserInfo() {
      if (!this.userId) return null
      
      try {
        const response = await axiosInstance.get(`${API_URL}/user/${this.userId}`)
        this.userInfo = response.data
        return response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    },

    async updateUserInfo(userData) {
      try {
        const response = await axiosInstance.put(
          `${API_URL}/update_user_info/${this.userId}`,
          userData
        )
        await this.fetchUserInfo()
        return response.data
      } catch (error) {
        throw new Error(error.response?.data?.message || '更新用户信息失败')
      }
    },

    async getUserStats() {
      try {
        const response = await axiosInstance.get(`${API_URL}/user_intake/${this.userId}`)
        return response.data
      } catch (error) {
        console.error('获取用户统计数据失败:', error)
        return null
      }
    },

    logout() {
      this.userId = null
      this.userInfo = null
      this.isLoggedIn = false
      localStorage.removeItem('user_id')
    },

    async fetchUserProfile() {
      this.loading = true
      this.error = null
      
      try {
        // 这里使用模拟数据，实际项目中应该连接到后端API
        // const response = await axios.get('/api/user/profile')
        
        // 模拟网络请求延迟
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 使用模拟数据
        const mockUserData = {
          id: 1,
          name: '测试用户',
          email: 'test@example.com',
          age: 23,
          gender: '女',
          height: 175,
          weight: 60,
          targetCalories: 2000,
          dietaryPreferences: ['均衡饮食'],
          healthGoals: ['保持健康']
        }
        
        this.userData = mockUserData
        this.isLoggedIn = true
      } catch (error) {
        console.error('获取用户资料错误:', error)
        this.error = error.message || '获取用户资料失败'
      } finally {
        this.loading = false // 确保无论成功或失败都会重置loading状态
      }
    },
    
    // 初始化方法，用于应用启动时检查登录状态
    init() {
      // 这里可以检查本地存储中的token等
      // 目前先默认为登录状态以便测试
      this.isLoggedIn = true
      this.fetchUserProfile()
    }
  }
})
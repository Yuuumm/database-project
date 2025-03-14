<!-- src/views/ProfileView.vue -->
<template>
    <div class="profile-view">
      <AppHeader />
      
      <main class="profile-content">
        <div class="container">
          <h1>个人资料</h1>
          
          <div class="profile-card" v-if="userInfo">
            <form @submit.prevent="handleSubmit" class="profile-form">
              <div class="form-group">
                <label for="name">姓名</label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="form.name"
                  required
                >
              </div>
  
              <div class="form-group">
                <label for="email">邮箱</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="form.email"
                  required
                >
              </div>
  
              <div class="form-group">
                <label for="gender">性别</label>
                <select id="gender" v-model="form.gender" required>
                  <option value="female">女</option>
                  <option value="male">男</option>
                </select>
              </div>
  
              <div class="form-row">
                <div class="form-group">
                  <label for="weight">体重（kg）</label>
                  <input 
                    type="number" 
                    id="weight" 
                    v-model="form.weight"
                    step="0.1"
                    required
                  >
                </div>
  
                <div class="form-group">
                  <label for="height">身高（cm）</label>
                  <input 
                    type="number" 
                    id="height" 
                    v-model="form.height"
                    required
                  >
                </div>
              </div>
  
              <div class="form-group">
                <label for="laborIntensity">每日劳动强度</label>
                <select id="laborIntensity" v-model="form.laborIntensity" required>
                  <option value="brain-domain">脑力为主</option>
                  <option value="labor-domain">体力为主</option>
                  <option value="half">轻度劳动</option>
                </select>
              </div>
  
              <div class="form-actions">
                <button type="submit" :disabled="loading">
                  {{ loading ? '保存中...' : '保存修改' }}
                </button>
              </div>
            </form>
          </div>
  
          <div v-else class="loading">
            加载中...
          </div>
        </div>
      </main>
  
      <AppFooter />
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'
  import AppHeader from '@/components/common/AppHeader.vue'
  import AppFooter from '@/components/common/AppFooter.vue'
  
  const userStore = useUserStore()
  const loading = ref(false)
  const userInfo = ref(null)

  const form = reactive({
    name: '',
    email: '',
    gender: 'female',
    weight: '',
    height: '',
    laborIntensity: 'brain-domain'
  })
  
  onMounted(async () => {
    await loadUserInfo()
  })
  
  async function loadUserInfo() {
    try {
      const info = await userStore.fetchUserInfo()
      if (info) {
        userInfo.value = info
        Object.assign(form, info)
      }
    } catch (error) {
      console.error('加载用户信息失败:', error)
    }
  }
  
  async function handleSubmit() {
    loading.value = true
    try {
      await userStore.updateUserInfo(form)
      alert('个人资料更新成功')
    } catch (error) {
      alert(error.message)
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .profile-view {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .profile-content {
    flex: 1;
    padding: 2rem 0;
    background: #f4f4f9;
  }
  
  .profile-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    max-width: 600px;
    margin: 2rem auto;
  }
  
  .profile-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-row {
    display: flex;
    gap: 1rem;
  }
  
  .form-row .form-group {
    flex: 1;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #666;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-actions {
    margin-top: 1rem;
  }
  
  .form-actions button {
    width: 100%;
    padding: 0.75rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .form-actions button:hover {
    background: #45a049;
  }
  
  .form-actions button:disabled {
    background: #cccccc;
    cursor: not-allowed;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
    color: #666;
  }
  </style>
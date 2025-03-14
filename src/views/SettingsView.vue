<!-- src/views/SettingsView.vue -->
<template>
    <div class="settings-view">
      <AppHeader />
      
      <main class="settings-content">
        <div class="container">
          <h1>设置</h1>
          
          <div class="settings-card">
            <h2>账户设置</h2>
            
            <!-- 修改密码表单 -->
            <form @submit.prevent="handleChangePassword" class="settings-form">
              <div class="form-group">
                <label for="currentPassword">当前密码</label>
                <input 
                  type="password" 
                  id="currentPassword" 
                  v-model="passwordForm.currentPassword"
                  required
                >
              </div>
  
              <div class="form-group">
                <label for="newPassword">新密码</label>
                <input 
                  type="password" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword"
                  required
                >
                <small>密码至少8位，包含数字和字母</small>
              </div>
  
              <div class="form-group">
                <label for="confirmPassword">确认新密码</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword"
                  required
                >
              </div>
  
              <button type="submit" :disabled="passwordLoading">
                {{ passwordLoading ? '修改中...' : '修改密码' }}
              </button>
            </form>
          </div>
  
          <div class="settings-card">
            <h2>通知设置</h2>
            <div class="settings-options">
              <div class="setting-item">
                <label class="switch">
                  <input 
                    type="checkbox" 
                    v-model="notifications.email"
                    @change="saveNotificationSettings"
                  >
                  <span class="slider"></span>
                </label>
                <span>接收邮件通知</span>
              </div>
  
              <div class="setting-item">
                <label class="switch">
                  <input 
                    type="checkbox" 
                    v-model="notifications.dailyReminder"
                    @change="saveNotificationSettings"
                  >
                  <span class="slider"></span>
                </label>
                <span>每日提醒记录饮食</span>
              </div>
            </div>
          </div>
  
          <div class="settings-card danger-zone">
            <h2>危险区域</h2>
            <button 
              class="delete-account" 
              @click="confirmDeleteAccount"
            >
              删除账户
            </button>
            <p class="warning">
              注意：账户删除后无法恢复，所有数据将永久丢失
            </p>
          </div>
        </div>
      </main>
  
      <AppFooter />
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import AppHeader from '@/components/common/AppHeader.vue'
  import AppFooter from '@/components/common/AppFooter.vue'
  
  const router = useRouter()
  const userStore = useUserStore()
  const passwordLoading = ref(false)
  
  const passwordForm = reactive({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  
  const notifications = reactive({
    email: true,
    dailyReminder: true
  })
  
  async function handleChangePassword() {
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      alert('两次输入的密码不一致')
      return
    }
  
    passwordLoading.value = true
    try {
      // 实现修改密码的逻辑
      await userStore.changePassword(passwordForm)
      alert('密码修改成功')
      passwordForm.currentPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    } catch (error) {
      alert(error.message)
    } finally {
      passwordLoading.value = false
    }
  }
  
  async function saveNotificationSettings() {
    try {
      // 实现保存通知设置的逻辑
      await userStore.updateNotificationSettings(notifications)
    } catch (error) {
      console.error('保存通知设置失败:', error)
    }
  }
  
  function confirmDeleteAccount() {
    if (confirm('确定要删除账户吗？此操作不可恢复！')) {
      try {
        // 实现删除账户的逻辑
        userStore.deleteAccount()
        router.push('/login')
      } catch (error) {
        alert(error.message)
      }
    }
  }
  </script>
  
  <style scoped>
  .settings-view {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .settings-content {
    flex: 1;
    padding: 2rem 0;
    background: #f4f4f9;
  }
  
  .settings-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
  }
  
  .settings-form {
    max-width: 400px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-group small {
    display: block;
    color: #666;
    margin-top: 0.25rem;
  }
  
  button {
    padding: 0.75rem 1.5rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:disabled {
    background: #cccccc;
    cursor: not-allowed;
  }
  
  .setting-item {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
    margin-right: 1rem;
  }
  
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
  }
  
  .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }
  
  input:checked + .slider {
    background-color: #4CAF50;
  }
  
  input:checked + .slider:before {
    transform: translateX(26px);
  }
  
  .danger-zone {
    border: 1px solid #dc3545;
  }
  
  .delete-account {
    background: #dc3545;
  }
  
  .delete-account:hover {
    background: #c82333;
  }
  
  .warning {
    color: #dc3545;
    margin-top: 0.5rem;
    font-size: 0.9rem;
  }
  </style>
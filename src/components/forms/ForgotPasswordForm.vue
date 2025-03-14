<!-- src/components/forms/ForgotPasswordForm.vue -->
<template>
    <div class="forgot-password-form">
      <h2>重置密码</h2>
      <p class="description">
        请输入您的注册邮箱，我们将发送重置密码链接到您的邮箱。
      </p>
  
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">邮箱地址</label>
          <input 
            type="email" 
            id="email" 
            v-model="email"
            required
            placeholder="请输入注册邮箱"
          >
        </div>
  
        <div class="form-actions">
          <button type="submit" :disabled="loading">
            {{ loading ? '发送中...' : '发送重置链接' }}
          </button>
          <button 
            type="button" 
            class="back-button"
            @click="$emit('switch-form', 'login')"
          >
            返回登录
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const emit = defineEmits(['submit', 'switch-form'])
  const loading = ref(false)
  const email = ref('')
  
  async function handleSubmit() {
    loading.value = true
    try {
      await emit('submit', { email: email.value })
      email.value = '' // 清空表单
    } catch (error) {
      console.error('重置密码失败:', error)
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .forgot-password-form {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .description {
    color: #666;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #4CAF50;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
  }
  
  .form-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  button[type="submit"] {
    background: #4CAF50;
    color: white;
  }
  
  button[type="submit"]:hover {
    background: #45a049;
  }
  
  button[type="submit"]:disabled {
    background: #cccccc;
    cursor: not-allowed;
  }
  
  .back-button {
    background: #f5f5f5;
    color: #666;
  }
  
  .back-button:hover {
    background: #e0e0e0;
  }
  </style>
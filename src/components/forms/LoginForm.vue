<!-- src/components/forms/LoginForm.vue -->
<template>
    <form @submit.prevent="handleSubmit" class="login-form">
      <div class="form-group">
        <label for="username">用户名</label>
        <input 
          type="text" 
          id="username" 
          v-model="form.username" 
          required
        >
      </div>
      
      <div class="form-group">
        <label for="password">密码</label>
        <input 
          type="password" 
          id="password" 
          v-model="form.password" 
          required
        >
      </div>
  
      <div class="form-actions">
        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        <button type="button" @click="$emit('switch-form', 'register')">
          注册新账号
        </button>
      </div>
    </form>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue'
  
  const emit = defineEmits(['submit', 'switch-form'])
  const loading = ref(false)
  const form = reactive({
    username: '',
    password: ''
  })
  
  const handleSubmit = async () => {
    loading.value = true
    try {
      await emit('submit', { ...form })
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .login-form {
    max-width: 400px;
    margin: 0 auto;
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
  
  .form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"] {
    background: #4CAF50;
    color: white;
  }
  
  button[type="button"] {
    background: #f5f5f5;
    color: #666;
  }
  </style>
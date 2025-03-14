<!-- src/components/forms/RegisterForm.vue -->
<template>
    <form @submit.prevent="handleSubmit" class="register-form">
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
        <small>密码至少8位，包含数字和字母</small>
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
        <label for="name">姓名</label>
        <input 
          type="text" 
          id="name" 
          v-model="form.name"
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
  
      <div class="form-group">
        <label for="weight">体重（kg）</label>
        <input 
          type="number" 
          id="weight" 
          v-model="form.weight"
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
          {{ loading ? '注册中...' : '注册' }}
        </button>
        <button type="button" @click="$emit('switch-form', 'login')">
          返回登录
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
    password: '',
    email: '',
    name: '',
    gender: 'female',
    weight: '',
    height: '',
    laborIntensity: 'brain-domain'
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
  .register-form {
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
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-group small {
    display: block;
    color: #666;
    margin-top: 0.25rem;
    font-size: 0.875rem;
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
  
  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  </style>
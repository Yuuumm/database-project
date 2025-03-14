<!-- src/views/LoginView.vue -->
<template>
    <div class="login-view">
      <div class="login-container">
        <h1>健康饮食管理系统</h1>
        
        <div v-if="currentForm === 'login'">
          <LoginForm 
            @submit="handleLogin"
            @switch-form="switchForm"
          />
          <div class="form-links">
            <a href="#" @click.prevent="currentForm = 'forgot'">忘记密码？</a>
          </div>
        </div>
  
        <div v-else-if="currentForm === 'register'">
          <RegisterForm 
            @submit="handleRegister"
            @switch-form="switchForm"
          />
        </div>
  
        <div v-else>
          <ForgotPasswordForm 
            @submit="handleForgotPassword"
            @switch-form="switchForm"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import LoginForm from '@/components/forms/LoginForm.vue'
  import RegisterForm from '@/components/forms/RegisterForm.vue'
  import ForgotPasswordForm from '@/components/forms/ForgotPasswordForm.vue'
  
  const router = useRouter()
  const userStore = useUserStore()
  const currentForm = ref('login')
  
  const switchForm = (formName) => {
    currentForm.value = formName
  }
  
  const handleLogin = async (credentials) => {
    try {
      await userStore.login(credentials)
      router.push('/dashboard')
    } catch (error) {
      alert(error.message)
    }
  }
  
  const handleRegister = async (userData) => {
    try {
      await userStore.register(userData)
      alert('注册成功！请登录')
      currentForm.value = 'login'
    } catch (error) {
      alert(error.message)
    }
  }
  
  const handleForgotPassword = async (email) => {
    try {
      // 实现忘记密码逻辑
      alert('重置密码链接已发送到您的邮箱')
      currentForm.value = 'login'
    } catch (error) {
      alert(error.message)
    }
  }
  </script>
  
  <style scoped>
  .login-view {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f4f9;
  }
  
  .login-container {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
  }
  
  .form-links {
    text-align: center;
    margin-top: 1rem;
  }
  
  .form-links a {
    color: #4CAF50;
    text-decoration: none;
  }
  
  .form-links a:hover {
    text-decoration: underline;
  }
  </style>
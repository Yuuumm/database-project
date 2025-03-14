<!-- src/components/common/AppHeader.vue -->
<template>
    <header class="app-header">
      <nav>
        <router-link to="/" class="logo">健康饮食管理系统</router-link>
        <div class="nav-links" v-if="userStore.isLoggedIn">
          <router-link to="/dashboard">仪表盘</router-link>
          <router-link to="/profile">个人信息</router-link>
          <a href="#" @click.prevent="handleLogout">退出</a>
        </div>
      </nav>
    </header>
  </template>
  
  <script setup>
  import { useUserStore } from '@/stores/user'
  import { useRouter } from 'vue-router'
  
  const userStore = useUserStore()
  const router = useRouter()
  
  const handleLogout = () => {
    userStore.logout()
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .app-header {
    background: #fff;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .nav-links a {
    margin-left: 1.5rem;
    color: #666;
    text-decoration: none;
  }
  
  .nav-links a:hover {
    color: #4CAF50;
  }
  
  .logo {
    font-size: 1.2rem;
    font-weight: bold;
    color: #4CAF50;
    text-decoration: none;
  }
  </style>
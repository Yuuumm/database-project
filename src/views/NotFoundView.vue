<!-- src/views/NotFoundView.vue -->
<template>
    <div class="not-found">
      <div class="content">
        <h1>404</h1>
        <h2>页面未找到</h2>
        <p>抱歉，您访问的页面不存在</p>
        <div class="actions">
          <router-link to="/" class="home-link">返回首页</router-link>
          <button @click="goBack" class="back-button">返回上一页</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const goBack = () => {
    router.back()
  }
  </script>
  
  <style scoped>
  .not-found {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f4f9;
  }
  
  .content {
    text-align: center;
    padding: 2rem;
  }
  
  h1 {
    font-size: 6rem;
    color: #4CAF50;
    margin: 0;
    line-height: 1;
  }
  
  h2 {
    font-size: 2rem;
    color: #2c3e50;
    margin: 1rem 0;
  }
  
  p {
    color: #666;
    margin-bottom: 2rem;
  }
  
  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
  
  .home-link,
  .back-button {
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
  }
  
  .home-link {
    background: #4CAF50;
    color: white;
  }
  
  .back-button {
    background: #f5f5f5;
    color: #666;
    border: none;
    cursor: pointer;
  }
  
  .home-link:hover {
    background: #45a049;
  }
  
  .back-button:hover {
    background: #e0e0e0;
  }
  </style>
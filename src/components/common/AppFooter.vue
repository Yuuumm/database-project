<!-- src/components/common/AppFooter.vue -->
<template>
    <footer class="app-footer">
      <div class="footer-content">
        <p>&copy; {{ currentYear }} 健康饮食管理系统</p>
        <div class="footer-links">
          <a href="#" @click.prevent="showAbout">关于我们</a>
          <a href="#" @click.prevent="showPrivacy">隐私政策</a>
          <a href="#" @click.prevent="showContact">联系我们</a>
        </div>
      </div>
    </footer>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const currentYear = computed(() => new Date().getFullYear())
  
  const showAbout = () => {
    // 实现关于我们的逻辑
    console.log('显示关于我们')
  }
  
  const showPrivacy = () => {
    // 实现隐私政策的逻辑
    console.log('显示隐私政策')
  }
  
  const showContact = () => {
    // 实现联系我们的逻辑
    console.log('显示联系方式')
  }
  </script>
  
  <style scoped>
  .app-footer {
    background: #f8f9fa;
    padding: 1.5rem 0;
    margin-top: 2rem;
    border-top: 1px solid #eee;
  }
  
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
  }
  
  .footer-links {
    display: flex;
    gap: 1.5rem;
  }
  
  .footer-links a {
    color: #666;
    text-decoration: none;
    font-size: 0.9rem;
  }
  
  .footer-links a:hover {
    color: #4CAF50;
  }
  </style>
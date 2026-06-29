<template>
  <div class="graph-panel">
    <div class="header">
      <div>
        <h1>能力图谱</h1>
        <p>可视化展示个人技能结构与发展趋势</p>
      </div>
      <div class="user-info-bar">
        <span class="user-name">{{ username }}</span>
        <div class="user-avatar">{{ userInitial }}</div>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </div>
    </div>

    <div class="placeholder-card">
      <div class="placeholder-icon">🔗</div>
      <div class="placeholder-text">能力图谱 功能开发中，敬请期待...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.graph-panel {
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
}

.header p {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

.user-info-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info-bar .user-name {
  font-size: 14px;
  color: #1a1a1a;
  font-weight: 500;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.logout-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.placeholder-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.placeholder-text {
  font-size: 16px;
  color: #999;
}
</style>

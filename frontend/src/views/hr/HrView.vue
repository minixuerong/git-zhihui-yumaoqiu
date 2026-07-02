<template>
  <div class="hr-page">
    <div class="empty-state">
      <div class="empty-icon">HR</div>
      <h2>招聘者工作台</h2>
      <p>功能开发中，敬请期待...</p>
      <el-button @click="userStore.logout(); router.push('/login')">退出登录</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
</script>

<style scoped>
.hr-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}

.empty-state {
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin: 0 auto 16px;
}

.empty-state h2 {
  font-size: 20px;
  color: #1e293b;
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 14px;
  color: #94a3b8;
  margin: 0 0 24px;
}
</style>

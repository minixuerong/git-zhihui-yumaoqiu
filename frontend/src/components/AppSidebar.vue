<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Logo -->
    <div class="logo">CAPABILITY<span class="logo-highlight">.BRAIN</span></div>

    <!-- 导航菜单 -->
    <nav>
      <a
        v-for="item in menuItems"
        :key="item.key"
        href="javascript:void(0)"
        class="nav-item"
        :class="{ active: activeTab === item.key }"
        @click="$emit('tab-change', item.key)"
      >
        <span class="nav-icon" v-if="item.icon" v-html="item.icon"></span>
        <span class="nav-text">{{ item.label }}</span>
      </a>

      <div class="nav-divider" v-if="dividerItems.length"></div>

      <a
        v-for="item in dividerItems"
        :key="item.key"
        href="javascript:void(0)"
        class="nav-item"
        :class="{ active: activeTab === item.key }"
        @click="$emit('tab-change', item.key)"
      >
        <span class="nav-icon" v-if="item.icon" v-html="item.icon"></span>
        <span class="nav-text">{{ item.label }}</span>
      </a>

      <div class="nav-divider"></div>

      <a href="javascript:void(0)" class="nav-item disabled">
        <span class="nav-text">系统设置</span>
      </a>
      <a href="javascript:void(0)" class="nav-item disabled">
        <span class="nav-text">帮助文档</span>
      </a>
    </nav>

    <!-- 底部用户信息 -->
    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">A</div>
        <div class="user-detail">
          <div class="user-name">管理员</div>
          <div class="user-role">管理员</div>
        </div>
      </div>
      <button class="logout-btn" @click="handleLogout">
        <span>退出登录</span>
      </button>
    </div>

    <!-- 折叠按钮 -->
    <div class="toggle-btn" @click="isCollapsed = !isCollapsed"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
  activeTab: string
}>()

defineEmits<{
  'tab-change': [tab: string]
}>()

const router = useRouter()
const userStore = useUserStore()
const isCollapsed = ref(false)

const menuItems = [
  { key: 'dashboard', label: '数据概览', icon: '' },
  { key: 'job-management', label: '岗位数据管理', icon: '' },
  { key: 'skill-management', label: '技能数据管理', icon: '' },
  { key: 'user-management', label: '用户管理', icon: '' }
]

const dividerItems = [
  { key: 'update-config', label: '更新时间配置', icon: '' },
  { key: 'schedule-config', label: '循环任务配置', icon: '' }
]

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 220px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 16px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.03);
}

.sidebar.collapsed {
  width: 56px;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 24px;
  letter-spacing: -0.3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 8px 12px;
}

.logo-highlight {
  color: #3b82f6;
}

.sidebar.collapsed .logo {
  font-size: 20px;
  text-align: center;
  padding: 8px;
  margin-bottom: 20px;
}

.sidebar.collapsed .logo-highlight {
  display: none;
}

nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

nav::-webkit-scrollbar { width: 4px; }
nav::-webkit-scrollbar-track { background: transparent; }
nav::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 2px; }
nav::-webkit-scrollbar-thumb:hover { background: #9ca3af; }

.nav-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  color: #6b7280;
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 2px;
  border-radius: 6px;
  transition: all 0.2s ease;
  white-space: nowrap;
  cursor: pointer;
  position: relative;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2px;
  height: 0;
  background: #3b82f6;
  border-radius: 0 1px 1px 0;
  transition: height 0.2s ease;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-item:hover::before { height: 20px; }

.nav-item.active {
  background: #eff6ff;
  color: #3b82f6;
  font-weight: 500;
}

.nav-item.active::before { height: 20px; }

.nav-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-item.disabled:hover {
  background: transparent;
  color: #6b7280;
}

.nav-text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 12px 8px;
}

/* Footer */
.sidebar-footer {
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  margin-top: auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.user-detail { flex: 1; overflow: hidden; }
.user-name { font-size: 13px; font-weight: 600; color: #1f2937; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: #9ca3af; }

.sidebar.collapsed .user-detail { display: none; }
.sidebar.collapsed .user-info { justify-content: center; padding: 8px; }

.logout-btn {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  background: #ffffff;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.sidebar.collapsed .logout-btn span { display: none; }

/* Toggle */
.toggle-btn {
  position: absolute;
  right: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 48px;
  border: 1px solid #e5e7eb;
  border-left: none;
  border-radius: 0 6px 6px 0;
  background: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #6b7280;
  transition: all 0.2s ease;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
}

.toggle-btn:hover { background: #f3f4f6; color: #3b82f6; }
.toggle-btn::before { content: '‹'; font-size: 16px; font-weight: 300; }
.sidebar.collapsed .toggle-btn::before { content: '›'; }

/* Responsive */
@media (max-width: 768px) {
  .sidebar { width: 56px; padding: 12px 4px; }
  .sidebar .logo { font-size: 20px; text-align: center; padding: 8px; margin-bottom: 16px; }
  .sidebar .logo-highlight { display: none; }
  .sidebar .nav-text { display: none; }
  .sidebar .nav-item { justify-content: center; padding: 10px; }
  .sidebar .nav-divider { margin: 8px 4px; }
  .sidebar .user-detail { display: none; }
  .sidebar .user-info { justify-content: center; padding: 6px; }
  .sidebar .logout-btn span { display: none; }
  .sidebar .logout-btn { padding: 8px; }
  .toggle-btn { display: none; }
}
</style>

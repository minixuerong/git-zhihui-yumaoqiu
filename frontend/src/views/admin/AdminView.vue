<template>
  <div class="admin-layout">
    <AppSidebar :active-tab="activeTab" @tab-change="activeTab = $event" />
    <div class="main-content">
      <div class="admin-page">
        <!-- Header -->
        <div class="page-header">
          <div>
            <h1>{{ pageTitle }}</h1>
            <p class="page-subtitle">{{ pageSubtitle }}</p>
          </div>
          <div class="header-right">
            <span class="admin-name">{{ currentUser?.username || '管理员' }}</span>
            <el-button @click="handleLogout">退出登录</el-button>
          </div>
        </div>

        <DashboardPanel v-show="activeTab === 'dashboard'" @go-to-new-jobs="goToNewJobs" />
        <JobManagementPanel v-show="activeTab === 'job-management'" :new-only-filter="newOnlyFilter" @clear-new-filter="clearNewFilter" />
        <SkillManagementPanel v-show="activeTab === 'skill-management'" />
        <div v-show="activeTab === 'graph-management'" class="graph-wrapper">
          <GraphPanel />
        </div>
        <UserManagementPanel v-show="activeTab === 'user-management'" />
        <UpdateConfigPanel v-show="activeTab === 'update-config'" />
        <ScheduleConfigPanel v-show="activeTab === 'schedule-config'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppSidebar from '@/components/AppSidebar.vue'
import DashboardPanel from './DashboardPanel.vue'
import JobManagementPanel from './JobManagementPanel.vue'
import SkillManagementPanel from './SkillManagementPanel.vue'
import UserManagementPanel from './UserManagementPanel.vue'
import UpdateConfigPanel from './UpdateConfigPanel.vue'
import ScheduleConfigPanel from './ScheduleConfigPanel.vue'
import GraphPanel from '@/views/user/GraphPanel.vue'

const router = useRouter()
const userStore = useUserStore()
const currentUser = computed(() => userStore.user)
const activeTab = ref('dashboard')
const newOnlyFilter = ref(false)

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  dashboard: { title: '数据概览', subtitle: '管理系统核心数据与配置' },
  'job-management': { title: '岗位数据管理', subtitle: '管理和维护岗位数据' },
  'skill-management': { title: '技能数据管理', subtitle: '管理和维护技能节点' },
  'user-management': { title: '用户管理', subtitle: '管理系统用户账户' },
  'update-config': { title: '更新时间配置', subtitle: '设置数据更新时间' },
  'schedule-config': { title: '循环任务配置', subtitle: '管理循环执行任务' },
  'graph-management': { title: '能力图谱', subtitle: '全景图谱可视化展示' }
}
const pageTitle = computed(() => pageTitles[activeTab.value]?.title || '')
const pageSubtitle = computed(() => pageTitles[activeTab.value]?.subtitle || '')

function goToNewJobs() {
  newOnlyFilter.value = true
  activeTab.value = 'job-management'
}

function clearNewFilter() {
  newOnlyFilter.value = false
}

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout { min-height: 100vh; background: #f9fafb; }
.main-content { margin-left: 220px; min-height: 100vh; }
.admin-page { padding: 30px; }
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.page-header h1 { font-size: 24px; font-weight: 600; color: #1a1a1a; }
.page-subtitle { font-size: 14px; color: #999; margin-top: 4px; }
.header-right { display: flex; align-items: center; gap: 12px; }
.admin-name { font-size: 14px; color: #666; }
@media (max-width: 768px) { .main-content { margin-left: 56px; } }
.graph-wrapper { width: 100%; height: calc(100vh - 160px); }
</style>

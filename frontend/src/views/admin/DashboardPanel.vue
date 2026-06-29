<template>
  <div class="tab-content">
    <!-- 今日新增岗位 - 醒目跳转条 -->
    <div class="new-jobs-banner" @click="$emit('go-to-new-jobs')">
      <div class="banner-content">
        <div class="banner-icon">📋</div>
        <div class="banner-text">
          <span class="banner-title">今日新增岗位</span>
          <span class="banner-count">{{ stats.today_new_jobs }} 个</span>
        </div>
      </div>
      <el-button type="primary" size="small" round>查看详情 →</el-button>
    </div>

    <div v-loading="dashboardLoading" class="stats-grid">
      <div class="stat-card"><div class="stat-icon blue">JC</div><div class="stat-value">{{ stats.total_jobs }}</div><div class="stat-label">岗位总数</div></div>
      <div class="stat-card"><div class="stat-icon green">SK</div><div class="stat-value">{{ stats.total_skills }}</div><div class="stat-label">技能节点</div></div>
      <div class="stat-card"><div class="stat-icon orange">US</div><div class="stat-value">{{ stats.total_users }}</div><div class="stat-label">用户数量</div></div>
      <div class="stat-card"><div class="stat-icon purple">UP</div><div class="stat-value">{{ stats.pending_updates }}</div><div class="stat-label">待审核更新</div></div>
    </div>

    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header"><span>最近更新记录</span><el-button size="small" @click="loadEvolutions">刷新</el-button></div>
      </template>
      <el-table v-loading="evoLoading" :data="evolutions" stripe style="width: 100%">
        <el-table-column prop="job_name" label="岗位名称" />
        <el-table-column prop="changes_summary" label="变更说明" />
        <el-table-column prop="created_at" label="更新时间" width="180" />
        <el-table-column prop="evolution_type" label="变更类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.evolution_type === 'update' ? 'success' : 'warning'" size="small">{{ row.evolution_type }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card class="content-card" shadow="never">
      <template #header><div class="card-header"><span>系统运行状态</span><el-button size="small" @click="loadTasks">刷新</el-button></div></template>
      <el-table v-loading="taskLoading" :data="tasks" stripe style="width: 100%">
        <el-table-column prop="source_name" label="任务名称" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'failed' ? 'danger' : 'warning'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboardStats, getEvolutions, getTasks } from '@/api/admin'

defineEmits<{
  'go-to-new-jobs': []
}>()

const stats = ref({ total_jobs: 0, total_skills: 0, total_users: 0, pending_updates: 0, today_new_jobs: 0 })
const evolutions = ref<any[]>([])
const tasks = ref<any[]>([])

const dashboardLoading = ref(false)
async function loadStats() {
  dashboardLoading.value = true
  try { stats.value = await getDashboardStats() } catch (e) { console.error(e) }
  finally { dashboardLoading.value = false }
}

const evoLoading = ref(false)
async function loadEvolutions() {
  evoLoading.value = true
  try { evolutions.value = await getEvolutions(0, 20) } catch (e) { console.error(e) }
  finally { evoLoading.value = false }
}

const taskLoading = ref(false)
async function loadTasks() {
  taskLoading.value = true
  try { tasks.value = await getTasks() } catch (e) { console.error(e) }
  finally { taskLoading.value = false }
}

onMounted(() => {
  loadStats()
  loadEvolutions()
  loadTasks()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}
.stat-card {
  background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;
}
.stat-icon {
  width: 40px; height: 40px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; color: #fff; margin-bottom: 12px;
}
.stat-icon.blue { background: #3b82f6; }
.stat-icon.green { background: #16a34a; }
.stat-icon.orange { background: #ea580c; }
.stat-icon.purple { background: #8b5cf6; }
.stat-value { font-size: 24px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.stat-label { font-size: 13px; color: #999; }
.content-card { margin-bottom: 24px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header span { font-size: 16px; font-weight: 600; color: #1a1a1a; }

/* 今日新增岗位 - 醒目跳转条 */
.new-jobs-banner {
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 12px; padding: 18px 24px; margin-bottom: 24px;
  cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
}
.new-jobs-banner:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(59,130,246,0.3);
}
.banner-content { display: flex; align-items: center; gap: 14px; }
.banner-icon { font-size: 28px; line-height: 1; }
.banner-text { display: flex; flex-direction: column; gap: 2px; }
.banner-title { font-size: 16px; font-weight: 600; color: #fff; }
.banner-count { font-size: 28px; font-weight: 700; color: #fff; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
</style>

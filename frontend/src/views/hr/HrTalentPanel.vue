<template>
  <div class="hr-talent-panel">
    <div class="panel-header">
      <div>
        <h1>人才管理</h1>
        <p>查看您发布岗位的求职者投递情况</p>
      </div>
    </div>

    <!-- 岗位卡片列表 -->
    <div class="job-list">
      <div v-if="jobs.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <h3>暂无投递数据</h3>
        <p>请先在「岗位管理」中发布岗位，求职者投递后会自动显示在此处</p>
      </div>

      <div v-for="job in jobs" :key="job.id" class="job-card" @click="$emit('view-applicants', job)">
        <div class="job-card-header">
          <div class="job-title-row">
            <h3 class="job-name">{{ job.name }}</h3>
            <span class="status-tag" :class="job.status">{{ statusLabel(job.status) }}</span>
          </div>
          <div class="job-dept">{{ job.department || '未设置部门' }}</div>
        </div>

        <div class="job-stats">
          <div class="stat-item">
            <span class="stat-num primary">{{ job._applicant_count ?? 0 }}</span>
            <span class="stat-label">总投递</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num warning">{{ job._pending_count ?? 0 }}</span>
            <span class="stat-label">待处理</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num success">{{ job._interview_count ?? 0 }}</span>
            <span class="stat-label">面试中</span>
          </div>
        </div>

        <div class="job-card-footer">
          <span class="view-link">查看求职者 →</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getJobs } from '@/api/jobs'

const userStore = useUserStore()

interface JobItem {
  id: number
  name: string
  code: string
  department?: string
  status: string
  created_at: string
  _applicant_count?: number
  _pending_count?: number
  _interview_count?: number
}

const jobs = ref<JobItem[]>([])

defineEmits<{ 'view-applicants': [job: JobItem] }>()

async function loadJobs() {
  try {
    const res = await getJobs({ limit: 100, uploader_id: userStore.user?.id })
    jobs.value = (res.items || []).map(j => ({
      ...j,
      _applicant_count: 0,
      _pending_count: 0,
      _interview_count: 0,
    }))
  } catch (e) {
    console.error('加载岗位失败', e)
  }
}

function statusLabel(s: string) {
  return { draft: '草稿', active: '发布中', deprecated: '已下架' }[s] || s
}

onMounted(loadJobs)
</script>

<style scoped>
.hr-talent-panel {
  max-width: 1200px;
  animation: fadeUp 0.3s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-header {
  margin-bottom: 28px;
}

.panel-header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.3px;
}

.panel-header p {
  font-size: 14px;
  color: #9ca3af;
  margin-top: 6px;
}

.job-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 900px) {
  .job-list { grid-template-columns: 1fr; }
}

.job-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px 24px;
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-card:hover {
  border-color: #c4b5fd;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.1);
  transform: translateY(-2px);
}

.job-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.job-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.job-name {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.job-dept {
  font-size: 13px;
  color: #9ca3af;
}

.status-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.status-tag.active { background: #dcfce7; color: #16a34a; }
.status-tag.draft { background: #fef3c7; color: #d97706; }
.status-tag.deprecated { background: #f3f4f6; color: #9ca3af; }

.job-stats {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 14px 0;
  border-top: 1px solid #f3f4f6;
  border-bottom: 1px solid #f3f4f6;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-num {
  font-size: 22px;
  font-weight: 700;
}

.stat-num.primary { color: #8b5cf6; }
.stat-num.warning { color: #f59e0b; }
.stat-num.success { color: #22c55e; }

.stat-label {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
}

.stat-divider {
  width: 1px;
  height: 30px;
  background: #e5e7eb;
}

.job-card-footer {
  display: flex;
  justify-content: flex-end;
}

.view-link {
  font-size: 13px;
  font-weight: 500;
  color: #8b5cf6;
  transition: all 0.2s;
}

.job-card:hover .view-link { color: #7c3aed; }

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  background: #fff;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
}

.empty-icon { font-size: 48px; margin-bottom: 12px; }

.empty-state h3 {
  font-size: 18px;
  color: #374151;
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}
</style>

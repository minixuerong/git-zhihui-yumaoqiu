<template>
  <div class="applicant-panel">
    <!-- 顶部返回栏 -->
    <div class="top-bar">
      <button class="back-btn" @click="$emit('back')">
        <span class="back-arrow">←</span>
        <span>返回人才管理</span>
      </button>
    </div>

    <!-- 岗位信息头 -->
    <div class="job-hero">
      <div class="hero-left">
        <div class="hero-tags">
          <span class="hero-tag status" :class="job.status">{{ statusLabel(job.status) }}</span>
          <span class="hero-tag dept">{{ job.department || '未设置部门' }}</span>
        </div>
        <h1 class="hero-title">{{ job.name }}</h1>
        <p class="hero-code">编码：{{ job.code }}</p>
      </div>
      <div class="hero-right">
        <div class="hero-stat">
          <span class="hero-stat-num">{{ applicants.length }}</span>
          <span class="hero-stat-label">总投递</span>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card total">
        <span class="stat-icon">📋</span>
        <div class="stat-body">
          <span class="stat-val">{{ applicants.length }}</span>
          <span class="stat-lbl">全部求职者</span>
        </div>
      </div>
      <div class="stat-card pending">
        <span class="stat-icon">⏳</span>
        <div class="stat-body">
          <span class="stat-val">{{ pendingCount }}</span>
          <span class="stat-lbl">待处理</span>
        </div>
      </div>
      <div class="stat-card interviewed">
        <span class="stat-icon">✅</span>
        <div class="stat-body">
          <span class="stat-val">{{ reviewedCount }}</span>
          <span class="stat-lbl">已评估</span>
        </div>
      </div>
      <div class="stat-card matched">
        <span class="stat-icon">🎯</span>
        <div class="stat-body">
          <span class="stat-val">{{ highMatchCount }}</span>
          <span class="stat-lbl">高匹配(≥80%)</span>
        </div>
      </div>
    </div>

    <!-- 搜索/筛选栏 -->
    <div class="filter-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" v-model="searchQuery" placeholder="搜索求职者姓名..." class="search-input">
      </div>
      <select v-model="matchFilter" class="filter-select">
        <option value="">全部匹配度</option>
        <option value="high">高匹配 (≥80%)</option>
        <option value="medium">中匹配 (60%-80%)</option>
        <option value="low">低匹配 (<60%)</option>
      </select>
    </div>

    <!-- 求职者列表 -->
    <div class="applicant-section">
      <div v-if="filteredApplicants.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <h3>暂无求职者</h3>
        <p>该岗位尚未收到求职者投递</p>
      </div>

      <div class="applicant-grid">
        <div
          v-for="a in filteredApplicants"
          :key="a.id"
          class="applicant-card"
          :class="{ expanded: selectedId === a.id }"
          @click="toggleDetail(a)"
        >
          <!-- 卡片头部 -->
          <div class="card-header">
            <div class="card-avatar" :style="{ background: avatarGradient(a.candidate_name) }">
              {{ (a.candidate_name || '?')[0] }}
            </div>
            <div class="card-info">
              <div class="card-name">{{ a.candidate_name || '未知求职者' }}</div>
              <div class="card-meta">
                <span>📄 {{ a.resume_filename || '未命名简历' }}</span>
                <span>📅 {{ formatDate(a.created_at) }}</span>
              </div>
            </div>
            <div class="card-score" :class="scoreLevel(a.match_score)">
              <span class="score-val">{{ a.match_score != null ? (a.match_score * 100).toFixed(0) + '%' : '—' }}</span>
              <span class="score-lbl">匹配度</span>
            </div>
          </div>

          <!-- 展开详情 -->
          <div v-if="selectedId === a.id" class="card-detail">
            <div class="detail-divider"></div>
            <div class="detail-content">
              <div class="detail-row">
                <div class="detail-block">
                  <h4 class="detail-block-title">📊 差距分析</h4>
                  <div class="detail-block-body" v-if="a.gap_analysis">
                    <pre>{{ formatJson(a.gap_analysis) }}</pre>
                  </div>
                  <p v-else class="detail-empty">暂无分析数据</p>
                </div>
                <div class="detail-block">
                  <h4 class="detail-block-title">💡 改进建议</h4>
                  <div class="detail-block-body" v-if="a.improvement_suggestions">
                    <pre>{{ formatJson(a.improvement_suggestions) }}</pre>
                  </div>
                  <p v-else class="detail-empty">暂无建议</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/api/index'

interface JobItem {
  id: number
  name: string
  code: string
  department?: string
  status: string
  created_at: string
}

interface ApplicantItem {
  id: number
  resume_id: number
  job_id: number
  candidate_name?: string
  resume_filename?: string
  match_score?: number
  gap_analysis?: string
  improvement_suggestions?: string
  learning_path?: string
  created_at: string
}

const props = defineProps<{ job: JobItem }>()
defineEmits<{ back: [] }>()

const applicants = ref<ApplicantItem[]>([])
const selectedId = ref<number | null>(null)
const searchQuery = ref('')
const matchFilter = ref('')

const pendingCount = computed(() => applicants.value.filter(a => a.match_score == null).length)
const reviewedCount = computed(() => applicants.value.filter(a => a.match_score != null).length)
const highMatchCount = computed(() => applicants.value.filter(a => a.match_score != null && a.match_score >= 0.8).length)

const filteredApplicants = computed(() => {
  return applicants.value.filter(a => {
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      if (!(a.candidate_name || '').toLowerCase().includes(q)) return false
    }
    if (matchFilter.value === 'high' && (a.match_score == null || a.match_score < 0.8)) return false
    if (matchFilter.value === 'medium' && (a.match_score == null || a.match_score < 0.6 || a.match_score >= 0.8)) return false
    if (matchFilter.value === 'low' && (a.match_score != null && a.match_score >= 0.6)) return false
    return true
  })
})

function toggleDetail(a: ApplicantItem) {
  selectedId.value = selectedId.value === a.id ? null : a.id
}

const gradients = [
  'linear-gradient(135deg, #8b5cf6, #6366f1)',
  'linear-gradient(135deg, #f59e0b, #f97316)',
  'linear-gradient(135deg, #10b981, #059669)',
  'linear-gradient(135deg, #ef4444, #dc2626)',
  'linear-gradient(135deg, #3b82f6, #2563eb)',
  'linear-gradient(135deg, #ec4899, #db2777)',
  'linear-gradient(135deg, #14b8a6, #0d9488)',
  'linear-gradient(135deg, #a855f7, #9333ea)',
]

function avatarGradient(name?: string) {
  if (!name) return gradients[0]
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = (hash * 7 + name.charCodeAt(i)) % gradients.length
  return gradients[hash]
}

function scoreLevel(score?: number) {
  if (score == null) return 'none'
  if (score >= 0.8) return 'high'
  if (score >= 0.6) return 'medium'
  return 'low'
}

function statusLabel(s: string) {
  return { draft: '草稿', active: '发布中', deprecated: '已下架' }[s] || s
}

function formatDate(d: string) {
  return d ? d.slice(0, 10) : ''
}

function formatJson(val: string) {
  if (!val) return '—'
  try {
    return JSON.stringify(JSON.parse(val), null, 2)
  } catch {
    return val
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/match/records', { params: { job_id: props.job.id, limit: 200 } })
    const records = Array.isArray(res) ? res : []
    applicants.value = records.map((r: any) => ({
      id: r.id,
      resume_id: r.resume_id,
      job_id: r.job_id,
      candidate_name: r.candidate_name || `求职者 #${r.resume_id}`,
      resume_filename: r.resume_filename || '',
      match_score: r.match_score,
      gap_analysis: r.gap_analysis,
      improvement_suggestions: r.improvement_suggestions,
      learning_path: r.learning_path,
      created_at: r.created_at,
    }))
  } catch {
    applicants.value = []
  }
})
</script>

<style scoped>
/* ===== Layout ===== */
.applicant-panel {
  max-width: 1200px;
  animation: fadeUp 0.35s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Top Bar ===== */
.top-bar { margin-bottom: 24px; }

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #6b7280;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: #fafaff;
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08);
}

.back-arrow { font-size: 16px; }

/* ===== Job Hero ===== */
.job-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border: 1px solid #c4b5fd;
  border-radius: 14px;
  padding: 28px 32px;
  margin-bottom: 24px;
}

.hero-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.hero-tag {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.hero-tag.status.active { background: #dcfce7; color: #16a34a; }
.hero-tag.status.draft { background: #fef3c7; color: #d97706; }
.hero-tag.status.deprecated { background: #e5e7eb; color: #9ca3af; }
.hero-tag.dept { background: rgba(139, 92, 246, 0.12); color: #7c3aed; }

.hero-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 6px;
  letter-spacing: -0.3px;
}

.hero-code {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.hero-right {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-left: 32px;
  border-left: 1px solid rgba(139, 92, 246, 0.2);
}

.hero-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.hero-stat-num {
  font-size: 36px;
  font-weight: 800;
  color: #7c3aed;
  line-height: 1;
}

.hero-stat-label {
  font-size: 13px;
  color: #8b5cf6;
  font-weight: 500;
}

/* ===== Stats ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 28px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 18px 20px;
  transition: all 0.25s ease;
}

.stat-card:hover {
  border-color: #c4b5fd;
  box-shadow: 0 2px 12px rgba(139, 92, 246, 0.06);
}

.stat-icon { font-size: 24px; }

.stat-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-val {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.stat-lbl {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

.stat-card.total .stat-val { color: #8b5cf6; }
.stat-card.pending .stat-val { color: #f59e0b; }
.stat-card.interviewed .stat-val { color: #22c55e; }
.stat-card.matched .stat-val { color: #ef4444; }

/* ===== Filter Bar ===== */
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-box {
  flex: 1;
  max-width: 360px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.search-icon { font-size: 14px; }

.search-input {
  flex: 1;
  height: 42px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1f2937;
  background: transparent;
}

.search-input::placeholder { color: #9ca3af; }

.filter-select {
  padding: 0 14px;
  height: 42px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  background: #fff;
  min-width: 150px;
  cursor: pointer;
  transition: border-color 0.2s;
  color: #374151;
}

.filter-select:focus { border-color: #8b5cf6; }

/* ===== Applicant Grid ===== */
.applicant-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.applicant-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease;
}

.applicant-card:hover {
  border-color: #c4b5fd;
  box-shadow: 0 2px 16px rgba(139, 92, 246, 0.08);
}

.applicant-card.expanded {
  border-color: #8b5cf6;
  box-shadow: 0 4px 24px rgba(139, 92, 246, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 22px;
}

.card-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-info { flex: 1; min-width: 0; }

.card-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.card-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #9ca3af;
  flex-wrap: wrap;
}

.card-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
  padding: 8px 16px;
  border-radius: 10px;
  flex-shrink: 0;
  min-width: 72px;
}

.card-score.high { background: #dcfce7; }
.card-score.medium { background: #fef3c7; }
.card-score.low { background: #fef2f2; }
.card-score.none { background: #f3f4f6; }

.score-val {
  font-size: 18px;
  font-weight: 700;
}

.card-score.high .score-val { color: #16a34a; }
.card-score.medium .score-val { color: #d97706; }
.card-score.low .score-val { color: #dc2626; }
.card-score.none .score-val { color: #9ca3af; }

.score-lbl {
  font-size: 11px;
  font-weight: 500;
  color: #6b7280;
}

/* ===== Detail ===== */
.card-detail {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from { opacity: 0; max-height: 0; }
  to { opacity: 1; max-height: 600px; }
}

.detail-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0 22px;
}

.detail-content {
  padding: 20px 22px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 768px) {
  .detail-row { grid-template-columns: 1fr; }
}

.detail-block {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-block-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.detail-block-body {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 14px 16px;
  max-height: 200px;
  overflow-y: auto;
}

.detail-block-body::-webkit-scrollbar { width: 4px; }
.detail-block-body::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 2px; }

.detail-block-body pre {
  margin: 0;
  font-size: 13px;
  color: #374151;
  white-space: pre-wrap;
  line-height: 1.6;
  font-family: 'Menlo', 'Consolas', monospace;
}

.detail-empty {
  color: #9ca3af;
  font-size: 14px;
  margin: 0;
  padding: 20px 0;
  text-align: center;
}

/* ===== Empty ===== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: #fff;
  border: 2px dashed #e5e7eb;
  border-radius: 14px;
}

.empty-icon { font-size: 56px; margin-bottom: 16px; }

.empty-state h3 {
  font-size: 20px;
  color: #374151;
  margin: 0 0 8px;
}

.empty-state p {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}
</style>

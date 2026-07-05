<template>
  <div class="update-panel">
    <!-- 顶部 -->
    <div class="header">
      <div>
        <h1>能力更新</h1>
        <p>持续跟踪技能变化，实时更新个人能力画像</p>
      </div>
      <div class="header-right">
        <div class="job-selector">
          <label>选择岗位：</label>
          <select v-model="selectedJob" @change="onJobChange">
            <option value="">-- 请选择岗位 --</option>
            <option
              v-for="job in jobList"
              :key="job.id"
              :value="job.name"
            >{{ job.name }}</option>
          </select>
        </div>
        <div class="user-info-bar">
          <span class="user-name">{{ username }}</span>
          <div class="user-avatar">{{ userInitial }}</div>
          <button class="logout-btn" @click="handleLogout">退出登录</button>
        </div>
      </div>
    </div>

    <!-- 未选择岗位 -->
    <div v-if="!selectedJob" class="empty-state">
      <div class="empty-icon">🔍</div>
      <div class="empty-text">请选择岗位查看其更新要求</div>
    </div>

    <!-- 已选择岗位 -->
    <template v-if="selectedJob">
      <!-- 现有技能概览 -->
      <div class="current-skills">
        <div class="cs-header">
          <span class="cs-title">当前岗位已有技能</span>
          <span class="cs-count">{{ currentSkills.length }} 项</span>
        </div>
        <div class="cs-tags">
          <span v-for="skill in currentSkills" :key="skill" class="cs-tag">{{ skill }}</span>
        </div>
        <div class="cs-hint" v-if="!currentSkills.length">
          该岗位在图谱中暂无关联技能数据
        </div>
      </div>

      <!-- 更新统计 -->
      <div class="stats-row">
        <div class="stat-card highlight">
          <div class="stat-value">{{ highWeightItems.length }}</div>
          <div class="stat-label">高权重更新</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ matchedUpdates.length }}</div>
          <div class="stat-label">更新总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ maxWeight }}</div>
          <div class="stat-label">最高权重</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ newSkillCount }}</div>
          <div class="stat-label">新增技能组合</div>
        </div>
      </div>

      <!-- 高权重更新 -->
      <div class="section" v-if="highWeightItems.length">
        <div class="section-header urgent">
          <span class="section-icon">⚡</span>
          <span class="section-title">高权重更新要求</span>
          <span class="section-badge">需优先关注</span>
        </div>
        <div class="update-list">
          <div
            v-for="(item, index) in highWeightItems"
            :key="'high-' + index"
            class="update-card high"
          >
            <div class="card-row">
              <div class="card-badges">
                <span
                  v-for="skill in item.skill_pair"
                  :key="skill"
                  class="skill-tag"
                  :class="{ existing: currentSkills.includes(skill), new: !currentSkills.includes(skill) }"
                >{{ skill }}</span>
              </div>
              <div class="weight-badge high">权重 {{ (item.emergence_score * 100).toFixed(0) }}</div>
            </div>
            <div class="weight-bar-wrap">
              <div class="weight-bar-bg">
                <div class="weight-bar-fill high" :style="{ width: (item.emergence_score * 100) + '%' }"></div>
              </div>
            </div>
            <div class="card-meta">
              <span class="growth">增长率 ×{{ item.growth_rate }}</span>
              <span class="status-confirmed" v-if="item.is_industry_confirmed">✓ 行业确认</span>
              <span class="status-pending" v-else>待确认</span>
              <span class="new-skill-badge" v-if="hasNewSkill(item)">含新增技能</span>
            </div>
            <div class="card-reason">{{ item.reason }}</div>
          </div>
        </div>
      </div>

      <!-- 低权重更新 -->
      <div class="section" v-if="lowWeightItems.length">
        <div class="section-header normal">
          <span class="section-icon">📋</span>
          <span class="section-title">低权重更新要求</span>
          <span class="section-badge subtle">参考关注</span>
        </div>
        <div class="update-list">
          <div
            v-for="(item, index) in lowWeightItems"
            :key="'low-' + index"
            class="update-card low"
          >
            <div class="card-row">
              <div class="card-badges">
                <span
                  v-for="skill in item.skill_pair"
                  :key="skill"
                  class="skill-tag subtle"
                  :class="{ existing: currentSkills.includes(skill), new: !currentSkills.includes(skill) }"
                >{{ skill }}</span>
              </div>
              <div class="weight-badge low">权重 {{ (item.emergence_score * 100).toFixed(0) }}</div>
            </div>
            <div class="weight-bar-wrap">
              <div class="weight-bar-bg">
                <div class="weight-bar-fill low" :style="{ width: (item.emergence_score * 100) + '%' }"></div>
              </div>
            </div>
            <div class="card-meta">
              <span class="growth">增长率 ×{{ item.growth_rate }}</span>
              <span class="new-skill-badge" v-if="hasNewSkill(item)">含新增技能</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 无更新 -->
      <div v-if="!matchedUpdates.length" class="no-updates">
        <div class="no-updates-icon">✅</div>
        <div class="no-updates-text">该岗位暂无技能更新要求</div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import graphData from '@/assets/graph_data.json'
import emergingData from '@/assets/emerging_jobs.json'

interface GraphNode {
  id: string
  name: string
  category: number
  categoryName?: string
}

interface GraphLink {
  source: string
  target: string
  value: number
}

interface Candidate {
  skill_pair: string[]
  growth_rate: number
  count: number
  external_authority_score: number
  emergence_score: number
  is_industry_confirmed: boolean
  status: string
  sample_job_titles: string[]
  reason: string
}

interface EmergingData {
  total_candidates: number
  industry_confirmed: number
  candidates: Candidate[]
}

const jobs = graphData.nodes.filter((n: GraphNode) => n.category >= 0 && n.category <= 7)
const links = graphData.links as GraphLink[]
const emerging = emergingData as EmergingData

const WEIGHT_THRESHOLD = 0.8
const SKILL_CATEGORY = 8

const router = useRouter()
const userStore = useUserStore()

const selectedJob = ref('')

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())

const jobList = computed(() => {
  return jobs.sort((a: GraphNode, b: GraphNode) => a.name.localeCompare(b.name, 'zh'))
})

/** 岗位当前已有的技能（从图谱关联中提取） */
const currentSkills = computed(() => {
  if (!selectedJob.value) return []
  return links
    .filter((l: GraphLink) => l.source === selectedJob.value)
    .map((l: GraphLink) => l.target)
    .filter((skill: string) => {
      const node = graphData.nodes.find((n: GraphNode) => n.id === skill)
      return node && node.category === SKILL_CATEGORY
    })
})

/** 匹配的更新：选择与岗位现有技能有关联的新兴技能组合 */
const matchedUpdates = computed(() => {
  if (!selectedJob.value || !currentSkills.value.length) return []

  const jobSkills = currentSkills.value

  return emerging.candidates
    .filter(c => c.skill_pair.some(s => jobSkills.includes(s)))
    .sort((a, b) => b.emergence_score - a.emergence_score)
})

const highWeightItems = computed(() => {
  return matchedUpdates.value.filter(c => c.emergence_score >= WEIGHT_THRESHOLD)
})

const lowWeightItems = computed(() => {
  return matchedUpdates.value.filter(c => c.emergence_score < WEIGHT_THRESHOLD)
})

const maxWeight = computed(() => {
  if (!matchedUpdates.value.length) return '0'
  return (Math.max(...matchedUpdates.value.map(c => c.emergence_score)) * 100).toFixed(0)
})

const newSkillCount = computed(() => {
  if (!matchedUpdates.value.length) return 0
  const allSkills = new Set<string>()
  matchedUpdates.value.forEach(c => c.skill_pair.forEach(s => allSkills.add(s)))
  const existing = new Set(currentSkills.value)
  let newCount = 0
  allSkills.forEach(s => { if (!existing.has(s)) newCount++ })
  return newCount
})

function hasNewSkill(item: Candidate) {
  return item.skill_pair.some(s => !currentSkills.value.includes(s))
}

function onJobChange() {
  // noop
}

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.update-panel {
  padding: 0;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
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

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.job-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.job-selector label {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
}

.job-selector select {
  padding: 8px 12px;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  font-size: 14px;
  color: #1a1a1a;
  background: #fff;
  min-width: 170px;
  cursor: pointer;
  outline: none;
}

.job-selector select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.1);
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

/* Empty */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  border: 1px dashed #d0d5dd;
  border-radius: 8px;
  background: #fafafa;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 15px;
  color: #999;
}

/* 当前技能 */
.current-skills {
  background: #f8faff;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 20px;
}

.cs-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.cs-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
}

.cs-count {
  font-size: 12px;
  color: #3b82f6;
  background: #dbeafe;
  padding: 1px 8px;
  border-radius: 8px;
}

.cs-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.cs-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  background: #dbeafe;
  color: #1e40af;
  font-size: 13px;
  font-weight: 500;
}

.cs-hint {
  font-size: 13px;
  color: #93c5fd;
}

/* Stats */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 18px;
  text-align: center;
}

.stat-card.highlight {
  border-color: #fca5a5;
  background: #fff5f5;
}

.stat-value {
  font-size: 30px;
  font-weight: 700;
  color: #3b82f6;
  line-height: 1.2;
}

.stat-card.highlight .stat-value {
  color: #ef4444;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

/* Section */
.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8e8e8;
}

.section-header.urgent {
  border-bottom-color: #fca5a5;
}

.section-header.normal {
  border-bottom-color: #d0d5dd;
}

.section-icon {
  font-size: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.section-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
  background: #fef3c7;
  color: #d97706;
}

.section-badge.subtle {
  background: #f0f0f0;
  color: #888;
}

/* Update List */
.update-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.update-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 14px 18px;
}

.update-card.high {
  border-left: 4px solid #ef4444;
}

.update-card.low {
  border-left: 4px solid #d0d5dd;
}

.card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.skill-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  background: #eff6ff;
  color: #3b82f6;
}

.skill-tag.existing {
  background: #dbeafe;
  color: #1e40af;
}

.skill-tag.new {
  background: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.skill-tag.subtle.existing {
  background: #f0f0f0;
  color: #888;
}

.skill-tag.subtle.new {
  background: #fef9e7;
  color: #b8860b;
  border: 1px solid #fde68a;
}

.weight-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 12px;
  white-space: nowrap;
}

.weight-badge.high {
  background: #fef2f2;
  color: #dc2626;
}

.weight-badge.low {
  background: #f5f5f5;
  color: #999;
}

/* Weight Bar */
.weight-bar-wrap {
  margin-bottom: 8px;
}

.weight-bar-bg {
  width: 100%;
  height: 6px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.weight-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.weight-bar-fill.high {
  background: linear-gradient(90deg, #f87171, #ef4444);
}

.weight-bar-fill.low {
  background: linear-gradient(90deg, #d0d5dd, #aaa);
}

/* Meta */
.card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}

.growth {
  font-size: 12px;
  color: #d97706;
  background: #fef3c7;
  padding: 2px 8px;
  border-radius: 4px;
}

.status-confirmed {
  font-size: 12px;
  color: #16a34a;
  background: #dcfce7;
  padding: 2px 8px;
  border-radius: 4px;
}

.status-pending {
  font-size: 12px;
  color: #999;
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
}

.new-skill-badge {
  font-size: 11px;
  color: #d97706;
  background: #fef9e7;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #fde68a;
}

.card-reason {
  font-size: 13px;
  color: #888;
  line-height: 1.5;
}

/* No updates */
.no-updates {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  border: 1px dashed #d0d5dd;
  border-radius: 8px;
  background: #fafafa;
}

.no-updates-icon {
  font-size: 36px;
  margin-bottom: 8px;
}

.no-updates-text {
  font-size: 15px;
  color: #999;
}
</style>

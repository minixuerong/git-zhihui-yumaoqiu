<template>
  <div class="match-panel">
    <div class="header">
      <div>
        <h1>匹配分析</h1>
        <p>选择目标岗位与简历，进行智能匹配分析</p>
      </div>
      <div class="user-info-bar">
        <span class="user-name">{{ username }}</span>
        <div class="user-avatar">{{ userInitial }}</div>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </div>
    </div>

    <div class="match-layout">
      <!-- 左侧：岗位列表 -->
      <div class="panel job-panel">
        <div class="panel-header">
          <h2>岗位列表</h2>
          <div class="search-box">
            <el-input
              v-model="jobKeyword"
              placeholder="按岗位编号搜索"
              clearable
              size="small"
              @input="onJobSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
        <div class="panel-body">
          <div
            v-for="job in jobs"
            :key="job.id"
            class="job-card"
            :class="{ selected: selectedJob?.id === job.id }"
            @click="selectedJob = job"
          >
            <div class="job-name">{{ job.name }}</div>
            <div class="job-code">{{ job.code }}</div>
            <div class="job-dept" v-if="job.department">{{ job.department }}</div>
          </div>
          <div v-if="!jobs.length" class="empty">暂无岗位数据</div>
        </div>
        <div class="panel-footer" v-if="totalJobs > pageSize">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="totalJobs"
            layout="prev, pager, next"
            small
            @current-change="loadJobs"
          />
        </div>
      </div>

      <!-- 中间：分析按钮 -->
      <div class="center-col">
        <el-button
          type="primary"
          :disabled="!selectedJob || !selectedResume"
          :loading="analyzing"
          @click="doMatch"
          size="large"
        >
          {{ analyzing ? '分析中...' : '开始匹配分析' }}
        </el-button>
      </div>

      <!-- 右侧：简历列表 -->
      <div class="panel resume-panel">
        <div class="panel-header">
          <h2>我的简历</h2>
        </div>
        <div class="panel-body">
          <div
            v-for="item in resumes"
            :key="item.id"
            class="resume-card"
            :class="{ selected: selectedResume?.id === item.id }"
            @click="selectedResume = item"
          >
            <div class="resume-name">{{ item.filename }}</div>
            <div class="resume-status" :class="item.status">
              {{ item.status === 'parsed' ? '已解析' : '未解析' }}
            </div>
            <div class="resume-time">{{ formatTime(item.created_at) }}</div>
          </div>
          <div v-if="!resumes.length" class="empty">暂无简历，请先上传</div>
        </div>
      </div>
    </div>

    <!-- 结果区域 -->
    <div v-if="matchResult" class="result-section">
      <div class="result-header">
        <h2>匹配结果</h2>
        <el-button text @click="matchResult = null">关闭</el-button>
      </div>
      <div class="result-content">
        <div class="score-area">
          <div class="score-ring">
            <svg viewBox="0 0 120 120" width="140" height="140">
              <circle cx="60" cy="60" r="50" fill="none" stroke="#eee" stroke-width="10" />
              <circle
                cx="60" cy="60" r="50"
                fill="none"
                :stroke="scoreColor"
                stroke-width="10"
                stroke-linecap="round"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="scoreOffset"
                transform="rotate(-90, 60, 60)"
                style="transition: stroke-dashoffset 0.8s ease"
              />
              <text x="60" y="55" text-anchor="middle" font-size="28" font-weight="700" :fill="scoreColor">
                {{ Math.round(matchResult.match_score * 100) }}
              </text>
              <text x="60" y="78" text-anchor="middle" font-size="14" fill="#999">分</text>
            </svg>
          </div>
        </div>

        <div class="detail-area">
          <template v-if="matchResult.gap_analysis.length">
            <div class="detail-section">
              <h3>技能详情</h3>
              <div class="skill-grid">
                <div
                  v-for="item in matchResult.gap_analysis"
                  :key="item.skill_id"
                  class="skill-item"
                  :class="item.gap === 'missing' ? 'missing' : item.current_level && item.gap !== 'missing' ? 'weak' : ''"
                >
                  <div class="skill-name">{{ item.skill_name }}</div>
                  <div class="skill-levels">
                    <span v-if="item.current_level" class="level current">{{ item.current_level }}</span>
                    <span v-else class="level none">无</span>
                    <span class="arrow">→</span>
                    <span class="level required">{{ item.required_level }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <div class="detail-section">
            <h3>改进建议</h3>
            <ul class="suggestion-list">
              <li v-for="(s, i) in matchResult.improvement_suggestions" :key="i">{{ s }}</li>
              <li v-if="!matchResult.improvement_suggestions.length" class="no-data">暂无改进建议</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getJobs } from '@/api/jobs'
import { getResumes, matchAnalysis } from '@/api/resumes'
import { Search } from '@element-plus/icons-vue'
import type { Job } from '@/api/jobs'
import type { ResumeItem } from '@/api/resumes'

const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())
function handleLogout() {
  userStore.logout()
  router.push('/login')
}

// 岗位列表
const jobs = ref<Job[]>([])
const totalJobs = ref(0)
const currentPage = ref(1)
const pageSize = 48
const jobKeyword = ref('')
const loadingJobs = ref(false)

async function loadJobs() {
  loadingJobs.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize
    const res = await getJobs({ skip, limit: pageSize, data_type: 'cleaned', keyword: jobKeyword.value || undefined })
    jobs.value = res.items
    totalJobs.value = res.total
  } catch {
    // ignore
  } finally {
    loadingJobs.value = false
  }
}

let searchTimer: ReturnType<typeof setTimeout>
function onJobSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadJobs()
  }, 300)
}

// 简历列表
const resumes = ref<ResumeItem[]>([])
async function loadResumes() {
  try {
    const res = await getResumes()
    resumes.value = res
  } catch {
    // ignore
  }
}

// 选中状态
const selectedJob = ref<Job | null>(null)
const selectedResume = ref<ResumeItem | null>(null)
const analyzing = ref(false)
const matchResult = ref<{
  match_score: number
  gap_analysis: Array<{ skill_id: number; skill_name: string; current_level: string | null; required_level: string; gap: string | number }>
  improvement_suggestions: string[]
  learning_path: string[]
} | null>(null)

// SVG 圆环
const circumference = Math.PI * 2 * 50
const scoreOffset = computed(() => {
  const score = matchResult.value?.match_score ?? 0
  const voff = (1 - score) * circumference
  return isNaN(voff) ? circumference : voff
})
const scoreColor = computed(() => {
  if (!matchResult.value) return '#999'
  const s = matchResult.value.match_score
  if (s >= 0.7) return '#22c55e'
  if (s >= 0.4) return '#eab308'
  return '#ef4444'
})

function formatTime(t: string) {
  if (!t) return ''
  return t.slice(0, 10)
}

async function doMatch() {
  if (!selectedJob.value || !selectedResume.value) return
  analyzing.value = true
  matchResult.value = null
  try {
    const res = await matchAnalysis(selectedResume.value.id, selectedJob.value.id)
    matchResult.value = res
  } catch (e: any) {
    matchResult.value = {
      match_score: 0,
      gap_analysis: [],
      improvement_suggestions: [e?.response?.data?.detail || '分析失败，请稍后重试'],
      learning_path: []
    }
  } finally {
    analyzing.value = false
  }
}

onMounted(() => {
  loadJobs()
  loadResumes()
})
</script>

<style scoped>
.match-panel {
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.header p {
  font-size: 14px;
  color: #999;
  margin: 4px 0 0;
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

/* 左右布局 */
.match-layout {
  display: flex;
  gap: 16px;
  align-items: stretch;
}

.panel {
  flex: 1;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  min-height: 400px;
  max-height: 560px;
}

.panel-header {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.panel-header h2 {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.search-box {
  width: 200px;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.panel-footer {
  padding: 8px 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

/* 中间列 */
.center-col {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 0 8px;
}

/* 岗位卡片 */
.job-card {
  padding: 10px 12px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.15s;
}

.job-card:hover {
  border-color: #3b82f6;
  background: #f8faff;
}

.job-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.job-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.job-code {
  font-size: 12px;
  color: #999;
}

.job-dept {
  font-size: 12px;
  color: #3b82f6;
  margin-top: 2px;
}

/* 简历卡片 */
.resume-card {
  padding: 10px 12px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.15s;
}

.resume-card:hover {
  border-color: #3b82f6;
  background: #f8faff;
}

.resume-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.resume-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.resume-status {
  font-size: 12px;
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
}

.resume-status.parsed {
  color: #16a34a;
  background: #f0fdf4;
}

.resume-status.pending, .resume-status.uploaded {
  color: #eab308;
  background: #fefce8;
}

.resume-time {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.empty {
  text-align: center;
  color: #bbb;
  padding: 40px 0;
  font-size: 14px;
}

/* 结果区域 */
.result-section {
  margin-top: 24px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.result-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.result-content {
  display: flex;
  gap: 32px;
  padding: 24px 20px;
}

.score-area {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
}

.detail-area {
  flex: 1;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 10px;
}

.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
}

.skill-item {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fafafa;
}

.skill-item.missing {
  border-color: #fecaca;
  background: #fef2f2;
}

.skill-name {
  font-size: 13px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.skill-levels {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.level {
  padding: 1px 6px;
  border-radius: 3px;
}

.level.current {
  color: #3b82f6;
  background: #eff6ff;
}

.level.required {
  color: #16a34a;
  background: #f0fdf4;
}

.level.none {
  color: #ef4444;
  background: #fef2f2;
}

.arrow {
  color: #999;
  font-size: 12px;
}

.suggestion-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestion-list li {
  padding: 6px 0;
  font-size: 13px;
  color: #374151;
  border-bottom: 1px solid #f5f5f5;
}

.suggestion-list li:last-child {
  border-bottom: none;
}

.no-data {
  color: #bbb;
}
</style>

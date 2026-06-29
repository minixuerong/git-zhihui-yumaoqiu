<template>
  <div class="user-layout">
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="logo">CAPABILITY<span>.BRAIN</span></div>
      <nav>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'home' }" @click="activeTab = 'home'">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">我的首页</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'resume' }" @click="activeTab = 'resume'">
          <span class="nav-icon">📄</span>
          <span class="nav-text">上传简历</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'match' }" @click="activeTab = 'match'">
          <span class="nav-icon">📊</span>
          <span class="nav-text">匹配分析</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'learning' }" @click="activeTab = 'learning'">
          <span class="nav-icon">📚</span>
          <span class="nav-text">学习规划</span>
        </a>
        <div class="nav-divider"></div>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'graph' }" @click="activeTab = 'graph'">
          <span class="nav-icon">🔗</span>
          <span class="nav-text">能力图谱</span>
        </a>
        <a href="javascript:void(0)" class="nav-item active" :class="{ active: activeTab === 'discovery' }" @click="activeTab = 'discovery'">
          <span class="nav-icon">🔍</span>
          <span class="nav-text">岗位发现</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'update' }" @click="activeTab = 'update'">
          <span class="nav-icon">🔄</span>
          <span class="nav-text">能力更新</span>
        </a>
        <div class="nav-divider"></div>
        <div class="nav-item disabled">
          <span class="nav-icon">⚙️</span>
          <span class="nav-text">系统设置</span>
        </div>
        <div class="nav-item disabled">
          <span class="nav-icon">❓</span>
          <span class="nav-text">帮助文档</span>
        </div>
      </nav>
      <div class="toggle-btn" @click="sidebarCollapsed = !sidebarCollapsed"></div>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ userInitial }}</div>
          <div class="user-detail">
            <div class="user-name">{{ username }}</div>
            <div class="user-role">普通用户</div>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout"><span>退出登录</span></button>
      </div>
    </div>

    <div class="main">
      <!-- 我的首页 -->
      <div v-show="activeTab === 'home'" class="tab-content">
        <div class="header">
          <h1>我的首页</h1>
          <div class="user-info-bar">
            <div class="search-box">
              <input type="text" placeholder="搜索岗位...">
            </div>
            <span class="user-name">{{ username }}</span>
            <div class="user-avatar">{{ userInitial }}</div>
            <button class="logout-btn" @click="handleLogout">退出</button>
          </div>
        </div>
        <div class="stats">
          <div class="stat-card"><div class="stat-value">85%</div><div class="stat-label">综合匹配度</div></div>
          <div class="stat-card"><div class="stat-value">24</div><div class="stat-label">已掌握技能</div></div>
          <div class="stat-card"><div class="stat-value">12</div><div class="stat-label">待学习技能</div></div>
          <div class="stat-card"><div class="stat-value">5</div><div class="stat-label">推荐岗位</div></div>
        </div>
        <div class="home-grid">
          <div>
            <div class="section">
              <h2>快捷操作</h2>
              <div class="quick-actions">
                <div class="action-btn" @click="activeTab = 'resume'">
                  <div class="icon resume">CV</div>
                  <div class="text">上传简历</div>
                </div>
                <div class="action-btn" @click="activeTab = 'match'">
                  <div class="icon match">MA</div>
                  <div class="text">匹配分析</div>
                </div>
                <div class="action-btn" @click="activeTab = 'learning'">
                  <div class="icon learning">LP</div>
                  <div class="text">学习规划</div>
                </div>
                <div class="action-btn" @click="activeTab = 'graph'">
                  <div class="icon graph">GP</div>
                  <div class="text">能力图谱</div>
                </div>
              </div>
            </div>
            <div class="section">
              <h2>推荐岗位</h2>
              <div class="card">
                <div class="card-header"><h3>智能推荐</h3><a href="javascript:void(0)" @click="activeTab = 'match'">查看全部 →</a></div>
                <div class="card-body">
                  <div class="match-item">
                    <div class="job-title">前端开发工程师</div>
                    <div class="skills">React, Vue, TypeScript</div>
                    <div class="match-score">
                      <div class="score-bar"><div class="score-fill" style="width:85%"></div></div>
                      <span class="score-text">85%</span>
                    </div>
                  </div>
                  <div class="match-item">
                    <div class="job-title">全栈开发工程师</div>
                    <div class="skills">Node.js, React, MongoDB</div>
                    <div class="match-score">
                      <div class="score-bar"><div class="score-fill" style="width:78%"></div></div>
                      <span class="score-text">78%</span>
                    </div>
                  </div>
                  <div class="match-item">
                    <div class="job-title">AI算法工程师</div>
                    <div class="skills">Python, TensorFlow, PyTorch</div>
                    <div class="match-score">
                      <div class="score-bar"><div class="score-fill" style="width:65%"></div></div>
                      <span class="score-text">65%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <div class="section">
              <h2>最近活动</h2>
              <div class="card">
                <div class="card-body">
                  <ul class="recent-list">
                    <li class="recent-item"><span class="title">上传简历解析完成</span><span class="date">今天 14:30</span></li>
                    <li class="recent-item"><span class="title">匹配分析更新</span><span class="date">今天 10:00</span></li>
                    <li class="recent-item"><span class="title">学习规划生成</span><span class="date">昨天 16:45</span></li>
                    <li class="recent-item"><span class="title">技能数据更新</span><span class="date">昨天 09:00</span></li>
                    <li class="recent-item"><span class="title">登录系统</span><span class="date">3天前</span></li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="section">
              <h2>学习进度</h2>
              <div class="card">
                <div class="card-body">
                  <div class="progress-item">
                    <div class="progress-label"><span>React进阶</span><span>60%</span></div>
                    <div class="score-bar"><div class="score-fill" style="width:60%"></div></div>
                  </div>
                  <div class="progress-item">
                    <div class="progress-label"><span>TypeScript</span><span>45%</span></div>
                    <div class="score-bar"><div class="score-fill" style="width:45%"></div></div>
                  </div>
                  <div class="progress-item">
                    <div class="progress-label"><span>Node.js</span><span>30%</span></div>
                    <div class="score-bar"><div class="score-fill" style="width:30%"></div></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 岗位发现（默认页面） -->
      <div v-show="activeTab === 'discovery'" class="tab-content">
        <div class="header">
          <div>
            <h1>新岗位发现</h1>
            <p>基于多源数据发现新兴岗位需求</p>
          </div>
          <div class="user-info-bar">
            <div class="search-box">
              <input type="text" placeholder="搜索岗位...">
            </div>
            <span class="user-name">{{ username }}</span>
            <div class="user-avatar">{{ userInitial }}</div>
            <button class="logout-btn" @click="handleLogout">退出登录</button>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>发现配置</h3>
            <button class="btn btn-primary" @click="loadJobs" :loading="discoveryLoading">刷新</button>
          </div>
          <div class="card-body">
            <div class="discovery-form">
              <div class="form-group">
                <label class="form-label">数据源</label>
                <select class="form-select" v-model="discoveryConfig.dataSource">
                  <option>全部数据源</option>
                  <option>招聘网站</option>
                  <option>行业报告</option>
                  <option>社交媒体</option>
                  <option>企业内部</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">领域</label>
                <select class="form-select" v-model="discoveryConfig.field">
                  <option>全部领域</option>
                  <option>人工智能</option>
                  <option>大数据</option>
                  <option>云计算</option>
                  <option>物联网</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">时间范围</label>
                <select class="form-select" v-model="discoveryConfig.timeRange">
                  <option>最近7天</option>
                  <option>最近30天</option>
                  <option>最近90天</option>
                  <option>最近半年</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">关键词</label>
                <input type="text" class="form-input" v-model="discoveryConfig.keywords" placeholder="输入关键词，多个用逗号分隔">
              </div>
              <div class="form-group">
                <label class="form-label">置信度阈值</label>
                <input type="range" class="form-input range" min="0" max="100" v-model.number="discoveryConfig.confidence">
              </div>
              <div class="form-group">
                <label class="form-label">结果数量</label>
                <input type="number" class="form-input" v-model.number="discoveryConfig.resultCount" value="10">
              </div>
            </div>
          </div>
        </div>

        <div class="result-stats">
          <div class="stat-item"><div class="stat-value">{{ totalJobs }}</div><div class="stat-label">新发现岗位</div></div>
          <div class="stat-item"><div class="stat-value">{{ discoveryJobs.length }}</div><div class="stat-label">当前展示</div></div>
          <div class="stat-item"><div class="stat-value">{{ discoveryJobs.filter(j => j.is_new).length }}</div><div class="stat-label">今日新增</div></div>
          <div class="stat-item"><div class="stat-value">{{ discoveryJobs.filter(j => j.status === 'active').length }}</div><div class="stat-label">活跃岗位</div></div>
        </div>

        <div :class="{ loading: discoveryLoading }" class="jobs-grid">
          <div v-if="discoveryLoading" class="loading-overlay">加载中...</div>
          <div class="job-card" v-for="job in discoveryJobs" :key="job.id" @click="openDetail(job)">
            <div class="job-header">
              <h3 class="job-title">{{ job.name }}</h3>
              <span class="job-badge" :class="getBadge(job).cls">{{ getBadge(job).text }}</span>
            </div>
            <p class="job-desc">{{ job.core_responsibilities || '暂无描述' }}</p>
            <div class="job-tags">
              <span class="job-tag" v-if="job.department">{{ job.department }}</span>
              <span class="job-tag" v-if="job.data_source">{{ job.data_source }}</span>
            </div>
            <div class="job-footer">
              <span class="job-date">{{ formatDate(job.created_at) }}</span>
              <a href="javascript:void(0)" class="view-detail">查看详情 →</a>
            </div>
          </div>
          <div v-if="!discoveryLoading && discoveryJobs.length === 0" class="empty-state">
            暂无岗位数据
          </div>
        </div>

        <!-- 详情弹窗 -->
        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">上一页</button>
          <button
            v-for="p in totalPages"
            :key="p"
            class="page-btn"
            :class="{ active: p === currentPage }"
            @click="goToPage(p)"
          >{{ p }}</button>
          <button class="page-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">下一页</button>
          <span class="page-info">共 {{ totalJobs }} 条，{{ totalPages }} 页</span>
        </div>

        <!-- 详情弹窗 -->
        <div class="modal-overlay" :class="{ active: showDetail }" @click.self="showDetail = false">
          <div class="modal">
            <div class="modal-header">
              <h3 class="modal-title">岗位详情</h3>
              <button class="close-btn" @click="showDetail = false">×</button>
            </div>
            <div class="modal-body" v-if="selectedJob">
              <div class="detail-section">
                <span class="section-label">岗位名称</span>
                <h2 class="detail-job-title">{{ selectedJob.name }}</h2>
              </div>
              <div class="detail-section">
                <span class="section-label">岗位编码</span>
                <p class="detail-desc">{{ selectedJob.code }}</p>
              </div>
              <div class="detail-section">
                <span class="section-label">岗位描述</span>
                <p class="detail-desc">{{ selectedJob.core_responsibilities || '暂无描述' }}</p>
              </div>
              <div class="detail-section">
                <span class="section-label">部门</span>
                <p class="detail-desc">{{ selectedJob.department || '未设置' }}</p>
              </div>
              <div class="detail-section">
                <span class="section-label">数据来源</span>
                <p class="detail-desc">{{ selectedJob.data_source || '未知' }}</p>
              </div>
              <div class="detail-section">
                <span class="section-label">状态</span>
                <p class="detail-desc">
                  <span class="job-badge" :class="getBadge(selectedJob).cls" style="font-size:13px;padding:4px 12px">{{ getBadge(selectedJob).text }}</span>
                </p>
              </div>
              <div class="detail-section">
                <span class="section-label">创建时间</span>
                <p class="detail-desc">{{ selectedJob.created_at || '未知' }}</p>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showDetail = false">关闭</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Tab: 上传简历 ===== -->
      <div v-show="activeTab === 'resume'" class="tab-content">
        <ResumePanel />
      </div>

      <!-- ===== Tab: 匹配分析 ===== -->
      <div v-show="activeTab === 'match'" class="tab-content">
        <MatchPanel />
      </div>

      <!-- ===== Tab: 学习规划 ===== -->
      <div v-show="activeTab === 'learning'" class="tab-content">
        <LearningPanel />
      </div>

      <!-- ===== Tab: 能力图谱 ===== -->
      <div v-show="activeTab === 'graph'" class="tab-content">
        <GraphPanel />
      </div>

      <!-- ===== Tab: 能力更新 ===== -->
      <div v-show="activeTab === 'update'" class="tab-content">
        <UpdatePanel />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getJobs } from '@/api/jobs'
import ResumePanel from './ResumePanel.vue'
import MatchPanel from './MatchPanel.vue'
import LearningPanel from './LearningPanel.vue'
import GraphPanel from './GraphPanel.vue'
import UpdatePanel from './UpdatePanel.vue'

const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())

const sidebarCollapsed = ref(false)
const activeTab = ref('discovery') // 默认跳转到岗位发现

const discoveryConfig = reactive({
  dataSource: '全部数据源',
  field: '全部领域',
  timeRange: '最近7天',
  keywords: '',
  confidence: 70,
  resultCount: 10,
})

interface JobItem {
  id: number
  name: string
  code: string
  department: string | null
  core_responsibilities: string | null
  data_source: string | null
  status: string
  is_new: boolean
  created_at: string
}

const discoveryJobs = ref<JobItem[]>([])
const discoveryLoading = ref(false)
const totalJobs = ref(0)
const currentPage = ref(1)
const pageSize = 48
const totalPages = computed(() => Math.ceil(totalJobs.value / pageSize))

async function loadJobs() {
  discoveryLoading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize
    const res = await getJobs({ skip, limit: pageSize, data_type: 'cleaned' })
    discoveryJobs.value = res.items || []
    totalJobs.value = res.total || 0
  } catch (e) {
    console.error('加载岗位失败', e)
  } finally {
    discoveryLoading.value = false
  }
}

function goToPage(page: number) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadJobs()
}

onMounted(() => {
  loadJobs()
})

const showDetail = ref(false)
const selectedJob = ref<JobItem | null>(null)

function openDetail(job: JobItem) {
  selectedJob.value = job
  showDetail.value = true
}

function getBadge(job: JobItem) {
  if (job.is_new) return { text: '新发现', cls: 'new' }
  if (job.status === 'active') return { text: '活跃', cls: 'analysis' }
  return { text: '待审核', cls: 'pending' }
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  return dateStr.slice(0, 10)
}

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  background: #f9fafb;
}

/* ===== Sidebar ===== */
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

.sidebar.collapsed { width: 56px; }

.sidebar .logo {
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

.sidebar .logo span { color: #3b82f6; }

.sidebar.collapsed .logo { font-size: 20px; text-align: center; padding: 8px; margin-bottom: 20px; }
.sidebar.collapsed .logo span { display: none; }
.sidebar.collapsed .nav-icon { margin-right: 0; }
.sidebar.collapsed .nav-text { display: none; }
.sidebar.collapsed .nav-item { justify-content: center; padding: 10px; }
.sidebar.collapsed .nav-section-label { display: none; }
.sidebar.collapsed .nav-divider { margin: 8px 4px; }
.sidebar.collapsed .user-detail { display: none; }
.sidebar.collapsed .user-info { justify-content: center; padding: 8px; }
.sidebar.collapsed .logout-btn span { display: none; }
.sidebar.collapsed .logout-btn { padding: 8px; }

.sidebar nav { flex: 1; overflow-y: auto; overflow-x: hidden; }
.sidebar nav::-webkit-scrollbar { width: 4px; }
.sidebar nav::-webkit-scrollbar-track { background: transparent; }
.sidebar nav::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 2px; }

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

.nav-item:hover { background: #f3f4f6; color: #374151; }
.nav-item:hover::before { height: 20px; }
.nav-item.active { background: #eff6ff; color: #3b82f6; font-weight: 500; }
.nav-item.active::before { height: 20px; }

.nav-icon { margin-right: 10px; font-size: 14px; }

.nav-item.disabled { opacity: 0.5; cursor: not-allowed; }
.nav-item.disabled:hover { background: transparent; color: #6b7280; }

.nav-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 12px 8px;
}

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

/* ===== Sidebar Footer ===== */
.sidebar-footer {
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  margin-top: auto;
}

.sidebar-footer .user-info {
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
}

.user-detail { flex: 1; overflow: hidden; }
.user-name { font-size: 13px; font-weight: 600; color: #1f2937; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: #9ca3af; }

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
  display: flex;
  align-items: center;
  justify-content: center;
}

.logout-btn:hover { background: #fef2f2; border-color: #fecaca; color: #dc2626; }

/* ===== Main Content ===== */
.main {
  margin-left: 220px;
  min-height: 100vh;
  padding: 30px;
  transition: margin-left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar.collapsed ~ .main { margin-left: 56px; }

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 { font-size: 24px; font-weight: 600; color: #1a1a1a; }
.header p { font-size: 14px; color: #999; margin-top: 4px; }

.user-info-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info-bar .user-name { font-size: 14px; color: #1a1a1a; font-weight: 500; }
.user-info-bar .user-avatar { width: 36px; height: 36px; font-size: 14px; }
.user-info-bar .logout-btn {
  width: auto;
  padding: 8px 16px;
  font-size: 13px;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #666;
}

.user-info-bar .logout-btn:hover { background: #fef2f2; border-color: #fecaca; color: #dc2626; }

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 8px 12px;
}

.search-box input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  color: #1a1a1a;
  width: 200px;
}

.search-box input::placeholder { color: #999; }

/* ===== Stats (Home) ===== */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #ffffff;
}

.stat-card .value { font-size: 28px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.stat-card .label { font-size: 13px; color: #999; }

/* ===== Home Grid ===== */
.home-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }

.section { margin-bottom: 30px; }
.section h2 { font-size: 16px; font-weight: 600; color: #1a1a1a; margin-bottom: 15px; }

.card { border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden; background: #ffffff; }
.card-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e0e0e0;
  background: #fafafa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 { font-size: 14px; font-weight: 600; color: #1a1a1a; }
.card-header a { font-size: 13px; color: #3b82f6; text-decoration: none; }
.card-body { padding: 20px; }

.quick-actions { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }

.action-btn {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #ffffff;
}

.action-btn:hover { border-color: #3b82f6; background: #f8fbff; }

.action-btn .icon {
  width: 36px;
  height: 36px;
  margin: 0 auto 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #fff;
}

.action-btn .text { font-size: 13px; color: #1a1a1a; font-weight: 500; }
.action-btn .icon.resume { background: #3b82f6; }
.action-btn .icon.match { background: #16a34a; }
.action-btn .icon.learning { background: #ea580c; }
.action-btn .icon.graph { background: #8b5cf6; }

.recent-list { list-style: none; }
.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.recent-item:last-child { border-bottom: none; }
.recent-item .title { font-size: 14px; color: #1a1a1a; }
.recent-item .date { font-size: 12px; color: #999; }

.match-score { display: flex; align-items: center; gap: 10px; }
.score-bar { flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden; }
.score-fill { height: 100%; background: #3b82f6; border-radius: 4px; }
.score-text { font-size: 14px; font-weight: 600; color: #3b82f6; }

.match-item { padding: 15px 0; border-bottom: 1px solid #f0f0f0; }
.match-item:last-child { border-bottom: none; }
.match-item .job-title { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; }
.match-item .skills { font-size: 12px; color: #999; margin-bottom: 8px; }

.progress-item { margin-bottom: 15px; }
.progress-item:last-child { margin-bottom: 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; }

/* ===== Discovery Form ===== */
.discovery-form {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-label { font-size: 13px; color: #666; font-weight: 500; }

.form-input, .form-select {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #fff;
  color: #1a1a1a;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus, .form-select:focus { border-color: #3b82f6; }
.form-input::placeholder { color: #999; }
.form-input.range { padding: 0; }

.btn {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary { background: #3b82f6; color: #fff; border-color: #3b82f6; }
.btn-primary:hover { background: #2563eb; }
.btn-secondary { background: #fff; color: #666; }
.btn-secondary:hover { background: #fafafa; }

/* ===== Result Stats ===== */
.result-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #ffffff;
}

.stat-value { font-size: 24px; font-weight: 700; color: #3b82f6; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: #999; }

/* ===== Jobs Grid ===== */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  position: relative;
  min-height: 100px;
}

.jobs-grid.loading {
  opacity: 0.6;
  pointer-events: none;
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  color: #3b82f6;
  font-weight: 500;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  font-size: 15px;
  color: #999;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 24px;
  flex-wrap: wrap;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #fff;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled):not(.active) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.page-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #fff;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  margin-left: 12px;
  font-size: 13px;
  color: #999;
}

.job-card {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 20px;
  transition: all 0.2s;
  cursor: pointer;
  background: #ffffff;
}

.job-card:hover { border-color: #3b82f6; background: #f8fbff; }

.job-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.job-title { font-size: 16px; font-weight: 600; color: #1a1a1a; }

.job-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.job-badge.new { background: #dcfce7; color: #16a34a; }
.job-badge.analysis { background: #e8f0fe; color: #3b82f6; }
.job-badge.pending { background: #fef3c7; color: #d97706; }

.job-desc {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.job-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.job-tag {
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.job-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #f0f0f0; }
.job-date { font-size: 12px; color: #999; }
.view-detail { font-size: 12px; color: #3b82f6; text-decoration: none; font-weight: 500; }
.view-detail:hover { text-decoration: underline; }

/* ===== Modal ===== */
.modal-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}

.modal-overlay.active { display: flex; }

.modal {
  background: #ffffff;
  border-radius: 8px;
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title { font-size: 18px; font-weight: 600; color: #1a1a1a; }

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #e0e0e0;
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: all 0.2s;
}

.close-btn:hover { background: #f0f0f0; }

.modal-body { padding: 24px; }
.detail-section { margin-bottom: 24px; }
.section-label { font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; display: block; }
.detail-job-title { font-size: 20px; color: #1a1a1a; }
.detail-desc { font-size: 14px; color: #1a1a1a; line-height: 1.8; }
.detail-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.detail-tag { padding: 6px 12px; background: #e8f0fe; border-radius: 16px; font-size: 13px; color: #3b82f6; }

.skill-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.skill-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: #f8fafc; border-radius: 4px; }
.skill-name { font-size: 13px; color: #1a1a1a; }
.skill-level { font-size: 12px; font-weight: 600; }
.skill-level.high { color: #16a34a; }
.skill-level.medium { color: #ea580c; }
.skill-level.low { color: #666; }

.confidence-bar { height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden; }
.confidence-fill { height: 100%; background: #3b82f6; border-radius: 4px; }
.confidence-text { text-align: right; margin-top: 4px; font-size: 13px; color: #3b82f6; font-weight: 600; }

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ===== Placeholder ===== */
.placeholder-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  font-size: 16px;
  color: #999;
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .stats, .result-stats { grid-template-columns: repeat(2, 1fr); }
  .quick-actions { grid-template-columns: repeat(2, 1fr); }
  .discovery-form { grid-template-columns: repeat(2, 1fr); }
  .jobs-grid { grid-template-columns: repeat(2, 1fr); }
  .home-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .sidebar { width: 56px; padding: 12px 4px; }
  .sidebar .logo { font-size: 20px; text-align: center; padding: 8px; margin-bottom: 16px; }
  .sidebar .logo span { display: none; }
  .sidebar .nav-text { display: none; }
  .sidebar .nav-item { justify-content: center; padding: 10px; }
  .sidebar .nav-icon { margin-right: 0; }
  .sidebar .nav-section-label { display: none; }
  .sidebar .nav-divider { margin: 8px 4px; }
  .sidebar .user-detail { display: none; }
  .sidebar .user-info { justify-content: center; padding: 6px; }
  .sidebar .logout-btn span { display: none; }
  .sidebar .logout-btn { padding: 8px; }
  .toggle-btn { display: none; }
  .main { margin-left: 56px; }
  .stats, .result-stats { grid-template-columns: repeat(2, 1fr); }
  .discovery-form { grid-template-columns: 1fr; }
  .jobs-grid { grid-template-columns: 1fr; }
  .home-grid { grid-template-columns: 1fr; }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar { width: 180px; }
  .main { margin-left: 180px; }
  .sidebar.collapsed { width: 56px; }
  .sidebar.collapsed ~ .main { margin-left: 56px; }
}
</style>

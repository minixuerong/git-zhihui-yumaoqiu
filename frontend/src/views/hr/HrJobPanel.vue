<template>
  <div class="hr-job-panel">
    <!-- 头部 -->
    <div class="panel-header">
      <div class="header-left">
        <h1>岗位管理</h1>
        <p class="header-desc">管理您发布的招聘岗位，发布后用户端即可查看</p>
      </div>
      <button class="btn-create" @click="openCreate">
        <span class="btn-icon">+</span>
        <span>发布新岗位</span>
      </button>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" v-model="searchKeyword" placeholder="搜索岗位名称..." @input="onSearch">
      </div>
      <select class="filter-select" v-model="statusFilter" @change="loadJobs">
        <option value="">全部状态</option>
        <option value="active">发布中</option>
        <option value="draft">草稿</option>
        <option value="deprecated">已下架</option>
      </select>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-num">{{ stats.total }}</span>
        <span class="stat-label">全部岗位</span>
      </div>
      <div class="stat-card active">
        <span class="stat-num">{{ stats.active }}</span>
        <span class="stat-label">发布中</span>
      </div>
      <div class="stat-card">
        <span class="stat-num">{{ stats.draft }}</span>
        <span class="stat-label">草稿</span>
      </div>
      <div class="stat-card">
        <span class="stat-num">{{ stats.deprecated }}</span>
        <span class="stat-label">已下架</span>
      </div>
    </div>

    <!-- 岗位列表 -->
    <div class="job-list">
      <div v-if="jobs.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>暂无岗位</h3>
        <p>点击上方"发布新岗位"创建您的第一个招聘岗位</p>
      </div>

      <div v-for="job in jobs" :key="job.id" class="job-card">
        <div class="job-card-left">
          <div class="job-status-dot" :class="job.status"></div>
        </div>
        <div class="job-card-body">
          <div class="job-title-row">
            <h3 class="job-name">{{ job.name }}</h3>
            <span class="status-badge" :class="job.status">{{ statusLabel(job.status) }}</span>
          </div>
          <div class="job-meta">
            <span class="meta-item">
              <span class="meta-icon">📌</span>
              <code>{{ job.code }}</code>
            </span>
            <span class="meta-item" v-if="job.department">
              <span class="meta-icon">🏢</span>
              {{ job.department }}
            </span>
            <span class="meta-item">
              <span class="meta-icon">📅</span>
              {{ formatDate(job.created_at) }}
            </span>
            <span class="meta-item">
              <span class="meta-icon">👥</span>
              暂无投递
            </span>
          </div>
          <p class="job-desc" v-if="job.core_responsibilities">{{ job.core_responsibilities.slice(0, 120) }}{{ job.core_responsibilities.length > 120 ? '...' : '' }}</p>
        </div>
        <div class="job-card-actions">
          <button class="action-btn edit" title="编辑" @click="openEdit(job)">✏️</button>
          <button class="action-btn delete" title="删除" @click="confirmDelete(job)">🗑️</button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button class="page-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">‹ 上一页</button>
      <button v-for="p in totalPages" :key="p" class="page-btn" :class="{ active: p === currentPage }" @click="goToPage(p)">{{ p }}</button>
      <button class="page-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">下一页 ›</button>
      <span class="page-info">共 {{ total }} 条</span>
    </div>

    <!-- 创建/编辑弹窗 -->
    <div class="modal-overlay" :class="{ active: showForm }" @click.self="showForm = false">
      <div class="modal" style="max-width: 560px;">
        <div class="modal-header">
          <h3 class="modal-title">{{ editingJob ? '编辑岗位' : '发布新岗位' }}</h3>
          <button class="close-btn" @click="showForm = false">×</button>
        </div>
        <div class="modal-body">
          <div v-if="formError" class="error-msg">{{ formError }}</div>
          <div class="form-group">
            <label class="form-label">岗位名称 <span class="required">*</span></label>
            <input type="text" class="form-input" v-model="form.name" placeholder="如：前端开发工程师">
          </div>
          <div class="form-row">
            <div class="form-group" style="flex:1">
              <label class="form-label">岗位编码 <span class="required">*</span></label>
              <input type="text" class="form-input" v-model="form.code" placeholder="如：FE-001" :disabled="!!editingJob">
            </div>
            <div class="form-group" style="flex:1">
              <label class="form-label">所属部门</label>
              <input type="text" class="form-input" v-model="form.department" placeholder="如：技术部">
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">岗位描述 / 核心职责</label>
            <textarea class="form-textarea" v-model="form.core_responsibilities" rows="4" placeholder="描述岗位的核心职责、任职要求等"></textarea>
          </div>
          <div class="form-tip">💡 发布后岗位将在用户端"岗位发现"中可见，状态为"发布中"</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showForm = false">取消</button>
          <button class="btn btn-primary" @click="handleSubmit" :disabled="saving">
            <span v-if="saving" class="btn-loading">⏳</span>
            {{ saving ? '发布中...' : editingJob ? '保存修改' : '确认发布' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认 -->
    <div class="modal-overlay" :class="{ active: showDeleteConfirm }" @click.self="showDeleteConfirm = false">
      <div class="modal" style="max-width: 400px;">
        <div class="modal-header">
          <h3 class="modal-title">确认删除</h3>
          <button class="close-btn" @click="showDeleteConfirm = false">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-warn">
            <span class="delete-warn-icon">⚠️</span>
            <p>确定要删除岗位 <strong>{{ deletingJob?.name }}</strong> 吗？此操作不可恢复，用户端将无法查看该岗位。</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showDeleteConfirm = false">取消</button>
          <button class="btn btn-danger" @click="handleDelete" :disabled="saving">{{ saving ? '删除中...' : '确认删除' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getJobs, createJob, updateJob, deleteJob } from '@/api/jobs'

const userStore = useUserStore()

interface JobItem {
  id: number
  name: string
  code: string
  department?: string
  core_responsibilities?: string
  status: string
  created_at: string
}

const jobs = ref<JobItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = 20
const totalPages = computed(() => Math.ceil(total.value / pageSize))
const searchKeyword = ref('')
const statusFilter = ref('')

const stats = computed(() => {
  const all = jobs.value
  return {
    total: all.length,
    active: all.filter(j => j.status === 'active').length,
    draft: all.filter(j => j.status === 'draft').length,
    deprecated: all.filter(j => j.status === 'deprecated').length,
  }
})

async function loadJobs() {
  try {
    const skip = (currentPage.value - 1) * pageSize
    const res = await getJobs({
      skip,
      limit: pageSize,
      keyword: searchKeyword.value || undefined,
      status: statusFilter.value || undefined,
      uploader_id: userStore.user?.id,
    })
    jobs.value = (res.items || []).map(j => ({
      ...j,
    }))
    total.value = res.total || 0
  } catch (e) {
    console.error('加载岗位失败', e)
  }
}

function onSearch() {
  currentPage.value = 1
  loadJobs()
}

function goToPage(p: number) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  loadJobs()
}

function statusLabel(s: string) {
  return { active: '发布中', draft: '草稿', deprecated: '已下架' }[s] || s
}

function formatDate(d: string) {
  return d ? d.slice(0, 10) : ''
}

onMounted(loadJobs)

// ===== 创建/编辑 =====
const showForm = ref(false)
const editingJob = ref<JobItem | null>(null)
const saving = ref(false)
const formError = ref('')
const form = reactive({
  name: '',
  code: '',
  department: '',
  core_responsibilities: '',
})

function openCreate() {
  editingJob.value = null
  form.name = ''
  form.code = ''
  form.department = ''
  form.core_responsibilities = ''
  formError.value = ''
  showForm.value = true
}

function openEdit(job: JobItem) {
  editingJob.value = job
  form.name = job.name
  form.code = job.code
  form.department = job.department || ''
  form.core_responsibilities = job.core_responsibilities || ''
  formError.value = ''
  showForm.value = true
}

async function handleSubmit() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = '请输入岗位名称'; return }
  if (!form.code.trim()) { formError.value = '请输入岗位编码'; return }

  saving.value = true
  try {
    if (editingJob.value) {
      await updateJob(editingJob.value.id, {
        name: form.name,
        department: form.department || undefined,
        core_responsibilities: form.core_responsibilities || undefined,
      })
    } else {
      // 新建：默认发布中 + cleaned（用户端可见）
      await createJob({
        name: form.name,
        code: form.code,
        department: form.department || undefined,
        core_responsibilities: form.core_responsibilities || undefined,
        status: 'active',
        data_type: 'cleaned',
      })
    }
    showForm.value = false
    loadJobs()
  } catch (e: any) {
    formError.value = e?.response?.data?.detail || '操作失败'
  } finally {
    saving.value = false
  }
}

// ===== 删除 =====
const showDeleteConfirm = ref(false)
const deletingJob = ref<JobItem | null>(null)

function confirmDelete(job: JobItem) {
  deletingJob.value = job
  showDeleteConfirm.value = true
}

async function handleDelete() {
  if (!deletingJob.value) return
  saving.value = true
  try {
    await deleteJob(deletingJob.value.id)
    showDeleteConfirm.value = false
    loadJobs()
  } catch (e: any) {
    console.error('删除失败', e)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.hr-job-panel {
  max-width: 1200px;
  animation: fadeUp 0.3s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Header ===== */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-left h1 {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.3px;
}

.header-desc {
  font-size: 14px;
  color: #9ca3af;
  margin-top: 6px;
}

.btn-create {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);
}

.btn-create:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
}

.btn-create:active {
  transform: translateY(0);
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  font-size: 14px;
  font-weight: 300;
}

/* ===== Toolbar ===== */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-box {
  flex: 1;
  max-width: 360px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
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
  height: 40px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1f2937;
  background: transparent;
}

.search-input::placeholder { color: #9ca3af; }

.filter-select {
  padding: 0 14px;
  height: 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  background: #fff;
  min-width: 130px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:focus { border-color: #8b5cf6; }

/* ===== Stats ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s;
}

.stat-card:hover { border-color: #d1d5db; }

.stat-card.active {
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border-color: #c4b5fd;
}

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
}

.stat-card.active .stat-num { color: #7c3aed; }

.stat-label {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 500;
}

/* ===== Job List ===== */
.job-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.job-card {
  display: flex;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.2s ease;
  position: relative;
}

.job-card:hover {
  border-color: #c4b5fd;
  box-shadow: 0 2px 12px rgba(139, 92, 246, 0.08);
}

.job-card-left {
  width: 4px;
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 22px;
}

.job-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.job-status-dot.active { background: #22c55e; box-shadow: 0 0 6px rgba(34, 197, 94, 0.4); }
.job-status-dot.draft { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.3); }
.job-status-dot.deprecated { background: #9ca3af; }

.job-card-body {
  flex: 1;
  padding: 16px 16px 16px 8px;
}

.job-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.job-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.status-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2px;
}

.status-badge.active { background: #dcfce7; color: #16a34a; }
.status-badge.draft { background: #fef3c7; color: #d97706; }
.status-badge.deprecated { background: #f3f4f6; color: #9ca3af; }

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 6px;
}

.meta-item {
  font-size: 13px;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 3px;
}

.meta-icon { font-size: 12px; }

.meta-item code {
  padding: 1px 6px;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 12px;
  color: #6b7280;
}

.job-desc {
  font-size: 13px;
  color: #9ca3af;
  margin: 6px 0 0;
  line-height: 1.5;
}

.job-card-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  border-left: 1px solid #f3f4f6;
  justify-content: flex-start;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn.edit:hover { border-color: #8b5cf6; background: #f5f3ff; }
.action-btn.delete:hover { border-color: #fca5a5; background: #fef2f2; }

/* ===== Empty ===== */
.empty-state {
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
  padding: 0 14px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled):not(.active) { border-color: #8b5cf6; color: #8b5cf6; }
.page-btn.active { background: #8b5cf6; border-color: #8b5cf6; color: #fff; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.page-info { margin-left: 12px; font-size: 13px; color: #9ca3af; }

/* ===== Form ===== */
.form-row {
  display: flex;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.form-input, .form-select {
  height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  background: #fff;
  color: #111827;
}

.form-input:focus, .form-select:focus { border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }
.form-input::placeholder { color: #9ca3af; }
.form-input:disabled { background: #f9fafb; color: #9ca3af; cursor: not-allowed; }

.form-textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  resize: vertical;
  font-family: inherit;
  transition: all 0.2s;
  color: #111827;
}

.form-textarea:focus { border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }

.form-tip {
  margin-top: 8px;
  padding: 10px 14px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  font-size: 13px;
  color: #16a34a;
}

.required { color: #dc2626; }

/* ===== Modal override ===== */
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}

.modal-overlay.active { display: flex; }

.modal {
  background: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: modalIn 0.25s ease;
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title { font-size: 18px; font-weight: 600; color: #111827; }

.close-btn {
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 1px solid #e5e7eb;
  background: #fafafa;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  font-size: 16px; color: #6b7280;
  transition: all 0.2s;
}

.close-btn:hover { background: #f3f4f6; }

.modal-body { padding: 24px; }

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ===== Buttons ===== */
.btn {
  padding: 9px 20px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: #fff;
  border: none;
}

.btn-primary:hover { box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-secondary { background: #fff; color: #374151; }
.btn-secondary:hover { background: #f9fafb; border-color: #9ca3af; }

.btn-danger {
  background: #dc2626;
  color: #fff;
  border: none;
}

.btn-danger:hover { background: #b91c1c; }

.btn-loading { margin-right: 4px; }

.error-msg {
  padding: 10px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 16px;
}

.delete-warn {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.delete-warn-icon { font-size: 20px; }

.delete-warn p {
  margin: 0;
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}
</style>

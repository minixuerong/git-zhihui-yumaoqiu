<template>
  <div class="tab-content">
    <div class="tab-header">
      <div class="tab-header-left">
        <h3 v-if="!newOnlyFilter">岗位数据管理</h3>
        <h3 v-else>今日新增岗位（{{ todayNewCount }} 个）</h3>
        <el-tag v-if="newOnlyFilter" type="success" size="small" effect="plain" style="margin-left: 8px;">今日新增筛选</el-tag>
      </div>
      <div class="tab-header-actions">
        <el-button-group style="margin-right: 8px;">
          <el-button :type="dataTypeFilter === '' ? 'primary' : 'default'" size="small" @click="setDataTypeFilter('')">
            全部<span v-if="countAll > 0" class="count-badge">{{ countAll }}</span>
          </el-button>
          <el-button :type="dataTypeFilter === 'raw' ? 'primary' : 'default'" size="small" @click="setDataTypeFilter('raw')">
            原始<span v-if="countRaw > 0" class="count-badge">{{ countRaw }}</span>
          </el-button>
          <el-button :type="dataTypeFilter === 'cleaned' ? 'primary' : 'default'" size="small" @click="setDataTypeFilter('cleaned')">
            清洗后<span v-if="countCleaned > 0" class="count-badge">{{ countCleaned }}</span>
          </el-button>
        </el-button-group>
        <el-button v-if="newOnlyFilter" @click="$emit('clear-new-filter')">显示全部</el-button>
        <el-button type="primary" @click="openJobDialog()">添加岗位</el-button>
      </div>
    </div>
    <el-card v-loading="jobLoading" shadow="never">
      <el-table :data="jobs" stripe style="width: 100%">
        <el-table-column prop="name" label="岗位名称" />
        <el-table-column prop="code" label="编码" width="120" />
        <el-table-column prop="department" label="部门" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openJobDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDeleteJob(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <div v-if="totalJobs > pageSize" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="totalJobs"
        layout="prev, pager, next, total"
        @current-change="onPageChange"
      />
    </div>

    <!-- 岗位 Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form label-width="100px">
        <el-form-item label="岗位名称">
          <el-input v-model="jobForm.name" placeholder="请输入岗位名称" />
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="jobForm.code" placeholder="请输入岗位编码" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="jobForm.department" placeholder="请输入所属部门" />
        </el-form-item>
        <el-form-item label="职责">
          <el-input v-model="jobForm.core_responsibilities" type="textarea" :rows="3" placeholder="请输入核心职责" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="jobForm.status" style="width: 100%">
            <el-option label="启用" value="active" />
            <el-option label="草稿" value="draft" />
            <el-option label="废弃" value="deprecated" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDialog" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getJobs, createJob, updateJob, deleteJob } from '@/api/jobs'
import { getDashboardStats } from '@/api/admin'

const props = defineProps<{
  newOnlyFilter: boolean
}>()

defineEmits<{
  'clear-new-filter': []
}>()

const todayNewCount = ref(0)
const jobLoading = ref(false)
const jobs = ref<any[]>([])
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const jobForm = ref({ name: '', code: '', department: '', core_responsibilities: '', status: 'draft' })
const dataTypeFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = 50
const totalJobs = ref(0)

// 各类型计数
const countAll = ref(0)
const countRaw = ref(0)
const countCleaned = ref(0)

async function loadJobs() {
  jobLoading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize
    const params: any = { skip, limit: pageSize, new_only: props.newOnlyFilter || undefined }
    if (dataTypeFilter.value) params.data_type = dataTypeFilter.value
    const res = await getJobs(params)
    jobs.value = res.items
    totalJobs.value = res.total || 0
  } catch (e) { console.error(e) }
  finally { jobLoading.value = false }
}

async function loadCounts() {
  try {
    const [allRes, rawRes, cleanedRes] = await Promise.all([
      getJobs({ limit: 1 }),
      getJobs({ limit: 1, data_type: 'raw' }),
      getJobs({ limit: 1, data_type: 'cleaned' }),
    ])
    countAll.value = allRes.total || 0
    countRaw.value = rawRes.total || 0
    countCleaned.value = cleanedRes.total || 0
  } catch (e) { console.error(e) }
}

function setDataTypeFilter(val: string) {
  dataTypeFilter.value = val
  currentPage.value = 1
  loadJobs()
}

function onPageChange() {
  loadJobs()
}

async function loadTodayNewCount() {
  try {
    const stats = await getDashboardStats()
    todayNewCount.value = stats.today_new_jobs
  } catch (e) { console.error(e) }
}

watch(() => props.newOnlyFilter, () => {
  loadJobs()
  if (props.newOnlyFilter) loadTodayNewCount()
})

function openJobDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑岗位'
    jobForm.value = { ...row }
  } else {
    dialogTitle.value = '添加岗位'
    jobForm.value = { name: '', code: '', department: '', core_responsibilities: '', status: 'draft' }
  }
  dialogVisible.value = true
}

async function saveDialog() {
  saving.value = true
  try {
    if (jobForm.value.id) {
      await updateJob(jobForm.value.id, jobForm.value)
      ElMessage.success('更新成功')
    } else {
      await createJob(jobForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadJobs()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleDeleteJob(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除岗位 "${row.name}"？`, '确认删除')
    await deleteJob(row.id)
    ElMessage.success('删除成功')
    loadJobs()
  } catch (e) { /* user cancelled */ }
}

// 首次加载
loadJobs()
loadCounts()
</script>

<style scoped>
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.tab-header-left { display: flex; align-items: center; }
.tab-header-actions { display: flex; align-items: center; gap: 8px; }
.tab-header h3 { font-size: 16px; font-weight: 600; color: #1a1a1a; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.count-badge {
  display: inline-block;
  margin-left: 4px;
  padding: 0 6px;
  font-size: 11px;
  line-height: 16px;
  border-radius: 8px;
  background: rgba(0,0,0,0.08);
  color: inherit;
}
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
</style>

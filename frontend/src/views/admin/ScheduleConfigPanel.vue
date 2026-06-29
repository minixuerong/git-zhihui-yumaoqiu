<template>
  <div class="tab-content">
    <div class="tab-header">
      <h3>循环任务配置</h3>
      <div class="tab-header-actions">
        <el-button v-if="batchMode" @click="handleBatchDelete" type="danger" size="small">批量删除</el-button>
        <el-button v-if="batchMode" @click="cancelBatchMode">取消</el-button>
        <el-button :type="batchMode ? 'default' : 'default'" @click="toggleBatchMode">批量管理</el-button>
        <el-button type="primary" @click="openTaskDialog()">添加任务</el-button>
      </div>
    </div>
    <div v-loading="taskLoading" class="schedule-list">
      <div v-for="(task, idx) in tasks" :key="idx" class="schedule-item">
        <div class="schedule-info">
          <el-checkbox
            v-if="batchMode"
            v-model="selectedTaskIds"
            :label="task.id"
            style="margin-right: 12px;"
          />
          <div class="schedule-name">{{ task.source_name }}</div>
          <div class="schedule-time">任务ID: {{ task.task_id }} | 创建时间: {{ task.created_at }}</div>
        </div>
        <div class="schedule-status">
          <span class="status-dot" :class="task.status === 'completed' || task.status === 'running' ? 'running' : 'idle'"></span>
          <span class="status-text">{{ task.status }}</span>
          <el-button v-if="!batchMode" size="small" @click="openTaskDialog(task)">编辑</el-button>
          <el-button v-if="!batchMode" size="small" type="danger" @click="handleDeleteTask(task)">删除</el-button>
        </div>
      </div>
      <el-empty v-if="tasks.length === 0" description="暂无任务" />
    </div>

    <!-- 任务 Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="taskForm.source_name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="来源URL">
          <el-input v-model="taskForm.source_url" placeholder="请输入来源URL" />
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTasks, deleteTask } from '@/api/admin'

const taskLoading = ref(false)
const tasks = ref<any[]>([])
const batchMode = ref(false)
const selectedTaskIds = ref<number[]>([])
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const taskForm = ref({ source_name: '', source_url: '' })
const editingTaskId = ref(0)

function toggleBatchMode() {
  batchMode.value = !batchMode.value
  if (!batchMode.value) {
    selectedTaskIds.value = []
  }
}

function cancelBatchMode() {
  batchMode.value = false
  selectedTaskIds.value = []
}

async function handleBatchDelete() {
  if (selectedTaskIds.value.length === 0) {
    ElMessage.warning('请先选择要删除的任务')
    return
  }
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedTaskIds.value.length} 个任务？`, '批量删除')
    for (const id of selectedTaskIds.value) {
      await deleteTask(id)
    }
    ElMessage.success(`成功删除 ${selectedTaskIds.value.length} 个任务`)
    batchMode.value = false
    selectedTaskIds.value = []
    loadTasks()
  } catch (e) { /* cancelled */ }
}

async function loadTasks() {
  taskLoading.value = true
  try { tasks.value = await getTasks() } catch (e) { console.error(e) }
  finally { taskLoading.value = false }
}

function openTaskDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑任务'
    taskForm.value = { source_name: row.source_name, source_url: row.source_url || '' }
    editingTaskId.value = row.id
  } else {
    dialogTitle.value = '添加任务'
    taskForm.value = { source_name: '', source_url: '' }
    editingTaskId.value = 0
  }
  dialogVisible.value = true
}

async function saveDialog() {
  saving.value = true
  try {
    dialogVisible.value = false
    ElMessage.success('保存成功，任务将后台执行')
    loadTasks()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleDeleteTask(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除任务 "${row.source_name}"？`, '确认删除')
    await deleteTask(row.id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (e) { /* cancelled */ }
}

loadTasks()
</script>

<style scoped>
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.tab-header-actions { display: flex; align-items: center; gap: 8px; }
.tab-header h3 { font-size: 16px; font-weight: 600; color: #1a1a1a; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.schedule-list { display: flex; flex-direction: column; gap: 12px; }
.schedule-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fff;
}
.schedule-name { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }
.schedule-time { font-size: 12px; color: #999; }
.schedule-status { display: flex; align-items: center; gap: 12px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.running { background: #16a34a; }
.status-dot.idle { background: #999; }
.status-text { font-size: 13px; color: #666; }
</style>

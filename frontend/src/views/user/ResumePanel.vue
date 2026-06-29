<template>
  <div class="resume-panel">
    <div class="header">
      <div>
        <h1>简历管理</h1>
        <p>上传简历文件，支持 PDF、DOCX、DOC 格式</p>
      </div>
      <div class="user-info-bar">
        <span class="user-name">{{ username }}</span>
        <div class="user-avatar">{{ userInitial }}</div>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </div>
    </div>

    <div
      class="upload-zone"
      :class="{ dragover: isDragOver }"
      @click="triggerFileInput"
      @dragover.prevent="dragOver"
      @dragleave.prevent="dragLeave"
      @drop.prevent="onDrop"
    >
      <div class="upload-title">拖拽简历文件到此处</div>
      <div class="upload-desc">或点击选择文件，支持批量上传多个简历</div>
      <button class="btn btn-primary" @click.stop="triggerFileInput" :disabled="uploading">
        {{ uploading ? '上传中...' : '选择文件' }}
      </button>
      <input
        ref="fileInputRef"
        type="file"
        multiple
        accept=".pdf,.docx,.doc"
        style="display: none"
        @change="onFileSelected"
      />
      <div class="upload-formats">
        <span class="format-badge">PDF</span>
        <span class="format-badge">DOCX</span>
        <span class="format-badge">DOC</span>
      </div>
    </div>

    <div class="history-header">
      <h2>上传历史</h2>
      <button class="btn btn-secondary" @click="loadHistory">刷新</button>
    </div>

    <div v-loading="loading" class="history-table-wrap">
      <el-table :data="historyList" style="width: 100%" stripe v-if="historyList.length > 0">
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'parsed' ? 'success' : 'warning'" size="small">
              {{ row.status === 'parsed' ? '已解析' : '待解析' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="上传时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewResume(row)">查看</el-button>
            <el-button type="danger" link size="small" @click="deleteResumeItem(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-else-if="!loading" class="empty-state">
        <p>暂无上传记录，请上传简历文件</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { uploadResume, getResumes, deleteResume, type ResumeItem } from '@/api/resumes'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())

const isDragOver = ref(false)
const uploading = ref(false)
const loading = ref(false)
const historyList = ref<ResumeItem[]>([])
const fileInputRef = ref<HTMLInputElement | null>(null)

onMounted(() => loadHistory())

function formatTime(t?: string) {
  if (!t) return '-'
  return t.slice(0, 19).replace('T', ' ')
}

async function loadHistory() {
  loading.value = true
  try {
    historyList.value = await getResumes({ limit: 100 })
  } catch { /* ignore */ }
  finally { loading.value = false }
}

async function uploadFiles(files: File[]) {
  uploading.value = true
  try {
    for (const file of files) {
      await uploadResume(file)
    }
    ElMessage.success(`成功上传 ${files.length} 个简历文件`)
    await loadHistory()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

function viewResume(row: ResumeItem) {
  window.open(`/api/v1/resumes/${row.id}/file?token=${localStorage.getItem('token')}`, '_blank')
}

async function deleteResumeItem(row: ResumeItem) {
  try {
    await ElMessageBox.confirm(`确定删除「${row.filename}」吗？`, '确认删除')
    await deleteResume(row.id)
    ElMessage.success('删除成功')
    await loadHistory()
  } catch { /* cancelled or failed */ }
}

function triggerFileInput() {
  fileInputRef.value?.click()
}

function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    uploadFiles(Array.from(target.files))
    target.value = ''
  }
}

function onDrop(event: DragEvent) {
  isDragOver.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    uploadFiles(Array.from(event.dataTransfer.files))
  }
}

function dragOver() { isDragOver.value = true }
function dragLeave() { isDragOver.value = false }

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.resume-panel {
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
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

.btn {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #fff;
  color: #666;
}

.btn-secondary:hover {
  background: #fafafa;
}

/* ===== Upload Zone ===== */
.upload-zone {
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  padding: 60px 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
  margin-bottom: 32px;
}

.upload-zone:hover {
  border-color: #3b82f6;
  background: #f8fbff;
}

.upload-zone.dragover {
  border-color: #3b82f6;
  background: #f0f7ff;
}

.upload-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.upload-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 24px;
}

.upload-formats {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.format-badge {
  padding: 8px 20px;
  background: #f0f0f0;
  border-radius: 6px;
  font-size: 13px;
  color: #666;
}

/* ===== History Table ===== */
.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.history-table-wrap {
  min-height: 200px;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 14px;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .user-info-bar {
    width: 100%;
    justify-content: flex-end;
  }

  .upload-zone {
    padding: 40px 20px;
  }
}
</style>

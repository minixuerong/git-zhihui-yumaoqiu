<template>
  <div class="tab-content">
    <div class="tab-header">
      <h3>用户管理</h3>
      <div class="role-tabs">
        <button
          v-for="tab in roleTabs"
          :key="tab.value"
          :class="['role-tab', { active: currentRole === tab.value }]"
          @click="switchRole(tab.value)"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
          <span class="tab-count">{{ getRoleCount(tab.value) }}</span>
        </button>
      </div>
    </div>

    <el-card v-loading="loading" shadow="never" class="user-card">
      <el-table :data="filteredUsers" stripe style="width: 100%" :empty-text="emptyText">
        <el-table-column prop="username" label="用户名" min-width="120" show-overflow-tooltip />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleTagType(row.role)" size="small">{{ getRoleLabel(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="full_name" label="姓名" min-width="100" show-overflow-tooltip />
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openUserDialog(row)">编辑</el-button>
            <el-button
              v-if="row.username !== 'admin'"
              link
              :type="row.is_active ? 'warning' : 'success'"
              size="small"
              @click="handleToggleUser(row)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form label-width="100px">
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="userForm.full_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="招聘者" value="hr" />
            <el-option label="普通用户" value="user" />
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
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getUsers, updateUser } from '@/api/users'
import { getAdminUsers, getAdminList } from '@/api/admin'

interface AdminItem {
  id: number
  username: string
  is_active: boolean
  created_at: string
}

const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const userForm = ref({ email: '', full_name: '', role: 'user' })
const editingUserId = ref(0)

const currentRole = ref<'admin' | 'user' | 'hr'>('user')
const userList = ref<any[]>([])
const adminList = ref<AdminItem[]>([])

const roleTabs = [
  { value: 'user', label: '普通用户', icon: '👤', count: 0 },
  { value: 'hr', label: '招聘者', icon: '💼', count: 0 },
  { value: 'admin', label: '管理员', icon: '🔧', count: 0 },
]

const emptyText = computed(() => `暂无${getRoleLabel(currentRole.value)}数据`)

const filteredUsers = computed(() => {
  if (currentRole.value === 'admin') {
    return adminList.value.map(admin => ({
      ...admin,
      role: 'admin',
      email: '',
      full_name: '',
    }))
  }
  return userList.value.filter(u => u.role === currentRole.value)
})

function getRoleCount(role: string): number {
  if (role === 'admin') return adminList.value.length
  return userList.value.filter(u => u.role === role).length
}

function getRoleLabel(role: string): string {
  const map: Record<string, string> = {
    user: '普通用户',
    hr: '招聘者',
    admin: '管理员',
  }
  return map[role] || role
}

function getRoleTagType(role: string): string {
  const map: Record<string, string> = {
    user: 'info',
    hr: 'warning',
    admin: 'danger',
  }
  return map[role] || 'info'
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function loadAllUsers() {
  loading.value = true
  try {
    const [users, admins] = await Promise.all([getUsers(), getAdminList()])
    userList.value = users
    adminList.value = admins
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function switchRole(role: 'admin' | 'user' | 'hr') {
  currentRole.value = role
}

function openUserDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑用户'
    userForm.value = {
      email: row.email || '',
      full_name: row.full_name || '',
      role: row.role || 'user',
    }
    editingUserId.value = row.id
  }
  dialogVisible.value = true
}

async function saveDialog() {
  saving.value = true
  try {
    if (editingUserId.value) {
      await updateUser(editingUserId.value, userForm.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadAllUsers()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleToggleUser(row: any) {
  try {
    await updateUser(row.id, { is_active: !row.is_active })
    ElMessage.success(row.is_active ? '已禁用' : '已启用')
    loadAllUsers()
  } catch (e) {
    console.error(e)
  }
}

loadAllUsers()
</script>

<style scoped>
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tab-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.role-tabs {
  display: flex;
  gap: 8px;
  background: #f5f7fa;
  padding: 6px;
  border-radius: 8px;
}

.role-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
  transition: all 0.25s ease;
}

.role-tab:hover {
  background: rgba(0, 0, 0, 0.04);
  color: #303133;
}

.role-tab.active {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.tab-icon {
  font-size: 16px;
}

.tab-label {
  font-weight: 500;
}

.tab-count {
  background: rgba(255, 255, 255, 0.25);
  padding: 1px 6px;
  border-radius: 10px;
  font-size: 12px;
  min-width: 20px;
  text-align: center;
}

.role-tab:not(.active) .tab-count {
  background: #e4e7ed;
  color: #909399;
}

.user-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.tab-content {
  animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

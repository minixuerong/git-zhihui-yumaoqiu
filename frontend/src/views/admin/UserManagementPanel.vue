<template>
  <div class="tab-content">
    <div class="tab-header">
      <h3>用户管理</h3>
    </div>
    <el-card v-loading="userLoading" shadow="never">
      <el-table :data="userList" stripe style="width: 100%">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="role" label="角色" width="120" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">{{ row.is_active ? '正常' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openUserDialog(row)">编辑</el-button>
            <el-button v-if="row.username !== 'admin'" link :type="row.is_active ? 'warning' : 'success'" size="small" @click="handleToggleUser(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 用户 Dialog -->
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
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getUsers, updateUser } from '@/api/users'

const userLoading = ref(false)
const userList = ref<any[]>([])
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const userForm = ref({ email: '', full_name: '', role: 'user' })
const editingUserId = ref(0)

async function loadUserList() {
  userLoading.value = true
  try { userList.value = await getUsers() } catch (e) { console.error(e) }
  finally { userLoading.value = false }
}

function openUserDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑用户'
    userForm.value = { email: row.email || '', full_name: row.full_name || '', role: row.role || 'user' }
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
    loadUserList()
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
    loadUserList()
  } catch (e) { console.error(e) }
}

loadUserList()
</script>

<style scoped>
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.tab-header h3 { font-size: 16px; font-weight: 600; color: #1a1a1a; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

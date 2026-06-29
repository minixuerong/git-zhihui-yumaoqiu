<template>
  <div class="tab-content">
    <div class="tab-header">
      <h3>技能数据管理</h3>
      <el-button type="primary" @click="openSkillDialog()">添加技能</el-button>
    </div>
    <el-card v-loading="skillLoading" shadow="never">
      <el-table :data="skills" stripe style="width: 100%">
        <el-table-column prop="name" label="技能名称" />
        <el-table-column prop="code" label="编码" width="120" />
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openSkillDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDeleteSkill(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 技能 Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form label-width="100px">
        <el-form-item label="技能名称">
          <el-input v-model="skillForm.name" placeholder="请输入技能名称" />
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="skillForm.code" placeholder="请输入技能编码" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="skillForm.category" placeholder="请输入技能分类" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="skillForm.description" type="textarea" :rows="3" placeholder="请输入技能描述" />
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
import { getSkills, createSkill, updateSkill, deleteSkill } from '@/api/skills'

const skillLoading = ref(false)
const skills = ref<any[]>([])
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const skillForm = ref({ name: '', code: '', category: '', description: '' })

async function loadSkills() {
  skillLoading.value = true
  try {
    const res = await getSkills({ limit: 100 })
    skills.value = res.items
  } catch (e) { console.error(e) }
  finally { skillLoading.value = false }
}

function openSkillDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑技能'
    skillForm.value = { ...row }
  } else {
    dialogTitle.value = '添加技能'
    skillForm.value = { name: '', code: '', category: '', description: '' }
  }
  dialogVisible.value = true
}

async function saveDialog() {
  saving.value = true
  try {
    if (skillForm.value.id) {
      await updateSkill(skillForm.value.id, skillForm.value)
      ElMessage.success('更新成功')
    } else {
      await createSkill(skillForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadSkills()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleDeleteSkill(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除技能 "${row.name}"？`, '确认删除')
    await deleteSkill(row.id)
    ElMessage.success('删除成功')
    loadSkills()
  } catch (e) { /* cancelled */ }
}

loadSkills()
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

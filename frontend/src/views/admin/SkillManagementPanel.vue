<template>
  <div class="tab-content">
    <div class="tab-header">
      <h3>技能数据管理</h3>
      <div class="header-actions">
        <el-button type="primary" @click="showAssocDialog = true">岗位技能关联</el-button>
        <el-button type="primary" plain @click="openSkillDialog()">添加技能</el-button>
      </div>
    </div>
    <el-card v-loading="skillLoading" shadow="never">
      <el-table :data="skills" stripe style="width: 100%">
        <el-table-column prop="name" label="技能名称" />
        <el-table-column prop="code" label="编码" width="120" />
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column label="关联岗位" min-width="200">
          <template #default="{ row }">
            <div class="job-tags">
              <el-tag
                v-for="job in skillJobMap[row.id] || []"
                :key="job.job_id"
                size="small"
                type="info"
                style="margin: 2px 4px 2px 0"
              >{{ job.job_name }}</el-tag>
              <span v-if="!skillJobMap[row.id]?.length" class="no-assoc">无</span>
            </div>
          </template>
        </el-table-column>
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

    <!-- 岗位技能关联 Dialog -->
    <el-dialog v-model="showAssocDialog" title="岗位技能关联管理" width="760px" @open="loadAssocData">
      <!-- 新增关联 -->
      <div class="assoc-form">
        <el-select v-model="assocForm.job_id" placeholder="选择岗位" filterable style="width:200px;margin-right:8px">
          <el-option v-for="j in jobs" :key="j.id" :label="j.name" :value="j.id" />
        </el-select>
        <el-select v-model="assocForm.skill_id" placeholder="选择技能" filterable style="width:180px;margin-right:8px">
          <el-option v-for="s in skills" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
        <el-input-number v-model="assocForm.importance" :min="0" :max="1" :step="0.1" style="width:100px;margin-right:8px" title="重要度" />
        <el-button type="primary" @click="addAssociation" :loading="assocSaving">添加</el-button>
      </div>
      <el-divider style="margin:12px 0" />
      <!-- 已有关联列表 -->
      <el-table :data="filteredAssocList" stripe style="width:100%" max-height="400">
        <el-table-column prop="job_name" label="岗位" min-width="140" />
        <el-table-column prop="skill_name" label="技能" min-width="120" />
        <el-table-column prop="importance_score" label="重要度" width="100">
          <template #default="{ row }">
            <el-tag :type="(row.importance_score||0) >= 0.7 ? 'danger' : (row.importance_score||0) >= 0.4 ? 'warning' : 'info'" size="small">
              {{ row.importance_score || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="requirement_type" label="类型" width="80" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button link type="danger" size="small" @click="deleteAssociation(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="assoc-footer">
        <span>共 {{ filteredAssocList.length }} 条关联</span>
        <span v-if="assocForm.job_id" style="color:#999;font-size:12px">（已过滤：仅显示当前岗位）</span>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSkills, createSkill, updateSkill, deleteSkill } from '@/api/skills'
import { getCapabilities, createCapability, deleteCapability } from '@/api/capabilities'
import { getGraphJobs } from '@/api/graph'

const skillLoading = ref(false)
const skills = ref<any[]>([])
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const skillForm = ref({ id: null, name: '', code: '', category: '', description: '' })

// 关联岗位映射 { skillId: [{job_id, job_name}, ...] }
const skillJobMap = ref<Record<number, any[]>>({})

// 从 graph_data.json 读取图谱岗位名
const graphJobNames = ref<string[]>([])

async function loadGraphJobNames() {
  try {
    const mod = await import('@/assets/graph_data.json')
    const names = mod.default.nodes
      .filter((n: any) => n.category !== 8)
      .map((n: any) => n.name)
    graphJobNames.value = names
  } catch (e) {
    console.warn('加载 graph_data.json 失败', e)
  }
}

async function loadSkills() {
  skillLoading.value = true
  try {
    const res = await getSkills({ limit: 100 })
    skills.value = res.items
    // 加载每个技能的关联岗位
    const map: Record<number, any[]> = {}
    const capRes = await getCapabilities({ limit: 200 })
    for (const c of capRes.items) {
      if (!map[c.skill_id]) map[c.skill_id] = []
      map[c.skill_id].push({ job_id: c.job_id, job_name: c.job_name })
    }
    skillJobMap.value = map
  } catch (e) { console.error(e) }
  finally { skillLoading.value = false }
}

function openSkillDialog(row?: any) {
  if (row) {
    dialogTitle.value = '编辑技能'
    skillForm.value = { ...row }
  } else {
    dialogTitle.value = '添加技能'
    skillForm.value = { id: null, name: '', code: '', category: '', description: '' }
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

// ===== 岗位技能关联管理 =====
const showAssocDialog = ref(false)
const jobs = ref<any[]>([])
const assocList = ref<any[]>([])
const assocTotal = ref(0)
const assocSaving = ref(false)
const assocForm = reactive({ job_id: null as number | null, skill_id: null as number | null, importance: 0.5 })

// 按选中岗位过滤关联列表
const filteredAssocList = computed(() => {
  if (!assocForm.job_id) return assocList.value
  return assocList.value.filter((a: any) => a.job_id === assocForm.job_id)
})

async function loadAssocData() {
  // 直接从后端接口获取图谱9岗位，无需前端模糊匹配
  const [jobsRes, capRes] = await Promise.all([
    getGraphJobs(),
    getCapabilities({ limit: 200 })
  ])
  jobs.value = jobsRes
  assocList.value = capRes.items
  assocTotal.value = capRes.total
  assocForm.job_id = null
  assocForm.skill_id = null
  assocForm.importance = 0.5
}

async function addAssociation() {
  if (!assocForm.job_id || !assocForm.skill_id) {
    ElMessage.warning('请选择岗位和技能')
    return
  }
  assocSaving.value = true
  try {
    await createCapability({
      job_id: assocForm.job_id,
      skill_id: assocForm.skill_id,
      importance_score: assocForm.importance
    })
    ElMessage.success('关联添加成功')
    await loadAssocData()
    loadSkills() // 刷新表格的关联岗位列
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  } finally {
    assocSaving.value = false
  }
}

async function deleteAssociation(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除 "${row.job_name} → ${row.skill_name}" 关联？`, '确认删除')
    await deleteCapability(row.id)
    ElMessage.success('删除成功')
    await loadAssocData()
    loadSkills()
  } catch (e) { /* cancelled */ }
}

loadGraphJobNames()
loadSkills()
</script>

<style scoped>
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.tab-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}
.header-actions {
  display: flex;
  gap: 8px;
}
.tab-content {
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.job-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
.no-assoc {
  color: #bbb;
  font-size: 12px;
}
.assoc-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 4px;
}
.assoc-footer {
  text-align: right;
  margin-top: 12px;
  font-size: 13px;
  color: #999;
}
</style>

<template>
  <div class="tab-content">
    <el-card shadow="never">
      <template #header><div class="card-header"><span>更新时间配置</span></div></template>
      <el-form label-width="160px" style="max-width: 500px">
        <el-form-item label="岗位数据更新时间">
          <el-time-picker v-model="updateTimes.job" format="HH:mm" placeholder="选择时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="技能图谱更新时间">
          <el-time-picker v-model="updateTimes.skill" format="HH:mm" placeholder="选择时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="匹配模型更新时间">
          <el-time-picker v-model="updateTimes.match" format="HH:mm" placeholder="选择时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="数据来源更新频率">
          <el-select v-model="updateFrequency" style="width: 100%">
            <el-option label="每日" value="daily" />
            <el-option label="每周" value="weekly" />
            <el-option label="每月" value="monthly" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveConfig">保存配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const updateTimes = ref({
  job: new Date(2024, 0, 1, 2, 0),
  skill: new Date(2024, 0, 1, 3, 0),
  match: new Date(2024, 0, 1, 4, 0)
})
const updateFrequency = ref('daily')

function saveConfig() {
  ElMessage.success('配置保存成功')
}
</script>

<style scoped>
.card-header span { font-size: 16px; font-weight: 600; color: #1a1a1a; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

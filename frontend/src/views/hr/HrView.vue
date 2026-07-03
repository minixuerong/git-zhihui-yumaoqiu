<template>
  <div class="hr-layout">
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="logo">CAPABILITY<span>.BRAIN</span></div>
      <nav>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'graph' }" @click="activeTab = 'graph'">
          <span class="nav-icon">🔗</span>
          <span class="nav-text">全景图谱</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'jobs' }" @click="activeTab = 'jobs'">
          <span class="nav-icon">📋</span>
          <span class="nav-text">岗位管理</span>
        </a>
        <a href="javascript:void(0)" class="nav-item" :class="{ active: activeTab === 'talent' }" @click="activeTab = 'talent'">
          <span class="nav-icon">👥</span>
          <span class="nav-text">人才管理</span>
        </a>
        <div class="nav-divider"></div>
        <div class="nav-item" :class="{ active: showChangePassword }" @click="showChangePassword = true">
          <span class="nav-icon">⚙️</span>
          <span class="nav-text">系统设置</span>
        </div>
      </nav>
      <div class="toggle-btn" @click="sidebarCollapsed = !sidebarCollapsed"></div>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ userInitial }}</div>
          <div class="user-detail">
            <div class="user-name">{{ username }}</div>
            <div class="user-role">招聘者</div>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout"><span>退出登录</span></button>
      </div>
    </div>

    <div class="main">
      <!-- 能力图谱 -->
      <div v-show="activeTab === 'graph'" class="tab-content">
        <GraphPanel />
      </div>

      <!-- 岗位管理 -->
      <div v-show="activeTab === 'jobs'" class="tab-content">
        <HrJobPanel />
      </div>

      <!-- 人才管理 -->
      <div v-show="activeTab === 'talent'" class="tab-content">
        <HrTalentPanel v-if="!selectedJob" @view-applicants="selectedJob = $event" />
        <HrApplicantPanel v-else :job="selectedJob" @back="selectedJob = null" />
      </div>

      <!-- 系统设置 - 密码修改弹窗 -->
      <div class="modal-overlay" :class="{ active: showChangePassword }" @click.self="showChangePassword = false">
        <div class="modal" style="max-width: 460px;">
          <div class="modal-header">
            <h3 class="modal-title">修改密码</h3>
            <button class="close-btn" @click="showChangePassword = false">×</button>
          </div>
          <div class="modal-body">
            <div v-if="changePwdSuccess" class="success-msg">✅ 密码修改成功，下次登录请使用新密码</div>
            <div v-if="changePwdError" class="error-msg">{{ changePwdError }}</div>
            <div class="form-group">
              <label class="form-label">旧密码</label>
              <input type="password" class="form-input" v-model="passwordForm.old_password" placeholder="请输入旧密码">
            </div>
            <div class="form-group">
              <label class="form-label">新密码</label>
              <input type="password" class="form-input" v-model="passwordForm.new_password" placeholder="请输入新密码（至少6位）">
            </div>
            <div class="form-group">
              <label class="form-label">确认新密码</label>
              <input type="password" class="form-input" v-model="passwordForm.confirm_password" placeholder="再次输入新密码">
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showChangePassword = false">取消</button>
            <button class="btn btn-primary" @click="handleChangePassword" :disabled="changePwdLoading">
              {{ changePwdLoading ? '修改中...' : '确认修改' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { changePassword as changePasswordApi } from '@/api/users'
import GraphPanel from '@/views/user/GraphPanel.vue'
import HrJobPanel from './HrJobPanel.vue'
import HrTalentPanel from './HrTalentPanel.vue'
import HrApplicantPanel from './HrApplicantPanel.vue'

const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.user?.username || '用户')
const userInitial = computed(() => (username.value.charAt(0) || 'U').toUpperCase())

const sidebarCollapsed = ref(false)
const activeTab = ref('jobs')

const selectedJob = ref<any>(null)

function handleLogout() {
  userStore.logout()
  router.push('/login')
}

// ===== 密码修改 =====
const showChangePassword = ref(false)
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})
const changePwdLoading = ref(false)
const changePwdError = ref('')
const changePwdSuccess = ref(false)

async function handleChangePassword() {
  changePwdError.value = ''
  changePwdSuccess.value = false

  if (!passwordForm.old_password || !passwordForm.new_password || !passwordForm.confirm_password) {
    changePwdError.value = '请填写所有字段'
    return
  }
  if (passwordForm.new_password.length < 6) {
    changePwdError.value = '新密码长度不能少于6位'
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    changePwdError.value = '两次输入的新密码不一致'
    return
  }

  changePwdLoading.value = true
  try {
    await changePasswordApi({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
    })
    changePwdSuccess.value = true
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (e: any) {
    changePwdError.value = e?.response?.data?.detail || '密码修改失败'
  } finally {
    changePwdLoading.value = false
  }
}
</script>

<style scoped>
.hr-layout {
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

.sidebar .logo span { color: #8b5cf6; }

.sidebar.collapsed .logo { font-size: 20px; text-align: center; padding: 8px; margin-bottom: 20px; }
.sidebar.collapsed .logo span { display: none; }
.sidebar.collapsed .nav-icon { margin-right: 0; }
.sidebar.collapsed .nav-text { display: none; }
.sidebar.collapsed .nav-item { justify-content: center; padding: 10px; }
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
  background: #8b5cf6;
  border-radius: 0 1px 1px 0;
  transition: height 0.2s ease;
}

.nav-item:hover { background: #f3f4f6; color: #374151; }
.nav-item:hover::before { height: 20px; }
.nav-item.active { background: #f5f3ff; color: #8b5cf6; font-weight: 500; }
.nav-item.active::before { height: 20px; }

.nav-icon { margin-right: 10px; font-size: 14px; }

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

.toggle-btn:hover { background: #f3f4f6; color: #8b5cf6; }
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
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
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

/* ===== Modal (共用) ===== */
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
.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ===== Form ===== */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

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

.form-input:focus, .form-select:focus { border-color: #8b5cf6; }
.form-input::placeholder { color: #999; }

.btn {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary { background: #8b5cf6; color: #fff; border-color: #8b5cf6; }
.btn-primary:hover { background: #7c3aed; }
.btn-secondary { background: #fff; color: #666; }
.btn-secondary:hover { background: #fafafa; }

.success-msg {
  padding: 10px 14px;
  background: #dcfce7;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  color: #16a34a;
  font-size: 14px;
  margin-bottom: 16px;
}

.error-msg {
  padding: 10px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 16px;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .sidebar { width: 56px; padding: 12px 4px; }
  .sidebar .logo { font-size: 20px; text-align: center; padding: 8px; margin-bottom: 16px; }
  .sidebar .logo span { display: none; }
  .sidebar .nav-text { display: none; }
  .sidebar .nav-item { justify-content: center; padding: 10px; }
  .sidebar .nav-icon { margin-right: 0; }
  .sidebar .nav-divider { margin: 8px 4px; }
  .sidebar .user-detail { display: none; }
  .sidebar .user-info { justify-content: center; padding: 6px; }
  .sidebar .logout-btn span { display: none; }
  .sidebar .logout-btn { padding: 8px; }
  .toggle-btn { display: none; }
  .main { margin-left: 56px; }
}
</style>

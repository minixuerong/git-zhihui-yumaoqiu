<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="bg-pattern"></div>
    <div class="network-grid"></div>

    <!-- 顶部导航 -->
    <header class="header">
      <div class="logo">
        <div class="logo-icon">CB</div>
        <span class="logo-text">CAPABILITY<span class="logo-dot">.</span>BRAIN</span>
      </div>
      <nav class="nav-links">
        <a href="javascript:void(0)" class="nav-link">产品功能</a>
        <a href="javascript:void(0)" class="nav-link">解决方案</a>
        <a href="javascript:void(0)" class="nav-link">文档中心</a>
        <a href="javascript:void(0)" class="nav-link">关于我们</a>
      </nav>
    </header>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧 Hero -->
      <section class="hero-section">
        <h1 class="hero-title">
          人才能力<br>
          <span class="hero-highlight">智能引擎</span>
        </h1>
        <p class="hero-desc">
          基于大模型与知识图谱技术，构建新一代人才能力分析平台。
          实时感知岗位技能演变，精准匹配人才与岗位，助力数字经济时代的人才战略升级。
        </p>
        <div class="hero-stats">
          <div class="hero-stat">
            <div class="hero-stat-value">1,284</div>
            <div class="hero-stat-label">岗位覆盖</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-value">8,542</div>
            <div class="hero-stat-label">技能节点</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-value">94%</div>
            <div class="hero-stat-label">解析准确率</div>
          </div>
        </div>
      </section>

      <!-- 右侧登录 -->
      <section class="login-section">
        <div class="login-card">
          <div v-if="errorMsg" class="error-message show">{{ errorMsg }}</div>

          <h2 class="login-title">登录系统</h2>
          <p class="login-subtitle">欢迎使用人才能力大脑</p>

          <el-form
            ref="formRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @submit.prevent="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
                size="large"
                class="custom-input"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                size="large"
                show-password
                class="custom-input"
              />
            </el-form-item>

            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="javascript:void(0)" class="forgot-link">忘记密码</a>
            </div>

            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :loading="loading"
              native-type="submit"
            >
              登录
            </el-button>
          </el-form>

          <div class="divider">
            <span class="divider-line"></span>
            <span class="divider-text">或</span>
            <span class="divider-line"></span>
          </div>

          <el-button size="large" class="code-login-btn">
            使用验证码登录
          </el-button>

          <p class="signup-link">
            还没有账号? <a href="javascript:void(0)" @click="registerDialogVisible = true">立即注册</a>
          </p>
        </div>
      </section>
    </div>

    <!-- 注册弹窗 -->
    <el-dialog v-model="registerDialogVisible" title="注册账号" width="420px" :close-on-click-modal="false">
      <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="registerForm.username" placeholder="用户名（至少3位）" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="密码（至少6位）" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRegister" :loading="registerLoading">注册</el-button>
      </template>
    </el-dialog>

    <!-- 特色功能 -->
    <section class="feature-cards">
      <div class="feature-card">
        <div class="feature-icon">FIND</div>
        <h3 class="feature-title">新岗位发现</h3>
        <p class="feature-desc">基于多源数据智能识别新兴岗位，自动生成标准化岗位定义，支持人工优化与动态更新。</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">GRAPH</div>
        <h3 class="feature-title">能力图谱</h3>
        <p class="feature-desc">构建技能级能力图谱，展示领域内岗位能力要求，支持按技术栈和级别切换视图。</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">MATCH</div>
        <h3 class="feature-title">精准匹配</h3>
        <p class="feature-desc">多维度人岗匹配分析，智能差距诊断，提供针对性改进建议与学习路径规划。</p>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-links">
        <a href="javascript:void(0)" class="footer-link">服务条款</a>
        <a href="javascript:void(0)" class="footer-link">隐私政策</a>
        <a href="javascript:void(0)" class="footer-link">安全保障</a>
        <a href="javascript:void(0)" class="footer-link">联系我们</a>
      </div>
      <div class="footer-copyright">
        &copy; 2024 人才能力大脑. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const errorMsg = ref('')
const rememberMe = ref(true)

const loginForm = reactive({
  username: 'admin',
  password: 'password'
})

const loginRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 注册
const registerDialogVisible = ref(false)
const registerLoading = ref(false)
const registerFormRef = ref<FormInstance>()
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})
const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次密码输入不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function handleRegister() {
  const valid = await registerFormRef.value?.validate().catch(() => false)
  if (!valid) return

  registerLoading.value = true
  try {
    await api.post('/users/register', {
      username: registerForm.username,
      password: registerForm.password
    })
    ElMessage.success('注册成功，请登录')
    registerDialogVisible.value = false
    loginForm.username = registerForm.username
    registerForm.username = ''
    registerForm.password = ''
    registerForm.confirmPassword = ''
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '注册失败')
  } finally {
    registerLoading.value = false
  }
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  errorMsg.value = ''

  try {
    await userStore.login(loginForm.username, loginForm.password)
    if (userStore.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/user')
    }
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '用户名或密码错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #ffffff;
  color: #1e293b;
  overflow-x: hidden;
  position: relative;
}

/* ===== 背景装饰 ===== */
.bg-pattern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.network-grid {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(59, 130, 246, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* ===== 顶部导航 ===== */
.header {
  position: relative;
  z-index: 10;
  padding: 24px 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #0f172a;
}

.logo-dot {
  color: #3b82f6;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #0f172a;
}

/* ===== 主内容区 ===== */
.main-content {
  position: relative;
  z-index: 10;
  display: flex;
  min-height: calc(100vh - 80px - 200px);
}

/* -- Hero -- */
.hero-section {
  flex: 1;
  padding: 80px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.2;
  color: #0f172a;
}

.hero-highlight {
  background: linear-gradient(90deg, #3b82f6, #0ea5e9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 16px;
  color: #64748b;
  line-height: 1.8;
  max-width: 600px;
  margin-bottom: 40px;
}

.hero-stats {
  display: flex;
  gap: 48px;
}

.hero-stat {
  text-align: center;
}

.hero-stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #3b82f6;
}

.hero-stat-label {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 4px;
}

/* -- 登录 -- */
.login-section {
  width: 420px;
  padding: 80px 40px;
  background: rgba(0, 0, 0, 0.02);
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-card {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #0f172a;
}

.login-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.login-form {
  width: 100%;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forgot-link {
  font-size: 13px;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: #0ea5e9;
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  border: none;
}

.login-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #0284c7 100%);
}

.code-login-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #0f172a;
  border: 1px solid #e2e8f0;
}

.code-login-btn:hover {
  background: #e2e8f0;
}

.divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 24px 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.divider-text {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  font-size: 13px;
  color: #94a3b8;
}

.signup-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}

.error-message {
  display: none;
  padding: 12px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  font-size: 13px;
  color: #dc2626;
  margin-bottom: 16px;
}

.error-message.show {
  display: block;
}

/* 覆盖 Element Plus 输入框样式 */
:deep(.custom-input .el-input__wrapper) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: none !important;
  padding-left: 12px;
}

:deep(.custom-input .el-input__wrapper:hover) {
  border-color: #3b82f6;
}

:deep(.custom-input .el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

:deep(.custom-input .el-input__inner) {
  height: 48px;
  font-size: 14px;
}

:deep(.custom-input .el-input__prefix) {
  margin-right: 8px;
}

:deep(.custom-input .el-input__prefix-inner .el-icon) {
  font-size: 18px;
  color: #94a3b8;
}

/* ===== 特色功能 ===== */
.feature-cards {
  position: relative;
  z-index: 10;
  padding: 48px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  background: rgba(0, 0, 0, 0.02);
}

.feature-card {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  padding: 28px;
  transition: all 0.3s;
}

.feature-card:hover {
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.08);
}

.feature-icon {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #3b82f6;
  padding: 8px 12px;
  background: rgba(59, 130, 246, 0.08);
  border-radius: 4px;
  margin-bottom: 16px;
  display: inline-block;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #0f172a;
}

.feature-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

/* ===== 页脚 ===== */
.footer {
  position: relative;
  z-index: 10;
  padding: 32px 48px;
  background: rgba(0, 0, 0, 0.02);
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  font-size: 12px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-link:hover {
  color: #64748b;
}

.footer-copyright {
  font-size: 12px;
  color: #cbd5e1;
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 36px;
  }

  .login-section {
    width: 360px;
    padding: 60px 30px;
  }

  .feature-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .header {
    padding: 16px 24px;
  }

  .nav-links {
    display: none;
  }

  .main-content {
    flex-direction: column;
  }

  .hero-section {
    padding: 40px 24px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-stats {
    gap: 24px;
  }

  .hero-stat-value {
    font-size: 28px;
  }

  .login-section {
    width: 100%;
    padding: 40px 24px;
    border-left: none;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .feature-cards {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  .footer {
    flex-direction: column;
    gap: 16px;
    padding: 24px;
  }
}
</style>

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login/LoginView.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/login/admin',
      name: 'LoginAdmin',
      component: () => import('@/views/login/LoginView.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/admin/AdminView.vue'),
      meta: { title: '后台管理', requiresAuth: true, role: 'admin' }
    },
    {
      path: '/user',
      name: 'User',
      component: () => import('@/views/user/UserView.vue'),
      meta: { title: '用户首页', requiresAuth: true, role: 'user' }
    },
    {
      path: '/hr',
      name: 'Hr',
      component: () => import('@/views/hr/HrView.vue'),
      meta: { title: '招聘者工作台', requiresAuth: true, role: 'hr' }
    }
  ]
})

// 路由守卫 — 防止越权访问
router.beforeEach((to, _from, next) => {
  const saved = localStorage.getItem('user')
  const user = saved ? JSON.parse(saved) : null

  // 需要登录但未登录 → 跳登录页
  if (to.meta.requiresAuth && !user) {
    return next('/login')
  }

  // 已登录但角色不匹配 → 跳转对应首页
  if (to.meta.role && user && user.role !== to.meta.role) {
    const roleMap: Record<string, string> = {
      admin: '/admin',
      hr: '/hr',
      user: '/user'
    }
    return next(roleMap[user.role] || '/login')
  }

  next()
})

export default router

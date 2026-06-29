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
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/admin/AdminView.vue'),
      meta: { title: '后台管理', requiresAuth: true }
    },
    {
      path: '/user',
      name: 'User',
      component: () => import('@/views/user/UserView.vue'),
      meta: { title: '用户首页', requiresAuth: true }
    }
  ]
})

export default router

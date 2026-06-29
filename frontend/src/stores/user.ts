import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

interface UserInfo {
  id: number
  username: string
  role: 'admin' | 'user'
  token: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!user.value?.token)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const username = computed(() => user.value?.username || '')

  function setUser(info: UserInfo) {
    user.value = info
    localStorage.setItem('token', info.token)
    localStorage.setItem('user', JSON.stringify(info))
  }

  function loadFromStorage() {
    const token = localStorage.getItem('token')
    const saved = localStorage.getItem('user')
    if (token && saved) {
      user.value = JSON.parse(saved)
    }
  }

  async function login(username: string, password: string) {
    // 1. 调登录接口拿 token
    const tokenRes: any = await api.post('/users/login', { username, password })
    const token = tokenRes.access_token

    // 2. 临时保存 token，用于后续请求
    localStorage.setItem('token', token)

    // 3. 调 /users/me 获取用户信息
    const userRes: any = await api.get('/users/me')

    setUser({
      id: userRes.id,
      username: userRes.username,
      role: userRes.role,
      token: token
    })
    return userRes
  }

  function logout() {
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { user, isLoggedIn, isAdmin, username, setUser, loadFromStorage, login, logout }
})

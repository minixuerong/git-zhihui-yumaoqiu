import api from './index'

export interface User {
  id: number
  username: string
  email?: string
  full_name?: string
  role: string
  is_active: boolean
  created_at: string
}

export function getUsers() {
  return api.get<any, User[]>('/users/')
}

export function updateUser(id: number, data: { email?: string; full_name?: string; role?: string; is_active?: boolean }) {
  return api.put<any, User>(`/users/${id}`, data)
}

export function deleteUser(id: number) {
  return api.delete(`/users/${id}`)
}

export function changePassword(data: { old_password: string; new_password: string }) {
  return api.post('/users/change-password', data)
}

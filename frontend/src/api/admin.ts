import api from './index'

export interface DashboardStats {
  total_jobs: number
  total_skills: number
  total_users: number
  pending_updates: number
  today_new_jobs: number
}

export interface EvolutionRecord {
  id: number
  job_id: number
  job_name: string
  changes_summary: string
  changed_fields: string
  evolution_type: string
  created_at: string
}

export interface CrawlTask {
  id: number
  task_id: string
  source_name: string
  source_url: string
  status: string
  crawl_time: string | null
  clean_time: string | null
  analysis_time: string | null
  error_message: string | null
  created_at: string
}

export function getDashboardStats() {
  return api.get<any, DashboardStats>('/admin/dashboard/stats')
}

export function getEvolutions(skip = 0, limit = 20) {
  return api.get<any, EvolutionRecord[]>('/admin/evolutions', { params: { skip, limit } })
}

export function getTasks(skip = 0, limit = 100) {
  return api.get<any, CrawlTask[]>('/admin/tasks', { params: { skip, limit } })
}

export function deleteTask(taskId: number) {
  return api.delete(`/admin/tasks/${taskId}`)
}

export interface AdminItem {
  id: number
  username: string
  is_active: boolean
  created_at: string
}

export function getAdminUsers(role?: string) {
  return api.get<any, any[]>('/admin/users', { params: { role } })
}

export function getAdminList() {
  return api.get<any, AdminItem[]>('/admin/admins')
}

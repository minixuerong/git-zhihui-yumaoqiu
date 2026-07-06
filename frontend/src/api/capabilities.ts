import api from './index'

export interface Capability {
  id: number
  job_id: number
  skill_id: number
  job_name: string
  skill_name: string
  requirement_type: string
  level_required?: string
  importance_score?: number
  created_at?: string
  updated_at?: string
}

export interface PaginatedCapabilities {
  items: Capability[]
  total: number
  page: number
  size: number
}

export function getCapabilities(params: {
  skip?: number
  limit?: number
  job_id?: number
  skill_id?: number
} = {}) {
  return api.get<any, PaginatedCapabilities>('/capabilities/', { params })
}

export function createCapability(data: {
  job_id: number
  skill_id: number
  requirement_type?: string
  level_required?: string
  importance_score?: number
}) {
  return api.post<any, Capability>(`/capabilities/?job_id=${data.job_id}`, {
    skill_id: data.skill_id,
    requirement_type: data.requirement_type || 'required',
    level_required: data.level_required || null,
    importance_score: data.importance_score || 0.5
  })
}

export function updateCapability(id: number, data: {
  skill_id: number
  requirement_type?: string
  level_required?: string
  importance_score?: number
}) {
  return api.put<any, Capability>(`/capabilities/${id}`, data)
}

export function deleteCapability(id: number) {
  return api.delete(`/capabilities/${id}`)
}

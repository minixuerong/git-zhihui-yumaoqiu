import api from './index'

export interface Skill {
  id: number
  name: string
  code: string
  category?: string
  description?: string
  created_at: string
}

export interface PaginatedSkills {
  items: Skill[]
  total: number
  page: number
  size: number
}

export function getSkills({ skip = 0, limit = 10, category, keyword }: {
  skip?: number
  limit?: number
  category?: string
  keyword?: string
} = {}) {
  return api.get<any, PaginatedSkills>('/skills/', {
    params: { skip, limit, category, keyword }
  })
}

export function createSkill(data: { name: string; code: string; category?: string; description?: string }) {
  return api.post<any, Skill>('/skills/', data)
}

export function updateSkill(id: number, data: Partial<Skill>) {
  return api.put<any, Skill>(`/skills/${id}`, data)
}

export function deleteSkill(id: number) {
  return api.delete(`/skills/${id}`)
}

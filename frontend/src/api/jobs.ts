import api from './index'

export interface Job {
  id: number
  name: string
  code: string
  department?: string
  core_responsibilities?: string
  status?: string
  is_new?: boolean
  data_source?: string
  data_type?: string
  uploader_id?: number
  confidence_score?: number
  created_at: string
  updated_at: string
}

export interface PaginatedJobs {
  items: Job[]
  total: number
  page: number
  size: number
}

export function getJobs({ skip = 0, limit = 10, keyword, status, new_only, data_type, uploader_id }: {
  skip?: number
  limit?: number
  keyword?: string
  status?: string
  new_only?: boolean
  data_type?: string
  uploader_id?: number
} = {}) {
  return api.get<any, PaginatedJobs>('/jobs/', {
    params: { skip, limit, keyword, status, new_only, data_type, uploader_id }
  })
}

export function getJob(id: number) {
  return api.get<any, Job>(`/jobs/${id}`)
}

export function createJob(data: {
  name: string
  code: string
  department?: string
  core_responsibilities?: string
  status?: string
  data_type?: string
}) {
  return api.post<any, Job>('/jobs/', data)
}

export function updateJob(id: number, data: Partial<Job>) {
  return api.put<any, Job>(`/jobs/${id}`, data)
}

export function deleteJob(id: number) {
  return api.delete(`/jobs/${id}`)
}

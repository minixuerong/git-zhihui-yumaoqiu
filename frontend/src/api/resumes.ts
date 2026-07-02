import api from './index'

export interface ResumeItem {
  id: number
  filename: string
  file_path: string
  content: string | null
  parsed_skills: string | null
  parsed_data: string | null
  parsed_at: string | null
  uploader_id: number | null
  status: string
  created_at: string
}

/** 上传简历文件 */
export function uploadResume(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post<any, ResumeItem>('/resumes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/** 获取简历列表 */
export function getResumes(params?: { skip?: number; limit?: number }) {
  return api.get<any, ResumeItem[]>('/resumes/', { params })
}

/** 删除简历 */
export function deleteResume(id: number) {
  return api.delete(`/resumes/${id}`)
}

/** 匹配分析 */
export function matchAnalysis(resumeId: number, jobId: number) {
  return api.post<any, {
    match_score: number
    gap_analysis: Array<{
      skill_id: number
      skill_name: string
      current_level: string | null
      required_level: string
      gap: string | number
    }>
    improvement_suggestions: string[]
    learning_path: string[]
  }>('/match/analysis', { resume_id: resumeId, job_id: jobId })
}

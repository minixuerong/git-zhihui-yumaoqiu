import api from './index'

export function getGraphData() {
  return api.get('/graph/data')
}

export function getGraphJobs() {
  return api.get('/graph/jobs')
}

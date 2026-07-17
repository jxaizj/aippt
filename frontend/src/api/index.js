import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 — 自动解包 DRF 分页
api.interceptors.response.use(
  (response) => {
    const data = response.data
    // DRF 分页响应: {count, next, previous, results}
    if (data && typeof data === 'object' && Array.isArray(data.results)) {
      return data.results
    }
    return data
  },
  (error) => {
    const message = error.response?.data?.error || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default api

// ============ 会话 API ============
export const sessionApi = {
  list: (params = {}) => api.get('/sessions/', { params }),
  get: (id) => api.get(`/sessions/${id}/`),
  create: (data) => api.post('/sessions/', data),
  update: (id, data) => api.patch(`/sessions/${id}/`, data),
  delete: (id) => api.delete(`/sessions/${id}/`),
  duplicate: (id) => api.post(`/sessions/${id}/duplicate/`),
  saveAsTemplate: (id, data) => api.post(`/sessions/${id}/save_as_template/`, data),
  getMessages: (id) => api.get(`/sessions/${id}/messages/`),
  getPages: (id) => api.get(`/sessions/${id}/pages/`),
  getOperations: (id) => api.get(`/sessions/${id}/operations/`),
  getSpeeches: (id) => api.get(`/sessions/${id}/speeches/`),
}

// ============ 消息 API ============
export const messageApi = {
  list: (params = {}) => api.get('/sessions/messages/', { params }),
  create: (data) => api.post('/sessions/messages/', data),
}

// ============ 页面 API ============
export const pageApi = {
  list: (params = {}) => api.get('/sessions/pages/', { params }),
  get: (id) => api.get(`/sessions/pages/${id}/`),
  update: (id, data) => api.patch(`/sessions/pages/${id}/`, data),
  updateContent: (id, data) => api.post(`/sessions/pages/${id}/update_content/`, data),
  delete: (id) => api.delete(`/sessions/pages/${id}/`),
}

// ============ 风格 API ============
export const styleApi = {
  list: () => api.get('/sessions/styles/'),
  get: (id) => api.get(`/sessions/styles/${id}/`),
  create: (data) => api.post('/sessions/styles/', data),
  update: (id, data) => api.patch(`/sessions/styles/${id}/`, data),
  delete: (id) => api.delete(`/sessions/styles/${id}/`),
  toggleFavorite: (id) => api.post(`/sessions/styles/${id}/toggle_favorite/`),
}

// ============ 模板 API ============
export const templateApi = {
  list: () => api.get('/sessions/templates/'),
  get: (id) => api.get(`/sessions/templates/${id}/`),
  create: (data) => api.post('/sessions/templates/', data),
  update: (id, data) => api.patch(`/sessions/templates/${id}/`, data),
  delete: (id) => api.delete(`/sessions/templates/${id}/`),
  createSession: (id, data) => api.post(`/sessions/templates/${id}/create_session/`, data),
}

// ============ 模型配置 API ============
export const modelConfigApi = {
  list: () => api.get('/sessions/model-configs/'),
  get: (id) => api.get(`/sessions/model-configs/${id}/`),
  create: (data) => api.post('/sessions/model-configs/', data),
  update: (id, data) => api.patch(`/sessions/model-configs/${id}/`, data),
  delete: (id) => api.delete(`/sessions/model-configs/${id}/`),
  setActive: (id) => api.post(`/sessions/model-configs/${id}/set_active/`),
}

// ============ AI 引擎 API ============
export const aiApi = {
  generate: (data) => api.post('/ai/generate/', data),
  chatEdit: (data) => api.post('/ai/chat-edit/', data),
  generateSpeech: (data) => api.post('/ai/generate-speech/', data),
  generateOutline: (data) => api.post('/ai/generate-outline/', data),
  uploadDocument: (formData) => api.post('/ai/upload-document/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  importPptx: (formData) => api.post('/ai/import-pptx/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  analyzeImage: (formData) => api.post('/ai/analyze-image/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
}

// ============ 编辑器 API ============
export const editorApi = {
  updatePage: (data) => api.post('/editor/update-page/', data),
  moveElement: (data) => api.post('/editor/move-element/', data),
  resizeElement: (data) => api.post('/editor/resize-element/', data),
  deleteElement: (data) => api.post('/editor/delete-element/', data),
  copyElement: (data) => api.post('/editor/copy-element/', data),
  addElement: (data) => api.post('/editor/add-element/', data),
  setAnimation: (data) => api.post('/editor/set-animation/', data),
  removeAnimation: (data) => api.post('/editor/remove-animation/', data),
  reorderPages: (data) => api.post('/editor/reorder-pages/', data),
  deletePage: (data) => api.post('/editor/delete-page/', data),
  addPage: (data) => api.post('/editor/add-page/', data),
  undo: (data) => api.post('/editor/undo/', data),
  redo: (data) => api.post('/editor/redo/', data),
  rollback: (data) => api.post('/editor/rollback/', data),
}

// ============ 导出 API ============
export const exportApi = {
  pdf: (data) => api.post('/export/pdf/', data),
  png: (data) => api.post('/export/png/', data),
  pptx: (data) => api.post('/export/pptx/', data),
  mp4: (data) => api.post('/export/mp4/', data),
  html: (data) => api.post('/export/html/', data),
  download: (taskId) => `/api/export/download/${taskId}/`,
  tasks: (params = {}) => api.get('/export/tasks/', { params }),
}

// ============ 设置 API ============
export const settingsApi = {
  getAll: () => api.get('/settings/all/'),
  update: (data) => api.post('/settings/update/', data),
  getPreferences: () => api.get('/settings/preferences/'),
  updatePreference: (data) => api.post('/settings/preferences/update/', data),
  getModelUsage: () => api.get('/settings/model-usage/'),
  recordUsage: (data) => api.post('/settings/model-usage/record/', data),
}

// ============ 字体 API ============
export const fontApi = {
  list: () => api.get('/sessions/fonts/'),
  create: (data) => api.post('/sessions/fonts/', data),
  delete: (id) => api.delete(`/sessions/fonts/${id}/`),
}

// ============ 图片 API ============
export const imageApi = {
  list: (params = {}) => api.get('/sessions/images/', { params }),
  upload: (formData) => api.post('/sessions/images/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (id) => api.delete(`/sessions/images/${id}/`),
}

// ============ 演讲稿 API ============
export const speechApi = {
  list: (params = {}) => api.get('/sessions/speeches/', { params }),
  create: (data) => api.post('/sessions/speeches/', data),
  delete: (id) => api.delete(`/sessions/speeches/${id}/`),
}

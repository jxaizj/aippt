import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sessionApi, styleApi, modelConfigApi } from '@/api'

export const useSessionStore = defineStore('session', () => {
  const sessions = ref([])
  const currentSession = ref(null)
  const currentPages = ref([])
  const currentMessages = ref([])
  const loading = ref(false)

  const sortedSessions = computed(() => {
    return [...sessions.value].sort((a, b) =>
      new Date(b.updated_at) - new Date(a.updated_at)
    )
  })

  async function fetchSessions(params = {}) {
    loading.value = true
    try {
      const res = await sessionApi.list(params)
      sessions.value = res.results || res
    } finally {
      loading.value = false
    }
  }

  async function fetchSession(id) {
    loading.value = true
    try {
      currentSession.value = await sessionApi.get(id)
      return currentSession.value
    } finally {
      loading.value = false
    }
  }

  async function fetchPages(id) {
    currentPages.value = await sessionApi.getPages(id)
    return currentPages.value
  }

  async function fetchMessages(id) {
    currentMessages.value = await sessionApi.getMessages(id)
    return currentMessages.value
  }

  async function createSession(data) {
    const session = await sessionApi.create(data)
    return session
  }

  async function updateSession(id, data) {
    const session = await sessionApi.update(id, data)
    if (currentSession.value?.id === id) {
      currentSession.value = session
    }
    return session
  }

  async function deleteSession(id) {
    await sessionApi.delete(id)
    sessions.value = sessions.value.filter(s => s.id !== id)
  }

  return {
    sessions, currentSession, currentPages, currentMessages, loading,
    sortedSessions, fetchSessions, fetchSession, fetchPages, fetchMessages,
    createSession, updateSession, deleteSession,
  }
})

export const useStyleStore = defineStore('style', () => {
  const styles = ref([])
  const loading = ref(false)

  async function fetchStyles() {
    loading.value = true
    try {
      styles.value = await styleApi.list()
    } finally {
      loading.value = false
    }
  }

  async function toggleFavorite(id) {
    const updated = await styleApi.toggleFavorite(id)
    const idx = styles.value.findIndex(s => s.id === id)
    if (idx >= 0) styles.value[idx] = updated
  }

  return { styles, loading, fetchStyles, toggleFavorite }
})

export const useModelConfigStore = defineStore('modelConfig', () => {
  const configs = ref([])
  const activeConfig = ref(null)
  const loading = ref(false)

  async function fetchConfigs() {
    loading.value = true
    try {
      configs.value = await modelConfigApi.list()
      activeConfig.value = configs.value.find(c => c.active) || configs.value[0] || null
    } finally {
      loading.value = false
    }
  }

  async function setActive(id) {
    const config = await modelConfigApi.setActive(id)
    configs.value = configs.value.map(c => ({
      ...c,
      active: c.id === id
    }))
    activeConfig.value = config
  }

  async function createConfig(data) {
    const config = await modelConfigApi.create(data)
    configs.value.push(config)
    return config
  }

  async function updateConfig(id, data) {
    const config = await modelConfigApi.update(id, data)
    const idx = configs.value.findIndex(c => c.id === id)
    if (idx >= 0) configs.value[idx] = config
    return config
  }

  async function deleteConfig(id) {
    await modelConfigApi.delete(id)
    configs.value = configs.value.filter(c => c.id !== id)
  }

  return { configs, activeConfig, loading, fetchConfigs, setActive, createConfig, updateConfig, deleteConfig }
})

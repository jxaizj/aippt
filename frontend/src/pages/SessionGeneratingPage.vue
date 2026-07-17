<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center">
    <div class="max-w-lg w-full mx-4">
      <!-- 生成过程流式显示 -->
      <div
        v-if="streamLog.length"
        class="bg-gray-900 rounded-2xl p-4 shadow-sm border border-gray-800 mb-6"
      >
        <div class="flex items-center space-x-2 mb-3">
          <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
          <span class="w-2.5 h-2.5 rounded-full bg-yellow-400"></span>
          <span class="w-2.5 h-2.5 rounded-full bg-green-400"></span>
          <span class="text-xs text-gray-400 ml-2">生成过程</span>
        </div>
        <div
          ref="logBox"
          class="font-mono text-xs text-green-300 leading-relaxed max-h-64 overflow-y-auto whitespace-pre-wrap"
        >
          <div v-for="(line, idx) in streamLog" :key="idx">{{ line }}</div>
          <div v-if="generationStatus === 'running'" class="text-gray-500">
            <span class="animate-pulse">▍</span>
          </div>
        </div>
      </div>

      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <el-icon size="32" class="text-white"><Loading /></el-icon>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">AI 正在生成您的演示稿</h1>
        <p class="text-gray-500">{{ statusMessage }}</p>
      </div>

      <!-- 进度条 -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700">生成进度</span>
          <span class="text-sm text-green-600 font-medium">{{ progress }}%</span>
        </div>
        <el-progress :percentage="progress" :stroke-width="10" :status="progressStatus" />
        <div class="mt-4 flex items-center justify-between text-xs text-gray-400">
          <span>{{ completedPages }} / {{ totalPages }} 页</span>
          <span>预计剩余 {{ remainingTime }}</span>
        </div>
      </div>

      <!-- 页面生成状态 -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h3 class="font-medium text-gray-700 mb-3">页面状态</h3>
        <div class="space-y-2 max-h-60 overflow-y-auto">
          <div
            v-for="page in pages"
            :key="page.id"
            class="flex items-center justify-between py-2 px-3 rounded-lg"
            :class="pageStatusClass(page.status)"
          >
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium">第{{ page.page_number }}页</span>
              <span class="text-sm text-gray-500 truncate max-w-48">{{ page.title || '生成中...' }}</span>
            </div>
            <el-icon v-if="page.status === 'completed'" class="text-green-500"><Check /></el-icon>
            <el-icon v-else-if="page.status === 'running'" class="animate-spin text-blue-500"><Loading /></el-icon>
            <el-icon v-else-if="page.status === 'failed'" class="text-red-500"><Close /></el-icon>
            <el-icon v-else class="text-gray-400"><Clock /></el-icon>
          </div>
        </div>
      </div>

      <!-- 取消按钮 -->
      <div class="text-center mt-6">
        <el-button @click="handleCancel">取消生成</el-button>
        <el-button
          v-if="isCompleted"
          type="primary"
          @click="gotoEdit"
          class="bg-green-600 hover:bg-green-700 border-green-600"
        >
          开始编辑 →
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

const sessionId = ref(route.params.id)
const totalPages = ref(10)
const completedPages = ref(0)
const pages = ref([])
const statusMessage = ref('正在规划大纲...')
const generationStatus = ref('running') // running, completed, failed
const streamLog = ref([])
const logBox = ref(null)
let ws = null
let pollTimer = null

const progress = computed(() => {
  if (totalPages.value === 0) return 0
  return Math.round((completedPages.value / totalPages.value) * 100)
})

const progressStatus = computed(() => {
  if (generationStatus.value === 'completed') return 'success'
  if (generationStatus.value === 'failed') return 'exception'
  return ''
})

const isCompleted = computed(() => generationStatus.value === 'completed')

const remainingTime = computed(() => {
  const remaining = totalPages.value - completedPages.value
  const seconds = remaining * 5
  if (seconds < 60) return `${seconds}秒`
  return `${Math.ceil(seconds / 60)}分钟`
})

onMounted(() => {
  connectWebSocket()
  startPolling()
})

onUnmounted(() => {
  if (ws) ws.close()
  if (pollTimer) clearInterval(pollTimer)
})

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  ws = new WebSocket(`${protocol}//${window.location.host}/ws/generation/${sessionId.value}/`)
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    handleWSMessage(data)
  }
  ws.onopen = () => {
    ws.send(JSON.stringify({ action: 'start_generation' }))
  }
}

function handleWSMessage(data) {
  if (data.type === 'generation_status') {
    statusMessage.value = data.message
  } else if (data.type === 'page_completed') {
    const page = pages.value.find(p => p.page_number === data.page_number)
    if (page) {
      page.status = 'completed'
      page.title = data.title || page.title
    }
    completedPages.value++
  } else if (data.type === 'generation_completed') {
    generationStatus.value = 'completed'
    statusMessage.value = '生成完成！'
  } else if (data.type === 'generation_error') {
    generationStatus.value = 'failed'
    statusMessage.value = `生成失败: ${data.error}`
  }
}

async function startPolling() {
  pollTimer = setInterval(async () => {
    try {
      // 先读取生成运行状态与生成过程流式日志
      const runRes = await fetch(`/api/sessions/generation-runs/?session=${sessionId.value}`)
      const runData = await runRes.json()
      const runs = runData.results || runData
      if (Array.isArray(runs) && runs.length > 0) {
        const latest = runs[0]

        // 更新流式生成过程日志
        const log = latest.metadata?.stream_log
        if (Array.isArray(log) && log.length !== streamLog.value.length) {
          streamLog.value = log
          scrollLogToBottom()
        }

        if (latest.status === 'failed') {
          generationStatus.value = 'failed'
          statusMessage.value = `生成失败: ${latest.error || '未知错误'}`
          clearInterval(pollTimer)
          return
        }
      }

      // 再读取页面进度
      const res = await fetch(`/api/sessions/${sessionId.value}/pages/`)
      const data = await res.json()
      pages.value = data.results || data
      completedPages.value = pages.value.filter(p => p.status === 'completed').length
      totalPages.value = pages.value.length

      if (completedPages.value === totalPages.value && totalPages.value > 0) {
        generationStatus.value = 'completed'
        statusMessage.value = '生成完成！'
        clearInterval(pollTimer)
      }
    } catch (e) {
      console.error('Polling error:', e)
    }
  }, 1500)
}

async function handleCancel() {
  try {
    await ElMessageBox.confirm('确定要取消生成吗？', '提示', { type: 'warning' })
    if (ws) ws.close()
    router.push(`/session/${sessionId.value}`)
  } catch (e) {
    // cancelled
  }
}

function gotoEdit() {
  router.push(`/session/${sessionId.value}`)
}

function scrollLogToBottom() {
  nextTick(() => {
    if (logBox.value) {
      logBox.value.scrollTop = logBox.value.scrollHeight
    }
  })
}

function pageStatusClass(status) {
  const map = {
    completed: 'bg-green-50',
    running: 'bg-blue-50',
    failed: 'bg-red-50',
    pending: 'bg-gray-50',
  }
  return map[status] || 'bg-gray-50'
}
</script>

<template>
  <div class="min-h-screen bg-gray-900 flex flex-col">
    <!-- 顶部工具栏 -->
    <header class="bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between z-20">
      <div class="flex items-center space-x-4">
        <router-link to="/" class="flex items-center space-x-2 text-white">
          <div class="w-7 h-7 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">P</span>
          </div>
          <span class="font-medium">Oh My PPT</span>
        </router-link>
        <span class="text-gray-500">|</span>
        <span class="text-gray-300 text-sm">{{ sessionStore.currentSession?.title || '加载中...' }}</span>
      </div>
      <div class="flex items-center space-x-2">
        <el-button size="small" @click="handleUndo" :disabled="!canUndo">↩ 撤销</el-button>
        <el-button size="small" @click="handleRedo" :disabled="!canRedo">↪ 重做</el-button>
        <el-button size="small" @click="showVersionDialog = true">历史版本</el-button>
        <el-divider direction="vertical" />
        <el-button size="small" @click="showExportDialog = true">导出</el-button>
        <el-button size="small" type="primary" @click="handlePreview">预览</el-button>
      </div>
    </header>

    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧页面列表 -->
      <aside class="w-48 bg-gray-800 border-r border-gray-700 overflow-y-auto p-3 space-y-2">
        <div
          v-for="page in sessionStore.currentPages"
          :key="page.id"
          class="relative cursor-pointer rounded-lg overflow-hidden border-2 transition"
          :class="currentPageId === page.id ? 'border-green-500' : 'border-transparent hover:border-gray-600'"
          @click="selectPage(page.id)"
        >
          <div class="bg-white aspect-video flex items-center justify-center text-xs text-gray-600 p-1">
            <div v-if="page.html_content" class="w-full h-full overflow-hidden text-[4px]" v-html="page.html_content"></div>
            <span v-else class="text-gray-400">第{{ page.page_number }}页</span>
          </div>
          <div class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-[10px] px-1 py-0.5 text-center">
            {{ page.page_number }}
          </div>
        </div>
        <div
          class="border-2 border-dashed border-gray-600 rounded-lg aspect-video flex items-center justify-center cursor-pointer hover:border-green-500 transition"
          @click="handleAddPage"
        >
          <el-icon class="text-gray-500"><Plus /></el-icon>
        </div>
      </aside>

      <!-- 中间编辑区 -->
      <main class="flex-1 overflow-auto flex items-center justify-center p-8 bg-gray-900">
        <div v-if="currentPage" class="slide-canvas" :style="canvasStyle">
          <div
            v-if="currentPage.html_content"
            class="w-full h-full"
            v-html="currentPage.html_content"
            @click="handleCanvasClick"
          ></div>
          <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
            <div class="text-center">
              <el-icon size="48" class="mb-2"><Document /></el-icon>
              <p>第{{ currentPage.page_number }}页 - 等待生成</p>
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧对话面板 -->
      <aside class="w-80 bg-gray-800 border-l border-gray-700 flex flex-col">
        <!-- 标签切换 -->
        <div class="flex border-b border-gray-700">
          <button
            v-for="tab in ['对话', '检查器', '动画', '演讲稿']"
            :key="tab"
            class="flex-1 py-2 text-sm transition"
            :class="activeTab === tab ? 'text-green-400 border-b-2 border-green-400' : 'text-gray-400 hover:text-gray-200'"
            @click="activeTab = tab"
          >
            {{ tab }}
          </button>
        </div>

        <!-- 对话面板 -->
        <div v-if="activeTab === '对话'" class="flex-1 flex flex-col">
          <div class="flex-1 overflow-y-auto p-3 space-y-3">
            <div
              v-for="msg in sessionStore.currentMessages"
              :key="msg.id"
              class="rounded-lg p-3 text-sm"
              :class="msg.role === 'user' ? 'bg-green-900/50 text-green-100 ml-4' : 'bg-gray-700 text-gray-200 mr-4'"
            >
              <div class="text-xs text-gray-400 mb-1">{{ msg.role === 'user' ? '你' : 'AI' }}</div>
              <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            </div>
            <div v-if="aiThinking" class="bg-gray-700 rounded-lg p-3 text-sm text-gray-300">
              <el-icon class="animate-spin mr-1"><Loading /></el-icon>
              AI 正在思考...
            </div>
          </div>
          <div class="p-3 border-t border-gray-700">
            <el-input
              v-model="chatInput"
              type="textarea"
              :rows="3"
              placeholder="输入修改指令，例如：把标题颜色改成蓝色"
              @keydown.enter.exact.prevent="handleSendMessage"
            />
            <div class="flex justify-between items-center mt-2">
              <div class="flex space-x-1">
                <el-button size="small" @click="showImageUpload = !showImageUpload">📷 图片</el-button>
                <el-button size="small" @click="handleGenerateSpeech">🎤 演讲稿</el-button>
              </div>
              <el-button type="primary" size="small" @click="handleSendMessage" :loading="aiThinking">
                发送
              </el-button>
            </div>
          </div>
        </div>

        <!-- 检查器面板 -->
        <div v-if="activeTab === '检查器'" class="flex-1 overflow-y-auto p-3">
          <div class="text-gray-300 text-sm space-y-3">
            <div class="bg-gray-700 rounded-lg p-3">
              <h4 class="font-medium text-gray-200 mb-2">页面信息</h4>
              <p>标题: {{ currentPage?.title }}</p>
              <p>页码: {{ currentPage?.page_number }}</p>
              <p>状态: {{ currentPage?.status }}</p>
            </div>
            <div class="bg-gray-700 rounded-lg p-3">
              <h4 class="font-medium text-gray-200 mb-2">操作</h4>
              <div class="space-y-2">
                <el-button size="small" class="w-full" @click="handleDeletePage">删除此页</el-button>
                <el-button size="small" class="w-full" @click="handleDuplicatePage">复制此页</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 动画面板 -->
        <div v-if="activeTab === '动画'" class="flex-1 overflow-y-auto p-3">
          <div class="text-gray-300 text-sm">
            <div class="bg-gray-700 rounded-lg p-3 mb-3">
              <h4 class="font-medium text-gray-200 mb-2">页面切换动画</h4>
              <el-select v-model="pageTransition" class="w-full" size="small">
                <el-option label="无动画" value="none" />
                <el-option label="淡入淡出" value="fade" />
                <el-option label="滑动" value="slide" />
                <el-option label="推进" value="push" />
                <el-option label="缩放" value="zoom" />
                <el-option label="翻转" value="flip" />
              </el-select>
            </div>
            <div class="bg-gray-700 rounded-lg p-3">
              <h4 class="font-medium text-gray-200 mb-2">元素动画</h4>
              <p class="text-gray-400 text-xs mb-2">在画布上点击元素后设置动画</p>
              <div class="space-y-2">
                <el-select v-model="elementAnimation.effect" placeholder="动画效果" size="small" class="w-full">
                  <el-option label="淡入" value="fadeIn" />
                  <el-option label="上移入" value="fadeInUp" />
                  <el-option label="下移入" value="fadeInDown" />
                  <el-option label="左移入" value="fadeInLeft" />
                  <el-option label="右移入" value="fadeInRight" />
                  <el-option label="放大" value="zoomIn" />
                </el-select>
                <el-select v-model="elementAnimation.trigger" placeholder="触发方式" size="small" class="w-full">
                  <el-option label="自动播放" value="auto" />
                  <el-option label="点击触发" value="click" />
                  <el-option label="顺序播放" value="sequential" />
                </el-select>
                <el-button size="small" type="primary" class="w-full" @click="handleSetAnimation">应用动画</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 演讲稿面板 -->
        <div v-if="activeTab === '演讲稿'" class="flex-1 flex flex-col">
          <div class="p-3 border-b border-gray-700">
            <el-select v-model="speechStyle" size="small" class="w-full mb-2">
              <el-option label="正式演讲" value="formal" />
              <el-option label="轻松对话" value="casual" />
              <el-option label="叙事风格" value="narrative" />
            </el-select>
            <el-button type="primary" size="small" class="w-full" @click="handleGenerateSpeech" :loading="generatingSpeech">
              生成演讲稿
            </el-button>
          </div>
          <div class="flex-1 overflow-y-auto p-3 space-y-3">
            <div
              v-for="speech in speeches"
              :key="speech.id"
              class="bg-gray-700 rounded-lg p-3 text-sm text-gray-200"
            >
              <div class="text-xs text-gray-400 mb-1">{{ speech.style }}</div>
              <div class="whitespace-pre-wrap">{{ speech.content }}</div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- 导出对话框 -->
    <el-dialog v-model="showExportDialog" title="导出演示稿" width="400px">
      <div class="grid grid-cols-2 gap-3">
        <el-button @click="handleExport('pdf')" class="h-20">📄 PDF</el-button>
        <el-button @click="handleExport('png')" class="h-20">🖼️ PNG</el-button>
        <el-button @click="handleExport('pptx')" class="h-20">📊 PPTX</el-button>
        <el-button @click="handleExport('mp4')" class="h-20">🎬 MP4</el-button>
        <el-button @click="handleExport('html')" class="h-20">🌐 HTML打包</el-button>
      </div>
    </el-dialog>

    <!-- 历史版本对话框 -->
    <el-dialog v-model="showVersionDialog" title="历史版本" width="500px">
      <el-timeline>
        <el-timeline-item
          v-for="op in operations"
          :key="op.id"
          :timestamp="formatDate(op.created_at)"
          :type="op.type === 'generate' ? 'primary' : 'success'"
        >
          {{ op.type }} - {{ op.prompt || '无描述' }}
          <el-button size="small" link @click="handleRollback(op)">回退到此版本</el-button>
        </el-timeline-item>
      </el-timeline>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSessionStore } from '@/stores'
import { aiApi, editorApi, exportApi, speechApi, sessionApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const sessionStore = useSessionStore()

const sessionId = ref(route.params.id)
const currentPageId = ref(null)
const activeTab = ref('对话')
const chatInput = ref('')
const aiThinking = ref(false)
const canUndo = ref(true)
const canRedo = ref(false)
const showExportDialog = ref(false)
const showVersionDialog = ref(false)
const showImageUpload = ref(false)
const pageTransition = ref('fade')
const speechStyle = ref('formal')
const generatingSpeech = ref(false)
const speeches = ref([])
const operations = ref([])

const elementAnimation = ref({
  effect: 'fadeIn',
  trigger: 'auto',
  duration: 600,
})

const currentPage = computed(() => {
  return sessionStore.currentPages.find(p => p.id === currentPageId.value)
})

const canvasStyle = computed(() => {
  const session = sessionStore.currentSession
  if (!session) return {}
  const ratio = session.slide_height / session.slide_width
  const maxWidth = Math.min(window.innerWidth - 400, 900)
  const width = maxWidth
  const height = width * ratio
  return { width: `${width}px`, height: `${height}px` }
})

onMounted(async () => {
  await loadSession()
})

onUnmounted(() => {
  if (ws) ws.close()
})

let ws = null

async function loadSession() {
  await sessionStore.fetchSession(sessionId.value)
  await sessionStore.fetchPages(sessionId.value)
  await sessionStore.fetchMessages(sessionId.value)
  await fetchOperations()
  await fetchSpeeches()

  if (sessionStore.currentPages.length > 0) {
    currentPageId.value = sessionStore.currentPages[0].id
  }

  // 连接 WebSocket
  connectWebSocket()
}

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${sessionId.value}/`)
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'ai_response') {
      aiThinking.value = false
      sessionStore.fetchMessages(sessionId.value)
    }
  }
}

function selectPage(pageId) {
  currentPageId.value = pageId
}

function handleCanvasClick(e) {
  // 元素选择逻辑
}

async function handleSendMessage() {
  if (!chatInput.value.trim()) return
  aiThinking.value = true
  try {
    await aiApi.chatEdit({
      session_id: sessionId.value,
      message: chatInput.value,
      page_id: currentPageId.value,
    })
    chatInput.value = ''
  } catch (e) {
    ElMessage.error(e.message)
    aiThinking.value = false
  }
}

async function handleAddPage() {
  try {
    const result = await editorApi.addPage({
      session_id: sessionId.value,
      after_page_number: sessionStore.currentPages.length,
    })
    await sessionStore.fetchPages(sessionId.value)
    currentPageId.value = result.page_id
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDeletePage() {
  if (!currentPageId.value) return
  try {
    await editorApi.deletePage({ page_id: currentPageId.value })
    await sessionStore.fetchPages(sessionId.value)
    if (sessionStore.currentPages.length > 0) {
      currentPageId.value = sessionStore.currentPages[0].id
    }
    ElMessage.success('页面已删除')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDuplicatePage() {
  // 复制页面逻辑
}

async function handleSetAnimation() {
  if (!currentPageId.value) return
  try {
    await editorApi.setAnimation({
      page_id: currentPageId.value,
      selector: '.slide-element',
      animation: elementAnimation.value,
    })
    ElMessage.success('动画已设置')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleGenerateSpeech() {
  generatingSpeech.value = true
  try {
    await aiApi.generateSpeech({
      session_id: sessionId.value,
      page_id: currentPageId.value,
      style: speechStyle.value,
    })
    await fetchSpeeches()
    ElMessage.success('演讲稿生成完成')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    generatingSpeech.value = false
  }
}

async function fetchSpeeches() {
  speeches.value = await sessionApi.getSpeeches(sessionId.value)
}

async function fetchOperations() {
  operations.value = await sessionApi.getOperations(sessionId.value)
}

async function handleRollback(op) {
  try {
    await editorApi.rollback({
      session_id: sessionId.value,
      operation_id: op.id,
    })
    showVersionDialog.value = false
    await loadSession()
    ElMessage.success('已回退到该版本')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleUndo() {
  try {
    await editorApi.undo({ session_id: sessionId.value })
    await loadSession()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleRedo() {
  try {
    await editorApi.redo({ session_id: sessionId.value })
    await loadSession()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleExport(format) {
  try {
    showExportDialog.value = false
    const apiMap = { pdf: exportApi.pdf, png: exportApi.png, pptx: exportApi.pptx, mp4: exportApi.mp4, html: exportApi.html }
    await apiMap[format]({ session_id: sessionId.value })
    ElMessage.success(`正在导出${format.toUpperCase()}，请稍候...`)
  } catch (e) {
    ElMessage.error(e.message)
  }
}

function handlePreview() {
  router.push(`/session/${sessionId.value}/preview`)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}
</script>

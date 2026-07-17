<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
    <!-- 顶部导航 -->
    <nav class="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
              <span class="text-white font-bold text-lg">P</span>
            </div>
            <span class="text-xl font-bold text-gray-800">Oh My PPT</span>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/sessions" class="text-gray-600 hover:text-green-600 transition">我的演示稿</router-link>
            <router-link to="/templates" class="text-gray-600 hover:text-green-600 transition">模板库</router-link>
            <router-link to="/styles" class="text-gray-600 hover:text-green-600 transition">风格</router-link>
            <router-link to="/settings" class="text-gray-600 hover:text-green-600 transition">设置</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- 标题区 -->
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-gray-900 mb-4">
          AI 演示文稿生成器
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          输入主题，AI 自动规划大纲、配色、排版，直接生成精美的 HTML 演示稿
        </p>
      </div>

      <!-- 创建方式卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <router-link
          to="/session/create"
          class="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-green-200"
        >
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-green-200 transition">
            <el-icon size="24" class="text-green-600"><Edit /></el-icon>
          </div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">一句话创建</h3>
          <p class="text-sm text-gray-500">直接填写主题和需求，快速生成完整演示稿</p>
        </router-link>

        <div
          class="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-blue-200 cursor-pointer"
          @click="showChatCreate = true"
        >
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-200 transition">
            <el-icon size="24" class="text-blue-600"><ChatDotRound /></el-icon>
          </div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">对话创作</h3>
          <p class="text-sm text-gray-500">多轮对话梳理主题、资料、结构和每页重点</p>
        </div>

        <div
          class="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-purple-200 cursor-pointer"
          @click="showUploadDialog = true"
        >
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-purple-200 transition">
            <el-icon size="24" class="text-purple-600"><Upload /></el-icon>
          </div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">上传文档</h3>
          <p class="text-sm text-gray-500">上传 txt、md、csv、docx 文档自动整理生成</p>
        </div>

        <router-link
          to="/templates"
          class="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-orange-200"
        >
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-orange-200 transition">
            <el-icon size="24" class="text-orange-600"><Files /></el-icon>
          </div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">从模板创建</h3>
          <p class="text-sm text-gray-500">选择已保存的模板，沿用版式配色生成新内容</p>
        </router-link>
      </div>

      <!-- 快速创建 -->
      <div class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 mb-12">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">快速创建</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">主题</label>
            <el-input
              v-model="quickCreateForm.topic"
              placeholder="例如：人工智能在医疗领域的应用"
              size="large"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">详细描述</label>
            <el-input
              v-model="quickCreateForm.detail"
              placeholder="补充说明你的需求..."
              size="large"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">页数</label>
            <el-input-number v-model="quickCreateForm.page_count" :min="3" :max="30" size="large" class="w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">画布尺寸</label>
            <el-select v-model="quickCreateForm.slide_size" size="large" class="w-full">
              <el-option label="16:9 宽屏" value="wide-16-9" />
              <el-option label="4:3 标准" value="standard-4-3" />
              <el-option label="9:16 竖屏" value="vertical-9-16" />
              <el-option label="3:4 竖版" value="vertical-3-4" />
              <el-option label="1:1 方图" value="square-1-1" />
            </el-select>
          </div>
        </div>
        <div class="mt-6 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <el-select v-model="quickCreateForm.style_id" placeholder="选择风格（可选）" clearable class="w-56" filterable>
              <el-option-group v-for="group in groupedStyles" :key="group.category" :label="group.category">
                <el-option
                  v-for="style in group.styles"
                  :key="style.id"
                  :label="style.style_name"
                  :value="style.id"
                >
                  <span>{{ style.style_name }}</span>
                  <span class="text-xs text-gray-400 ml-2">{{ style.category }}</span>
                </el-option>
              </el-option-group>
            </el-select>
            <router-link to="/styles" class="text-sm text-green-600 hover:text-green-700">
              浏览全部风格 →
            </router-link>
          </div>
          <el-button
            type="primary"
            size="large"
            :loading="generating"
            @click="handleQuickCreate"
            class="bg-green-600 hover:bg-green-700 border-green-600"
          >
            <el-icon class="mr-1"><MagicStick /></el-icon>
            开始生成
          </el-button>
        </div>
      </div>

      <!-- 最近会话 -->
      <div v-if="sessionStore.sessions.length > 0">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-800">最近创建</h2>
          <router-link to="/sessions" class="text-green-600 hover:text-green-700 text-sm font-medium">
            查看全部 →
          </router-link>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div
            v-for="session in sessionStore.sortedSessions.slice(0, 6)"
            :key="session.id"
            class="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer"
            @click="$router.push(`/session/${session.id}`)"
          >
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs px-2 py-1 rounded-full" :class="statusClass(session.status)">
                {{ statusText(session.status) }}
              </span>
              <span class="text-xs text-gray-400">{{ formatDate(session.updated_at) }}</span>
            </div>
            <h3 class="font-semibold text-gray-800 mb-1 truncate">{{ session.title }}</h3>
            <p class="text-sm text-gray-500 truncate">{{ session.topic || '无描述' }}</p>
            <div class="mt-3 flex items-center text-xs text-gray-400 space-x-3">
              <span>{{ session.page_count_actual || 0 }} 页</span>
              <span>{{ session.slide_size }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 上传文档对话框 -->
    <el-dialog v-model="showUploadDialog" title="上传文档" width="500px">
      <el-upload
        drag
        :auto-upload="false"
        :on-change="handleDocumentSelect"
        accept=".txt,.md,.csv,.docx,.xlsx"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">拖拽文件到此处或 <em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip">支持 txt、md、csv、docx、xlsx 格式</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUploadDocument" :loading="uploading">解析并创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore, useStyleStore } from '@/stores'
import { aiApi, sessionApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const sessionStore = useSessionStore()
const styleStore = useStyleStore()

// 按分类分组的风格列表
const groupedStyles = computed(() => {
  const groups = {}
  for (const style of styleStore.styles) {
    const cat = style.category || '其他'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(style)
  }
  return Object.entries(groups)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([category, styles]) => ({ category, styles }))
})

const showUploadDialog = ref(false)
const showChatCreate = ref(false)
const generating = ref(false)
const uploading = ref(false)
const selectedFile = ref(null)

const quickCreateForm = reactive({
  topic: '',
  detail: '',
  page_count: 10,
  slide_size: 'wide-16-9',
  style_id: '',
})

onMounted(async () => {
  await Promise.all([
    sessionStore.fetchSessions(),
    styleStore.fetchStyles(),
  ])
})

async function handleQuickCreate() {
  if (!quickCreateForm.topic.trim()) {
    ElMessage.warning('请输入主题')
    return
  }
  generating.value = true
  try {
    const session = await sessionStore.createSession({
      title: quickCreateForm.topic,
      topic: quickCreateForm.topic,
      detail: quickCreateForm.detail,
      page_count: quickCreateForm.page_count,
      slide_size: quickCreateForm.slide_size,
      slide_width: slideWidth(quickCreateForm.slide_size),
      slide_height: slideHeight(quickCreateForm.slide_size),
      style: quickCreateForm.style_id || null,
    })

    // 触发AI生成
    await aiApi.generate({
      session_id: session.id,
      topic: quickCreateForm.topic,
      page_count: quickCreateForm.page_count,
      style_id: quickCreateForm.style_id || null,
      detail: quickCreateForm.detail,
    })

    router.push(`/session/${session.id}/generating`)
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    generating.value = false
  }
}

function handleDocumentSelect(file) {
  selectedFile.value = file.raw
}

async function handleUploadDocument() {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const result = await aiApi.uploadDocument(formData)
    ElMessage.success('文档解析成功')
    showUploadDialog.value = false

    // 创建会话并生成
    const session = await sessionStore.createSession({
      title: result.file_name.replace(/\.[^.]+$/, ''),
      topic: result.content.substring(0, 200),
      page_count: 10,
      slide_size: 'wide-16-9',
      slide_width: 1600,
      slide_height: 900,
    })

    await aiApi.generate({
      session_id: session.id,
      topic: result.content.substring(0, 500),
      page_count: 10,
      detail: result.content,
    })

    router.push(`/session/${session.id}/generating`)
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    uploading.value = false
  }
}

function slideWidth(size) {
  const map = { 'wide-16-9': 1600, 'standard-4-3': 1280, 'vertical-9-16': 900, 'vertical-3-4': 900, 'square-1-1': 1200 }
  return map[size] || 1600
}

function slideHeight(size) {
  const map = { 'wide-16-9': 900, 'standard-4-3': 960, 'vertical-9-16': 1600, 'vertical-3-4': 1200, 'square-1-1': 1200 }
  return map[size] || 900
}

function statusClass(status) {
  const map = {
    active: 'bg-green-100 text-green-700',
    completed: 'bg-blue-100 text-blue-700',
    failed: 'bg-red-100 text-red-700',
    archived: 'bg-gray-100 text-gray-700',
  }
  return map[status] || 'bg-gray-100 text-gray-700'
}

function statusText(status) {
  const map = { active: '进行中', completed: '已完成', failed: '失败', archived: '已归档' }
  return map[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return d.toLocaleDateString('zh-CN')
}
</script>

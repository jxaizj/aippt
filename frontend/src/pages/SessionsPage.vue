<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <router-link to="/" class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold">P</span>
              </div>
              <span class="text-lg font-bold text-gray-800">Oh My PPT</span>
            </router-link>
            <span class="text-gray-300">|</span>
            <h1 class="text-lg font-medium text-gray-700">我的演示稿</h1>
          </div>
          <router-link to="/session/create" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
            + 新建演示稿
          </router-link>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 筛选 -->
      <div class="flex items-center space-x-4 mb-6">
        <el-input
          v-model="searchQuery"
          placeholder="搜索演示稿..."
          clearable
          class="w-64"
          prefix-icon="Search"
        />
        <el-select v-model="filterStatus" placeholder="状态" clearable class="w-32">
          <el-option label="进行中" value="active" />
          <el-option label="已完成" value="completed" />
          <el-option label="失败" value="failed" />
        </el-select>
      </div>

      <!-- 会话列表 -->
      <div v-if="sessionStore.loading" class="flex justify-center py-20">
        <el-icon class="animate-spin text-3xl text-green-600"><Loading /></el-icon>
      </div>

      <div v-else-if="filteredSessions.length === 0" class="text-center py-20">
        <el-icon size="64" class="text-gray-300 mb-4"><Document /></el-icon>
        <p class="text-gray-500 mb-4">还没有演示稿</p>
        <router-link to="/" class="text-green-600 hover:text-green-700 font-medium">
          立即创建 →
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="session in filteredSessions"
          :key="session.id"
          class="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer group"
          @click="$router.push(`/session/${session.id}`)"
        >
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs px-2 py-1 rounded-full" :class="statusClass(session.status)">
              {{ statusText(session.status) }}
            </span>
            <el-dropdown @click.stop>
              <el-icon class="opacity-0 group-hover:opacity-100 transition cursor-pointer"><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleDuplicate(session)">复制</el-dropdown-item>
                  <el-dropdown-item @click="handleSaveAsTemplate(session)">保存为模板</el-dropdown-item>
                  <el-dropdown-item divided @click="handleDelete(session)" class="text-red-600">删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <h3 class="font-semibold text-gray-800 mb-1 truncate">{{ session.title }}</h3>
          <p class="text-sm text-gray-500 truncate mb-3">{{ session.topic || '无描述' }}</p>
          <div class="flex items-center text-xs text-gray-400 space-x-3">
            <span>{{ session.page_count_actual || 0 }} 页</span>
            <span>{{ session.slide_size }}</span>
            <span>{{ session.style_name || '默认风格' }}</span>
          </div>
          <div class="mt-3 text-xs text-gray-400">
            更新于 {{ formatDate(session.updated_at) }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSessionStore } from '@/stores'
import { sessionApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const sessionStore = useSessionStore()
const searchQuery = ref('')
const filterStatus = ref('')

onMounted(() => {
  sessionStore.fetchSessions()
})

const filteredSessions = computed(() => {
  let list = sessionStore.sortedSessions
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(s => s.title.toLowerCase().includes(q) || (s.topic || '').toLowerCase().includes(q))
  }
  if (filterStatus.value) {
    list = list.filter(s => s.status === filterStatus.value)
  }
  return list
})

async function handleDuplicate(session) {
  try {
    await sessionApi.duplicate(session.id)
    ElMessage.success('复制成功')
    sessionStore.fetchSessions()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleSaveAsTemplate(session) {
  try {
    await sessionApi.saveAsTemplate(session.id, { title: `${session.title} 模板` })
    ElMessage.success('已保存为模板')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDelete(session) {
  try {
    await ElMessageBox.confirm('确定要删除这个演示稿吗？', '提示', { type: 'warning' })
    await sessionStore.deleteSession(session.id)
    ElMessage.success('删除成功')
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message)
  }
}

function statusClass(status) {
  const map = { active: 'bg-green-100 text-green-700', completed: 'bg-blue-100 text-blue-700', failed: 'bg-red-100 text-red-700' }
  return map[status] || 'bg-gray-100 text-gray-700'
}

function statusText(status) {
  const map = { active: '进行中', completed: '已完成', failed: '失败' }
  return map[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN')
}
</script>

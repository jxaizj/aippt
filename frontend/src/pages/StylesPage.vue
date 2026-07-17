<template>
  <div class="min-h-screen bg-gray-50">
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
            <h1 class="text-lg font-medium text-gray-700">风格管理</h1>
          </div>
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-500">共 {{ totalCount }} 个风格</span>
            <el-radio-group v-model="sourceFilter" size="small">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button label="builtin">内置</el-radio-button>
              <el-radio-button label="ppt-master">PPT Master</el-radio-button>
            </el-radio-group>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 分类筛选 -->
      <div class="mb-6 flex items-center space-x-2 overflow-x-auto pb-2">
        <el-tag
          :type="activeCategory === '' ? 'primary' : 'info'"
          class="cursor-pointer"
          @click="activeCategory = ''"
        >
          全部
        </el-tag>
        <el-tag
          v-for="cat in categories"
          :key="cat"
          :type="activeCategory === cat ? 'primary' : 'info'"
          class="cursor-pointer whitespace-nowrap"
          @click="activeCategory = cat"
        >
          {{ cat }}
        </el-tag>
      </div>

      <!-- 风格网格 -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <div
          v-for="style in filteredStyles"
          :key="style.id"
          class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer group"
          @click="handleSelectStyle(style)"
        >
          <div class="aspect-video rounded-lg mb-3 flex items-center justify-center text-white text-2xl font-bold relative overflow-hidden"
            :style="{ background: getStyleGradient(style) }">
            <span class="relative z-10">{{ style.style_name?.[0] || 'S' }}</span>
            <div v-if="style.source === 'ppt-master'" class="absolute top-1 right-1 bg-white/30 rounded px-1 text-[8px] text-white">
              PPT-M
            </div>
          </div>
          <h3 class="font-medium text-gray-800 text-sm mb-1 truncate">{{ style.style_name }}</h3>
          <p class="text-xs text-gray-500 truncate h-4">{{ style.description || '无描述' }}</p>
          <div class="flex items-center justify-between mt-2">
            <span class="text-xs px-1.5 py-0.5 rounded bg-gray-100 text-gray-500">{{ style.category || '未分类' }}</span>
            <el-icon
              class="cursor-pointer transition"
              :class="style.favorite_at ? 'text-yellow-500' : 'text-gray-300 group-hover:text-gray-400'"
              @click.stop="styleStore.toggleFavorite(style.id)"
            ><Star /></el-icon>
          </div>
        </div>
      </div>

      <div v-if="filteredStyles.length === 0" class="text-center py-20">
        <el-icon size="48" class="text-gray-300 mb-3"><Brush /></el-icon>
        <p class="text-gray-500">该分类下暂无风格</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStyleStore } from '@/stores'

const router = useRouter()
const styleStore = useStyleStore()
const activeCategory = ref('')
const sourceFilter = ref('')

const totalCount = computed(() => styleStore.styles.length)

const categories = computed(() => {
  let styles = styleStore.styles
  if (sourceFilter.value) {
    styles = styles.filter(s => s.source === sourceFilter.value)
  }
  return [...new Set(styles.map(s => s.category).filter(Boolean))].sort()
})

const filteredStyles = computed(() => {
  let result = styleStore.styles.filter(s => s && s.id)
  if (sourceFilter.value) {
    result = result.filter(s => s.source === sourceFilter.value)
  }
  if (activeCategory.value) {
    result = result.filter(s => s.category === activeCategory.value)
  }
  return result
})

onMounted(() => {
  if (!styleStore.styles.length) styleStore.fetchStyles()
})

function getStyleGradient(style) {
  const gradients = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
    'linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)',
    'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
    'linear-gradient(135deg, #f5576c 0%, #ff6a88 100%)',
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
    'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
  ]
  const idx = style.id ? style.id.charCodeAt(0) % gradients.length : 0
  return gradients[idx]
}

function handleSelectStyle(style) {
  // 跳转到创建页面并预选该风格
  router.push({ path: '/session/create', query: { style_id: style.id } })
}
</script>

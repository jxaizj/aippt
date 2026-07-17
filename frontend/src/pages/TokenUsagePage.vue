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
            <h1 class="text-lg font-medium text-gray-700">Token 用量统计</h1>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-sm text-gray-500 mb-1">总输入 Token</h3>
          <p class="text-3xl font-bold text-blue-600">{{ totalInputTokens.toLocaleString() }}</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-sm text-gray-500 mb-1">总输出 Token</h3>
          <p class="text-3xl font-bold text-green-600">{{ totalOutputTokens.toLocaleString() }}</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-sm text-gray-500 mb-1">总 Token</h3>
          <p class="text-3xl font-bold text-purple-600">{{ totalTokens.toLocaleString() }}</p>
        </div>
      </div>

      <!-- 使用记录 -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-bold text-gray-800">使用记录</h2>
        </div>
        <el-table :data="usageRecords" border>
          <el-table-column prop="created_at" label="时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="provider" label="提供商" width="120" />
          <el-table-column prop="model" label="模型" width="150" />
          <el-table-column prop="input_tokens" label="输入Token" width="120" />
          <el-table-column prop="output_tokens" label="输出Token" width="120" />
          <el-table-column prop="total_tokens" label="总Token" width="120" />
        </el-table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { settingsApi } from '@/api'

const usageRecords = ref([])

const totalInputTokens = computed(() => usageRecords.value.reduce((sum, r) => sum + (r.input_tokens || 0), 0))
const totalOutputTokens = computed(() => usageRecords.value.reduce((sum, r) => sum + (r.output_tokens || 0), 0))
const totalTokens = computed(() => usageRecords.value.reduce((sum, r) => sum + (r.total_tokens || 0), 0))

onMounted(async () => {
  usageRecords.value = await settingsApi.getModelUsage()
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}
</script>

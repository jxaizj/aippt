<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="text-center">
      <el-icon size="64" class="text-green-500 animate-spin mb-4"><Loading /></el-icon>
      <h2 class="text-xl font-bold text-gray-800 mb-2">模板生成中...</h2>
      <p class="text-gray-500">使用模板创建演示稿</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // Redirect to home after brief display
  setTimeout(() => router.push('/'), 2000)
})
</script>

<template>
  <div class="min-h-screen bg-black flex items-center justify-center" @keydown="handleKeydown">
    <div v-if="currentPage" class="w-full h-full flex items-center justify-center">
      <div class="slide-preview" :style="previewStyle">
        <div v-if="currentPage.html_content" class="w-full h-full" v-html="currentPage.html_content"></div>
      </div>
    </div>

    <!-- 控制栏 -->
    <div class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-black/70 backdrop-blur rounded-full px-6 py-3 flex items-center space-x-4">
      <el-icon class="text-white cursor-pointer hover:text-green-400 transition" @click="prevPage"><ArrowLeft /></el-icon>
      <span class="text-white text-sm">{{ currentPageIndex + 1 }} / {{ pages.length }}</span>
      <el-icon class="text-white cursor-pointer hover:text-green-400 transition" @click="nextPage"><ArrowRight /></el-icon>
      <span class="text-gray-400 text-xs mx-2">|</span>
      <el-icon class="text-white cursor-pointer hover:text-green-400 transition" @click="toggleFullscreen"><FullScreen /></el-icon>
      <el-icon class="text-white cursor-pointer hover:text-red-400 transition" @click="exitPreview"><Close /></el-icon>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSessionStore } from '@/stores'

const route = useRoute()
const router = useRouter()
const sessionStore = useSessionStore()

const sessionId = ref(route.params.id)
const currentPageIndex = ref(0)

const pages = computed(() => sessionStore.currentPages)
const currentPage = computed(() => pages.value[currentPageIndex.value])

const previewStyle = computed(() => {
  const session = sessionStore.currentSession
  if (!session) return {}
  const ratio = session.slide_height / session.slide_width
  const vw = window.innerWidth
  const vh = window.innerHeight
  const windowRatio = vw / vh

  let width, height
  if (ratio > windowRatio) {
    height = vh * 0.9
    width = height / ratio
  } else {
    width = vw * 0.9
    height = width * ratio
  }
  return { width: `${width}px`, height: `${height}px` }
})

onMounted(async () => {
  await sessionStore.fetchSession(sessionId.value)
  await sessionStore.fetchPages(sessionId.value)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

function handleKeydown(e) {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
    nextPage()
  } else if (e.key === 'ArrowLeft') {
    prevPage()
  } else if (e.key === 'Escape') {
    exitPreview()
  }
}

function nextPage() {
  if (currentPageIndex.value < pages.value.length - 1) {
    currentPageIndex.value++
  }
}

function prevPage() {
  if (currentPageIndex.value > 0) {
    currentPageIndex.value--
  }
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

function exitPreview() {
  router.push(`/session/${sessionId.value}`)
}
</script>

<style scoped>
.slide-preview {
  background: white;
  box-shadow: 0 0 60px rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}
</style>

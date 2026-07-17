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
            <h1 class="text-lg font-medium text-gray-700">模板库</h1>
          </div>
          <el-button type="primary" @click="showCreateDialog = true">+ 创建模板</el-button>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="template in templates"
          :key="template.id"
          class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition group"
        >
          <div class="aspect-video bg-gradient-to-br from-green-100 to-emerald-100 flex items-center justify-center">
            <el-icon size="48" class="text-green-400"><Document /></el-icon>
          </div>
          <div class="p-4">
            <h3 class="font-semibold text-gray-800 mb-1">{{ template.title }}</h3>
            <p class="text-sm text-gray-500 mb-3 line-clamp-2">{{ template.description || '无描述' }}</p>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-400">{{ template.slide_size }}</span>
              <el-button size="small" type="primary" @click="handleUseTemplate(template)">
                使用模板
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="templates.length === 0" class="text-center py-20">
        <el-icon size="64" class="text-gray-300 mb-4"><Files /></el-icon>
        <p class="text-gray-500">还没有模板，可以从已有演示稿保存为模板</p>
      </div>
    </main>

    <!-- 使用模板对话框 -->
    <el-dialog v-model="showUseDialog" title="从模板创建" width="500px">
      <el-form label-position="top">
        <el-form-item label="标题">
          <el-input v-model="useForm.title" placeholder="新演示稿标题" />
        </el-form-item>
        <el-form-item label="主题">
          <el-input v-model="useForm.topic" type="textarea" :rows="3" placeholder="演示主题" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUseDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreateFromTemplate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { templateApi, aiApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const templates = ref([])
const showCreateDialog = ref(false)
const showUseDialog = ref(false)
const selectedTemplate = ref(null)

const useForm = ref({ title: '', topic: '' })

onMounted(async () => {
  templates.value = await templateApi.list()
})

async function handleUseTemplate(template) {
  selectedTemplate.value = template
  useForm.value = { title: template.title, topic: '' }
  showUseDialog.value = true
}

async function handleCreateFromTemplate() {
  if (!useForm.value.title.trim()) {
    ElMessage.warning('请输入标题')
    return
  }
  try {
    const session = await templateApi.createSession(selectedTemplate.value.id, useForm.value)
    await aiApi.generate({
      session_id: session.id,
      topic: useForm.value.topic || useForm.value.title,
      page_count: 10,
    })
    showUseDialog.value = false
    router.push(`/session/${session.id}/generating`)
  } catch (e) {
    ElMessage.error(e.message)
  }
}
</script>

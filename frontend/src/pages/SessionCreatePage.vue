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
            <h1 class="text-lg font-medium text-gray-700">创建演示稿</h1>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">创建新的演示稿</h2>

        <el-form :model="form" label-position="top" size="large">
          <el-form-item label="标题" required>
            <el-input v-model="form.title" placeholder="给你的演示稿起个名字" />
          </el-form-item>

          <el-form-item label="主题" required>
            <el-input
              v-model="form.topic"
              type="textarea"
              :rows="3"
              placeholder="描述你的演示主题，例如：人工智能在医疗领域的应用与发展趋势"
            />
          </el-form-item>

          <el-form-item label="详细描述">
            <el-input
              v-model="form.detail"
              type="textarea"
              :rows="4"
              placeholder="补充说明受众、重点内容、风格偏好等..."
            />
          </el-form-item>

          <div class="grid grid-cols-2 gap-4">
            <el-form-item label="页数">
              <el-input-number v-model="form.page_count" :min="3" :max="30" class="w-full" />
            </el-form-item>
            <el-form-item label="画布尺寸">
              <el-select v-model="form.slide_size" class="w-full">
                <el-option label="16:9 宽屏 (1600×900)" value="wide-16-9" />
                <el-option label="4:3 标准 (1280×960)" value="standard-4-3" />
                <el-option label="9:16 竖屏 (900×1600)" value="vertical-9-16" />
                <el-option label="3:4 竖版 (900×1200)" value="vertical-3-4" />
                <el-option label="1:1 方图 (1200×1200)" value="square-1-1" />
              </el-select>
            </el-form-item>
          </div>

          <el-form-item label="风格">
            <el-select v-model="form.style_id" placeholder="选择风格（可选）" clearable class="w-full">
              <el-option
                v-for="style in styleStore.styles"
                :key="style.id"
                :label="style.style_name"
                :value="style.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="AI模型">
            <el-select v-model="form.model_config_id" placeholder="选择模型配置" class="w-full">
              <el-option
                v-for="config in modelConfigStore.configs"
                :key="config.id"
                :label="`${config.name} (${config.provider}/${config.model})`"
                :value="config.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="参考文档">
            <el-upload
              :auto-upload="false"
              :on-change="handleFileSelect"
              accept=".txt,.md,.csv,.docx,.xlsx"
              :limit="1"
            >
              <el-button>选择文件</el-button>
              <template #tip>
                <div class="text-xs text-gray-400">上传文档作为生成参考（可选）</div>
              </template>
            </el-upload>
          </el-form-item>

          <div class="flex justify-end space-x-4 mt-8">
            <router-link to="/">
              <el-button size="large">取消</el-button>
            </router-link>
            <el-button
              type="primary"
              size="large"
              :loading="generating"
              @click="handleCreate"
              class="bg-green-600 hover:bg-green-700 border-green-600"
            >
              开始生成
            </el-button>
          </div>
        </el-form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore, useStyleStore, useModelConfigStore } from '@/stores'
import { aiApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const sessionStore = useSessionStore()
const styleStore = useStyleStore()
const modelConfigStore = useModelConfigStore()

const generating = ref(false)
const selectedFile = ref(null)

const form = reactive({
  title: '',
  topic: '',
  detail: '',
  page_count: 10,
  slide_size: 'wide-16-9',
  style_id: '',
  model_config_id: '',
})

onMounted(async () => {
  await Promise.all([
    styleStore.fetchStyles(),
    modelConfigStore.fetchConfigs(),
  ])
  // 默认选中当前激活的模型配置
  if (!form.model_config_id && modelConfigStore.activeConfig) {
    form.model_config_id = modelConfigStore.activeConfig.id
  }
})

function handleFileSelect(file) {
  selectedFile.value = file.raw
}

function getSlideDimensions(size) {
  const map = {
    'wide-16-9': [1600, 900],
    'standard-4-3': [1280, 960],
    'vertical-9-16': [900, 1600],
    'vertical-3-4': [900, 1200],
    'square-1-1': [1200, 1200],
  }
  return map[size] || [1600, 900]
}

async function handleCreate() {
  if (!form.title.trim() || !form.topic.trim()) {
    ElMessage.warning('请填写标题和主题')
    return
  }
  generating.value = true
  try {
    const [width, height] = getSlideDimensions(form.slide_size)
    const session = await sessionStore.createSession({
      title: form.title,
      topic: form.topic,
      detail: form.detail,
      page_count: form.page_count,
      slide_size: form.slide_size,
      slide_width: width,
      slide_height: height,
      style: form.style_id || null,
    })

    // 上传参考文档（如果有）
    let documentContent = form.detail
    if (selectedFile.value) {
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      const docResult = await aiApi.uploadDocument(formData)
      documentContent += '\n\n' + docResult.content
    }

    await aiApi.generate({
      session_id: session.id,
      topic: form.topic,
      page_count: form.page_count,
      style_id: form.style_id || null,
      detail: documentContent,
      model_config_id: form.model_config_id || null,
    })

    router.push(`/session/${session.id}/generating`)
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    generating.value = false
  }
}
</script>

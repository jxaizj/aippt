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
            <h1 class="text-lg font-medium text-gray-700">设置</h1>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- AI模型配置 -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-gray-800">AI 模型配置</h2>
          <el-button type="primary" @click="showAddModelDialog = true">+ 添加配置</el-button>
        </div>

        <div class="space-y-3">
          <div
            v-for="config in modelConfigStore.configs"
            :key="config.id"
            class="flex items-center justify-between p-4 rounded-xl border transition"
            :class="config.active ? 'border-green-300 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
          >
            <div class="flex items-center space-x-4">
              <div
                class="w-3 h-3 rounded-full"
                :class="config.active ? 'bg-green-500' : 'bg-gray-300'"
              ></div>
              <div>
                <h3 class="font-medium text-gray-800">{{ config.name }}</h3>
                <p class="text-sm text-gray-500">{{ config.provider }} / {{ config.model }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <el-button
                v-if="!config.active"
                size="small"
                @click="handleSetActive(config.id)"
              >
                启用
              </el-button>
              <el-button size="small" @click="handleEditConfig(config)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeleteConfig(config.id)">删除</el-button>
            </div>
          </div>
          <div v-if="modelConfigStore.configs.length === 0" class="text-center py-8 text-gray-400">
            还没有配置AI模型，请先添加配置
          </div>
        </div>
      </div>

      <!-- 应用设置 -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-xl font-bold text-gray-800 mb-6">应用设置</h2>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium text-gray-700">语言</h3>
              <p class="text-sm text-gray-500">界面语言</p>
            </div>
            <el-select v-model="settings.locale" class="w-40">
              <el-option label="简体中文" value="zh-CN" />
              <el-option label="English" value="en" />
            </el-select>
          </div>
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium text-gray-700">自动保存</h3>
              <p class="text-sm text-gray-500">编辑时自动保存更改</p>
            </div>
            <el-switch v-model="settings.autoSave" />
          </div>
        </div>
      </div>
    </main>

    <!-- 添加模型配置对话框 -->
    <el-dialog v-model="showAddModelDialog" :title="editingConfig ? '编辑配置' : '添加模型配置'" width="500px">
      <el-form :model="modelForm" label-position="top">
        <el-form-item label="配置名称">
          <el-input v-model="modelForm.name" placeholder="例如：DeepSeek" />
        </el-form-item>
        <el-form-item label="提供商">
          <el-select v-model="modelForm.provider" class="w-full">
            <el-option label="OpenAI" value="openai" />
            <el-option label="DeepSeek" value="deepseek" />
            <el-option label="Anthropic" value="anthropic" />
            <el-option label="Google" value="google" />
            <el-option label="Ollama" value="ollama" />
            <el-option label="其他" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型名称">
          <el-input v-model="modelForm.model" placeholder="例如：gpt-4, deepseek-chat" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="modelForm.api_key" type="password" show-password placeholder="sk-..." />
        </el-form-item>
        <el-form-item label="Base URL">
          <el-input v-model="modelForm.base_url" placeholder="https://api.openai.com/v1" />
        </el-form-item>
        <el-form-item label="最大Token数">
          <el-input-number v-model="modelForm.max_tokens" :min="1000" :max="128000" class="w-full" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddModelDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveConfig">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useModelConfigStore } from '@/stores'
import { ElMessage } from 'element-plus'

const modelConfigStore = useModelConfigStore()

const showAddModelDialog = ref(false)
const editingConfig = ref(null)

const settings = reactive({
  locale: 'zh-CN',
  autoSave: true,
})

const modelForm = reactive({
  name: '',
  provider: 'openai',
  model: '',
  api_key: '',
  base_url: '',
  max_tokens: 4096,
})

onMounted(async () => {
  await modelConfigStore.fetchConfigs()
})

async function handleSetActive(id) {
  await modelConfigStore.setActive(id)
  ElMessage.success('已切换激活配置')
}

function handleEditConfig(config) {
  editingConfig.value = config
  Object.assign(modelForm, config)
  showAddModelDialog.value = true
}

async function handleSaveConfig() {
  try {
    if (editingConfig.value) {
      await modelConfigStore.updateConfig(editingConfig.value.id, modelForm)
    } else {
      await modelConfigStore.createConfig(modelForm)
    }
    showAddModelDialog.value = false
    editingConfig.value = null
    resetModelForm()
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDeleteConfig(id) {
  await modelConfigStore.deleteConfig(id)
  ElMessage.success('删除成功')
}

function resetModelForm() {
  Object.assign(modelForm, {
    name: '', provider: 'openai', model: '', api_key: '', base_url: '', max_tokens: 4096
  })
}
</script>

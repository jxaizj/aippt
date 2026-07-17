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
            <h1 class="text-lg font-medium text-gray-700">字体管理</h1>
          </div>
          <el-button type="primary" @click="showAddDialog = true">+ 添加字体</el-button>
        </div>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="text-left px-6 py-3 text-sm font-medium text-gray-600">字体名称</th>
              <th class="text-left px-6 py-3 text-sm font-medium text-gray-600">分类</th>
              <th class="text-left px-6 py-3 text-sm font-medium text-gray-600">用途</th>
              <th class="text-left px-6 py-3 text-sm font-medium text-gray-600">语言</th>
              <th class="text-left px-6 py-3 text-sm font-medium text-gray-600">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="font in fonts" :key="font.id" class="border-b border-gray-50 hover:bg-gray-50">
              <td class="px-6 py-4">
                <span class="font-medium text-gray-800">{{ font.display_name }}</span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ font.category }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ font.usage }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ font.language }}</td>
              <td class="px-6 py-4">
                <el-button size="small" type="danger" @click="handleDelete(font.id)" :disabled="font.is_system">删除</el-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <el-dialog v-model="showAddDialog" title="添加字体" width="500px">
      <el-form label-position="top">
        <el-form-item label="字体文件">
          <el-upload
            :auto-upload="false"
            :on-change="handleFontSelect"
            accept=".woff2,.ttf,.otf"
            :limit="1"
          >
            <el-button>选择字体文件</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="显示名称">
          <el-input v-model="fontForm.display_name" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="fontForm.category" class="w-full">
            <el-option label="无衬线" value="sans-serif" />
            <el-option label="衬线" value="serif" />
            <el-option label="手写" value="handwriting" />
            <el-option label="等宽" value="monospace" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUploadFont">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { fontApi } from '@/api'
import { ElMessage } from 'element-plus'

const fonts = ref([])
const showAddDialog = ref(false)
const selectedFontFile = ref(null)

const fontForm = reactive({
  display_name: '',
  category: 'sans-serif',
})

onMounted(async () => {
  fonts.value = await fontApi.list()
})

function handleFontSelect(file) {
  selectedFontFile.value = file.raw
  if (!fontForm.display_name) {
    fontForm.display_name = file.name.replace(/\.[^.]+$/, '')
  }
}

async function handleUploadFont() {
  if (!selectedFontFile.value) {
    ElMessage.warning('请选择字体文件')
    return
  }
  try {
    const formData = new FormData()
    formData.append('file', selectedFontFile.value)
    formData.append('display_name', fontForm.display_name)
    formData.append('category', fontForm.category)
    await fontApi.create(formData)
    showAddDialog.value = false
    ElMessage.success('字体添加成功')
    fonts.value = await fontApi.list()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDelete(id) {
  await fontApi.delete(id)
  fonts.value = fonts.value.filter(f => f.id !== id)
  ElMessage.success('删除成功')
}
</script>

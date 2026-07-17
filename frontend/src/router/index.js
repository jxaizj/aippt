import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/HomePage.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/sessions',
    name: 'Sessions',
    component: () => import('@/pages/SessionsPage.vue'),
    meta: { title: '会话列表' }
  },
  {
    path: '/session/create',
    name: 'SessionCreate',
    component: () => import('@/pages/SessionCreatePage.vue'),
    meta: { title: '创建演示稿' }
  },
  {
    path: '/session/:id',
    name: 'SessionDetail',
    component: () => import('@/pages/SessionDetailPage.vue'),
    meta: { title: '演示稿详情' }
  },
  {
    path: '/session/:id/generating',
    name: 'SessionGenerating',
    component: () => import('@/pages/SessionGeneratingPage.vue'),
    meta: { title: '生成中' }
  },
  {
    path: '/session/:id/preview',
    name: 'SessionPreview',
    component: () => import('@/pages/SessionPreviewPage.vue'),
    meta: { title: '预览演示' }
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('@/pages/TemplatesPage.vue'),
    meta: { title: '模板库' }
  },
  {
    path: '/styles',
    name: 'Styles',
    component: () => import('@/pages/StylesPage.vue'),
    meta: { title: '风格管理' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/pages/SettingsPage.vue'),
    meta: { title: '设置' }
  },
  {
    path: '/fonts',
    name: 'Fonts',
    component: () => import('@/pages/FontsPage.vue'),
    meta: { title: '字体管理' }
  },
  {
    path: '/token-usage',
    name: 'TokenUsage',
    component: () => import('@/pages/TokenUsagePage.vue'),
    meta: { title: 'Token用量' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || ''} - Oh My PPT`
  next()
})

export default router

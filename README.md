# PPTAI — AI 驱动的 PPT 生成与编辑平台

> 基于 [Oh My PPT](https://github.com/arcsin1/oh-my-ppt) 的设计理念，使用 **Django + Vue3** 全栈重写的现代化 PPT AI 工具。  
> **Describe what you need — and let AI build clean, beautiful slides for you. Local-first. Self-hosted. Yours.**

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](./LICENSE)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js)](https://vuejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)

## ✨ 灵感来源

本项目深受 [Oh My PPT](https://github.com/arcsin1/oh-my-ppt) 的启发。Oh My PPT 的核心理念是：

- **一句话生成 PPT** — 把"我想做一个关于 XX 的演讲"交给 AI，几秒内获得完整幻灯片
- **本地优先** — 所有数据保存在你控制的服务器上，不依赖任何第三方云端
- **Web 优先** — 用 HTML/CSS 构建 PPT，不绑定 PowerPoint，跨平台即用即看
- **离线可用** — 自部署后完全可脱离外网运行

我们在继承这些理念的基础上，做了全面的架构升级：从 Electron + Electron Store 的桌面架构，重构为 **Django REST API + Vue3 SPA** 的 Web 全栈架构，让部署更灵活、扩展更容易。

## 🚀 核心特性

### 生成
- 💬 **一句话生成** — 输入主题，AI 自动生成完整 PPT 大纲和页面内容
- 🔀 **多任务并行** — 同时发起多个生成任务，互不干扰
- 📄 **文档转 PPT** — 上传 txt / md / csv / docx，AI 自动转换为演示文稿
- 🧱 **模板复用** — 保存/导出模板，下次一键套用
- 🎨 **图片风格识别** — 上传参考图，AI 识别设计风格并据此生成
- 🔤 **70+ 风格内置** — 多种预设风格，支持自定义添加

### 编辑
- ✏️ **对话式修改** — 用自然语言告诉 AI 你想改哪里
- 🖱️ **可视化拖拽编辑** — 鼠标拖拽调整元素位置大小
- ↩️ **撤销/重做** — 操作历史完整可回退
- 🧮 **LaTeX 公式** — 数学公式实时渲染
- 📊 **图表嵌入** — 基于 Chart.js 内嵌图表

### 预览 & 导出
- 🖥️ **全屏演示模式** — 键盘切换，ESC 退出
- 📝 **演讲稿生成** — AI 为整套或单页生成演讲备注
- 📄 **多格式导出** — PDF / PNG / PNG长图 / PPTX / MP4 / HTML
- 📦 **HTML 一键打包** — 生成自包含 HTML，离线即用

### 平台
- 🔒 **完全本地部署** — 所有数据在你的服务器上
- 🌐 **多 AI 模型支持** — OpenAI / DeepSeek / Kimi / 通义千问 / Ollama / 任意 OpenAI 兼容 API
- 🔄 **历史版本回退** — 任意时刻可回退到之前的版本
- 💾 **导入导出** — 跨设备迁移和协作
- 📖 **实时 WebSocket 推送** — 生成进度、对话消息实时更新

## 🛠 技术栈

### 后端
| 组件 | 技术 | 说明 |
|------|------|------|
| Web 框架 | **Django 5.2** | 稳定、成熟的 Web 框架 |
| REST API | **Django REST Framework** | 标准化 REST 接口 |
| 实时通信 | **Django Channels** | WebSocket 支持 |
| 数据库 | **SQLite / PostgreSQL** | 默认 SQLite，可一键切换 PG |
| AI 集成 | **OpenAI Python SDK** | 兼容 OpenAI / DeepSeek / Kimi / Ollama |

### 前端
| 组件 | 技术 | 说明 |
|------|------|------|
| 框架 | **Vue 3** | 渐进式前端框架 |
| 状态管理 | **Pinia** | 轻量级状态管理 |
| 路由 | **Vue Router** | SPA 路由 |
| UI 组件 | **Element Plus** | 成熟的组件库 |
| 样式 | **Tailwind CSS** | 原子化 CSS |
| 构建 | **Vite** | 极速构建工具 |
| HTTP | **Axios** | HTTP 客户端 |
| 图表 | **Chart.js** | 图表可视化 |

## 📁 项目结构

```
pptai/
├── backend/                    # Django 后端
│   ├── config/                 # 项目配置（settings / urls / asgi）
│   ├── sessions/               # 会话应用 — 核心数据模型与 API
│   ├── ai_engine/              # AI 引擎 — 生成/编辑/对话/ WebSocket
│   ├── editor/                 # 编辑器 — 页面编辑操作与动画
│   ├── export_app/             # 导出 — 多格式导出任务
│   ├── settings_app/           # 设置 — 应用配置与用量统计
│   ├── templates_app/          # 模板管理
│   ├── generation/             # 生成任务管理
│   ├── requirements.txt
│   └── manage.py
└── frontend/                   # Vue3 前端
    ├── src/
    │   ├── api/                # API 服务层
    │   ├── components/         # 公共组件
    │   ├── pages/              # 页面视图（11+ 页面）
    │   ├── router/             # 路由配置
    │   ├── stores/             # Pinia 状态管理
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## ⚡ 快速开始

### 前置要求
- Python 3.10+
- Node.js 18+

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:3000`，后端运行在 `http://localhost:8000`。

### 配置 AI 模型

首次使用时进入「设置」页面添加 AI 模型配置，支持：

- OpenAI 官方 (gpt-4o / gpt-4o-mini)
- DeepSeek (deepseek-chat / deepseek-reasoner)
- Kimi (Moonshot)
- 通义千问 (Qwen)
- Ollama (本地大模型)
- 任何 OpenAI 兼容 API

## 🌐 API 端点

| 模块 | 路径 | 说明 |
|------|------|------|
| 会话 | `/api/sessions/` | 会话 CRUD |
| 消息 | `/api/sessions/messages/` | 对话消息 |
| 页面 | `/api/sessions/pages/` | 页面管理 |
| 风格 | `/api/sessions/styles/` | 风格管理 |
| 模板 | `/api/sessions/templates/` | 模板管理 |
| 模型配置 | `/api/sessions/model-configs/` | AI 模型配置 |
| AI 引擎 | `/api/ai/` | AI 生成 / 编辑 / 演讲稿 |
| 编辑器 | `/api/editor/` | 页面编辑操作 |
| 导出 | `/api/export/` | 多格式导出 |
| 设置 | `/api/settings/` | 应用设置 |

### WebSocket

| 路径 | 说明 |
|------|------|
| `/ws/generation/{session_id}/` | 生成进度实时推送 |
| `/ws/chat/{session_id}/` | 对话消息实时推送 |
| `/ws/notifications/` | 全局通知 |

## 🗄 数据库配置

默认使用 SQLite，如需切换 PostgreSQL：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pptai',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🆚 Oh My PPT 与 PPTAI 对比

| 维度 | Oh My PPT | PPTAI |
|------|-----------|-------|
| 架构 | Electron 桌面应用 | Django + Vue3 Web 应用 |
| 部署方式 | 本地安装包 | 自托管 Web 服务 |
| 访问方式 | 桌面程序 | 浏览器（随时随地） |
| 数据库 | Electron Store | SQLite / PostgreSQL |
| 扩展性 | 单用户本地 | 多用户、可集群 |
| AI 集成 | 内置 SDK | 统一 OpenAI SDK，模型更灵活 |
| 实时通信 | 本地事件 | WebSocket (Channels) |
| 许可证 | Apache-2.0 | Apache-2.0 |

## 📸 截图

> （待添加项目截图）

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！如果你有新的功能想法或发现了 bug，请在仓库中提交 Issue。

## 🙏 致谢

本项目基于 [Oh My PPT](https://github.com/arcsin1/oh-my-ppt) 的理念和思路构建。特别感谢 arcsin1 的原创工作和持续维护，让"用 AI 做 PPT"这个想法成为现实。

Oh My PPT 的核心参考项目：
- [pptx2json](https://github.com/arcsin1/pptx2json) — PPTX 导入能力底层基础包
- [style-generate-skill](https://github.com/arcsin1/style-generate-skill) — 风格生成 Skill

## 📄 许可证

[Apache License 2.0](./LICENSE)

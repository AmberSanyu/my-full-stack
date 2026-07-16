## 目录结构
.
├── backend/                  # 后端项目 (FastAPI + SQLModel)
│   ├── app/                  # 主应用目录
│   │   ├── alembic/          # 数据库迁移配置 (生成的迁移脚本在 versions/ 下)
│   │   ├── api/              # API 路由
│   │   │   ├── routes/       # 具体的业务接口实现 (login, users, items 等)
│   │   │   └── main.py       # 路由总入口 (汇总所有业务路由)
│   │   ├── core/             # 核心基础配置
│   │   │   ├── config.py     # 环境变量读取与全局配置声明
│   │   │   ├── db.py         # 数据库 Session 与 Engine 初始化
│   │   │   └── security.py   # JWT 认证逻辑与密码加密工具
│   │   ├── email-templates/  # 业务邮件模板 (MJML/HTML 格式)
│   │   ├── crud.py           # 核心逻辑：封装数据库增删改查操作
│   │   ├── models.py         # 数据库模型：定义表结构 (SQLModel)
│   │   ├── utils.py          # 通用工具函数 (如发送邮件)
│   │   ├── main.py           # FastAPI 实例创建与全局中间件配置
│   │   ├── initial_data.py   # 脚本：系统首次启动时插入初始管理员数据
│   │   └── backend_pre_start.py # 脚本：等待并确认数据库连接可用
│   ├── scripts/              # 辅助开发脚本 (lint, format, test, prestart)
│   ├── tests/                # 自动化测试目录 (包含 api、crud 等测试)
│   ├── alembic.ini           # Alembic 迁移工具配置文件
│   ├── pyproject.toml        # 后端依赖管理与项目元数据 (基于 uv/pip)
│   └── Dockerfile            # 后端镜像构建定义 (Python 生产环境环境)
│
├── frontend/                # 前端项目根目录
│   ├── src/                 # 源代码
│   │   ├── client/          # 【核心】由 openapi-ts 自动生成的后端 SDK
│   │   │   ├── core/        # 生成的请求核心逻辑 (错误处理、类型定义等)
│   │   │   ├── schemas.gen.ts # 从后端 OpenAPI 导出的 JSON Schema
│   │   │   ├── sdk.gen.ts   # 封装好的 API 调用方法 (Service 层)
│   │   │   └── types.gen.ts # 所有的请求/响应 TypeScript 类型定义
│   │   ├── components/      # UI 组件 (Radix UI / 业务组件)
│   │   ├── hooks/           # 自定义 React Hooks (认证、状态等)
│   │   ├── lib/             # 公共工具库 (通常包含 utils, tailwind 合并函数等)
│   │   ├── routes/          # 【路由】TanStack Router 基于文件的路由实现
│   │   ├── index.css        # 全局样式 (Tailwind CSS 入口)
│   │   ├── main.tsx         # 应用渲染入口 (React 19)
│   │   ├── routeTree.gen.ts # TanStack Router 自动生成的路由映射树
│   │   └── vite-env.d.ts    # Vite 环境变量类型声明
│   ├── .tanstack/           # TanStack Router 的本地缓存/配置目录
│   ├── tests/               # Playwright 测试用例
│   ├── .dockerignore        # 排除不需要打进 Docker 镜像的文件 (如 node_modules)
│   ├── .env                 # 前端环境变量 (VITE_API_URL 等)
│   ├── .gitignore           # Git 忽略文件
│   ├── biome.json           # Biome 配置文件 (替代 ESLint/Prettier，极速格式化)
│   ├── components.json      # Shadcn UI / Radix UI 的组件初始化配置
│   ├── Dockerfile           # 生产环境部署镜像 (通常是 Node 编译 + Nginx 托管)
│   ├── Dockerfile.playwright # 专门用于运行 Playwright 测试的容器镜像
│   ├── index.html           # SPA 应用的入口 HTML
│   ├── nginx.conf           # Nginx 主配置文件
│   ├── nginx-backend-not-found.conf # Nginx 特殊配置：处理前端路由刷新 404 问题
│   ├── openapi-ts.config.ts # 【重要】openapi-ts 的生成配置，定义后端接口地址和输出路径
│   ├── package.json         # 项目依赖与脚本定义
│   ├── playwright.config.ts # E2E 测试框架 Playwright 的全局配置
│   ├── tsconfig.json        # TypeScript 主配置
│   ├── tsconfig.build.json  # 专门用于生产环境构建的 TS 配置
│   ├── tsconfig.node.json   # 针对 Vite 配置文件等 Node 环境的 TS 配置
│   └── vite.config.ts       # Vite 配置文件 (集成了 React、TanStack Router 等插件)
│
├── scripts/                  # 全局自动化脚本
│   ├── prestart.sh           # 容器启动前的核心脚本 (执行迁移和初始化)
│   └── generate-client.sh    # 根据后端 Swagger 自动生成前端 API 客户端
│
├── .github/                  # GitHub Actions (CI/CD 自动化流水线)
│   └── workflows/            # 定义测试、构建、部署流程
│
├── docker-compose.yml        # 本地开发/生产编排 (整合 db, backend, frontend)
├── compose.override.yml      # (可选) 本地开发时的端口映射覆盖
├── .env                      # 所有的核心环境变量 (SECRET, DB_PASS 等)
└── .gitignore                # 忽略文件配置 (已帮你确认包含 .env)


## GIT提交规则
GitHub 支持使用冒号包裹的简写语法 :emoji_name:。这种写法在提交后会被自动渲染成对应的彩色 Emoji。
以下是开发者提交代码时最常用、最通用的简写和它们对应的场景：
- 新功能：:sparkles: $\rightarrow$ :sparkles: (Sparkles) 或 :tada: $\rightarrow$ :tada: (Celebrate)
- 修复 Bug：:bug: $\rightarrow$ :bug: (Bug)
- 重构代码：:recycle: $\rightarrow$ :recycle: (Recycle)
- 文档更新：:memo: $\rightarrow$ :memo: (Memo) 或 :books: $\rightarrow$ :books: (Books)
- 性能优化：:zap: $\rightarrow$ :zap: (Zap/Lightning)
- 测试相关：:white_check_mark: $\rightarrow$ :white_check_mark: (White Check Mark)
- 移除代码/文件：:fire: $\rightarrow$ :fire: (Fire)
- 安全修复：:lock: $\rightarrow$ :lock: (Lock)
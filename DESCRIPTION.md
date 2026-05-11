.
├── backend/                  # 后端项目 (FastAPI)
│   ├── app/                  # 主应用目录
│   │   ├── api/              # API 路由
│   │   │   ├── routes/       # 具体的业务路由实现 (users, items, login)
│   │   │   ├── deps.py       # 依赖注入 (如获取当前用户、DB 会话)
│   │   │   └── main.py       # 路由总入口 (API Router 汇总)
│   │   ├── core/             # 核心配置
│   │   │   ├── config.py     # 环境变量读取与 Pydantic 配置
│   │   │   ├── db.py         # 数据库引擎初始化
│   │   │   └── security.py   # JWT 令牌生成、密码哈希处理
│   │   ├── crud/             # 封装增删改查逻辑 (保持 API 层简洁)
│   │   ├── models.py         # SQLModel 数据库表结构模型
│   │   ├── schemas.py        # Pydantic 数据验证模型 (Request/Response Body)
│   │   ├── main.py           # FastAPI 实例初始化入口
│   │   ├── initial_data.py   # 首次运行插入初始管理员数据
│   │   └── backend_pre_start.py # 启动前数据库连接检查
│   ├── alembic/              # 数据库迁移工具目录
│   ├── tests/                # 单元/集成测试
│   ├── pyproject.toml        # 后端依赖管理 (uv/pip)
│   └── Dockerfile            # 后端镜像构建定义
│
├── frontend/                 # 前端项目 (Vue 3 + TS + Vite)
│   ├── src/
│   │   ├── api/              # 自动生成的 API 客户端 (基于 OpenAPI)
│   │   ├── components/       # UI 通用组件 (Element Plus / Shadcn)
│   │   ├── routes/           # 基于文件的路由管理 (TanStack Router)
│   │   ├── store/            # 状态管理 (Pinia)
│   │   └── theme/            # 样式与主题配置
│   ├── public/               # 静态资源
│   ├── index.html            # 入口页面
│   ├── package.json          # 前端依赖配置
│   └── Dockerfile            # 前端镜像构建定义 (通常用 Nginx 托管)
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
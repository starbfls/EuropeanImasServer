# EuropeanImasServer

欧洲偶像大师制作人社区网站。Vue 3 + Vite + Tailwind CSS 提供页面，Flask 提供 API；照片和名片支持 Supabase PostgreSQL + Storage、免注册投稿和管理员审核。

## 目录

```text
EuropeanImasServer/
├── frontend/
│   ├── public/assets/      # 按用途分类的图片、字体和纹理
│   ├── scripts/            # 构建辅助脚本
│   ├── src/
│   │   ├── api/            # 前后台 API 请求
│   │   ├── components/     # 导航、页脚、Logo 等复用组件
│   │   ├── data/           # 人物配置与自动生成的活动兜底数据
│   │   ├── router/         # 路由与后台登录守卫
│   │   ├── styles/         # 全局样式
│   │   ├── views/          # 页面组件
│   │   ├── App.vue         # 页面布局
│   │   └── main.js         # 唯一前端入口
│   └── tests/
├── backend/
│   ├── data/
│   │   ├── content/        # 公告、日历、照片分类（Git 管理）
│   │   ├── gallery.json    # 本地模式照片记录
│   │   └── business_cards.json # 本地模式名片记录
│   ├── supabase/           # 建表、权限、存储桶与配额 SQL
│   ├── tests/
│   ├── app.py              # Flask 入口、API 与静态页面
│   ├── auth.py             # 管理员认证
│   ├── uploads.py          # 图片验证、处理与限流
│   ├── submission_store.py # 本地 / Supabase 存储
│   ├── create_admin.py     # 管理员初始化
│   ├── manage_supabase.py  # 检查、迁移与删除重试
│   ├── gunicorn.conf.py    # 生产进程配置
│   └── requirements.txt
├── docs/                   # 配置、部署与维护说明
├── Dockerfile              # 前后端同域部署
└── render.yaml             # 可选的 Render 部署配置
```

各目录的维护规则、删除项目和本地产物说明见 [目录整理说明](docs/PROJECT_STRUCTURE.md)。

## 本地运行

需要 Python 3.10+（建议 3.12）和 Node.js（Docker 使用 22）。在仓库根目录打开 PowerShell：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe app.py
```

macOS / Linux 使用 `python3 -m venv .venv`，然后通过 `.venv/bin/python` 执行安装和启动命令。已有环境和配置时，直接启动后端即可。

Windows 也可在 `backend` 目录运行 `powershell -ExecutionPolicy Bypass -File .\start.ps1`，固定使用项目的 `.venv`。直接运行 `python app.py` 会使用终端当前的 Python，可能缺少项目依赖。

另开终端：

```powershell
cd frontend
npm ci
npm run dev
```

访问 <http://localhost:3000>。后端在 <http://localhost:5000>；Vite 将 `/api` 和本地 `/uploads` 转发给后端，需要同时启动两个服务。

`npm run dev` 和 `npm run build` 会从 `backend/data/content/` 自动生成前端活动兜底数据，请在完整仓库中执行。修改活动 JSON 后，重启开发服务或运行 `npm run sync:content`。

## 存储与上线

完整步骤见 [Supabase 配置与部署指南](docs/SUPABASE_SETUP.md)。后端配置模板为 `backend/.env.example`，密钥只放在 `backend/.env` 或服务器环境变量中。

- `STORAGE_BACKEND=local`：投稿记录写入 `backend/data/`，图片保存于 `backend/uploads/`。
- `STORAGE_BACKEND=supabase`：投稿记录和图片保存在云端，不再读写本地投稿 JSON。
- 公告、日历和照片分类始终来自 `backend/data/content/`。
- Docker 会构建前端，再通过 Gunicorn + Flask 提供页面和 API；健康检查为 `/api/health`。

## 验证

```powershell
cd frontend
npm test
npm run build
```

```powershell
cd backend
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

后端测试使用模拟 HTTP，不会上传图片或修改真实 Supabase 数据。

## 页面

| 路由 | 页面 |
|---|---|
| `/` | 首页 |
| `/announcements`、`/announcements/:id` | 活动公告与详情 |
| `/imas-calendar` | 偶像大师活动日历 |
| `/gallery`、`/gallery/upload` | 照片墙与独立投稿页面 |
| `/business-cards` | 名片墙 |
| `/rules`、`/discord` | 规章、群组链接 |
| `/admin/login`、`/admin` | 管理员登录与审核 |

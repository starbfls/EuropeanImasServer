# EuropeanImasServer

Fan website for **THE EUROPE@N IDOLM@STER UNION** — a community for European iDOLM@STER producers.

## Supabase storage and production deployment

照片墙、名片墙已支持 Supabase PostgreSQL + Storage，保留免注册投稿及管理员审核。
完整的注册、建表、环境配置、旧数据迁移与部署步骤见 [Supabase 配置指南](docs/SUPABASE_SETUP.md)。
后端配置模板为 `backend/.env.example`；服务端 Secret key 不得放入前端或提交到 Git。
默认 `STORAGE_BACKEND=local` 保留本地开发模式，显式设置 `supabase` 后不再写本地投稿 JSON。
Dockerfile / render.yaml 提供前后端同域部署，用户数据在云端保存，无需投稿数据盘。

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + Tailwind CSS + Vue Router |
| Backend | Python / Flask |

## Project Structure

```
EuropeanImasServer/
├── frontend/          # Vue 3 + Vite application (port 3000)
│   ├── src/
│   │   ├── views/     # Page components (Home, News, Gallery, Rules)
│   │   ├── components/# Shared components (NavBar, Footer, NewsCard)
│   │   └── router/    # Vue Router config
│   └── public/        # Static assets (logo.png, europe.png)
└── backend/           # Flask API server (port 5000)
    └── app.py         # Routes: /api/news, /api/gallery, /api/health
```

## Run Locally

### 1. Backend (Flask)

#### Windows (Command Prompt)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Windows (PowerShell)
```powershell
cd backend
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

#### macOS / Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The API will be available at **http://localhost:5000**

### 2. Frontend (Vue + Vite)

```bash
cd frontend
npm install
npm run dev
```

The site will be available at **http://localhost:3000**

> The Vite dev server proxies all `/api/*` requests to `http://localhost:5000`, so both servers must be running for dynamic data to load. The frontend gracefully falls back to inline mock data if the backend is unreachable.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/news` | Returns all news articles |
| GET | `/api/news/<id>` | Returns a single article |
| GET | `/api/gallery` | Returns all gallery items |
| GET | `/api/health` | Health check |

## Pages

| Route | Page |
|-------|------|
| `/` | Homepage with hero banner and latest news |
| `/news` | News feed with all articles |
| `/news/:id` | Single article (renders Markdown content) |
| `/gallery` | Filterable masonry photo gallery with lightbox |
| `/rules` | Community rules and Discord / QQ group links |

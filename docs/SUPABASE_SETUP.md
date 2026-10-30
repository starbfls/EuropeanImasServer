# Supabase 配置、迁移与验收

照片墙、名片墙使用 Supabase PostgreSQL + Storage。浏览器只访问 Flask，用户不用注册
Supabase 账号，原来的管理员账号和审核页面继续使用。

活动公告、偶像大师活动日历、照片分类与官方图片继续由 Git 管理，不需要导入数据库。
`backend/data/temp_data.json` 不参与本方案。

## 1. 注册并创建项目

1. 打开 <https://supabase.com/dashboard>，注册/登录（可使用 GitHub）。
2. 创建 Organization，然后点击 **New project**。
3. 填写项目名，例如 `european-imas`，设置并保存数据库密码。
4. 选择欧洲区域，尽量与网站后端靠近，例如 Frankfurt；等待项目初始化完成。
5. 测试阶段可以使用可用的免费套餐；正式开放投稿前，在 Billing 中核对当前容量、
   流量、休眠与备份限制，选择适合的套餐。不要把免费额度当作永久无限存储。

## 2. 创建数据库表和两个图片桶

1. 在项目左侧打开 **SQL Editor**，新建查询。
2. 复制仓库 `backend/supabase/schema.sql` 的全部内容，粘贴后点击 **Run**。
   这是在自己的新项目中初始化，不需要把数据库密码写进代码。
3. 打开 **Table Editor**，确认有 `submissions` 和 `media_settings`。
4. 打开 **Storage**，确认以下两个桶：

   | 桶 | 可见性 | 内容 |
   |---|---|---|
   | `imas-pending` | Private | 待审核照片、名片及缩略图 |
   | `imas-public` | Public | 已审核的照片、名片及缩略图 |

SQL 已开启表的 RLS，并撤销匿名/普通用户的表权限。无需另外给匿名用户创建上传或读表策略。
Flask 用服务端密钥操作。不要把 `imas-pending` 改成 Public。

脚本可重复运行，不清空投稿；它会恢复这两个桶的预期可见性。请在本网站专用的新项目中运行。

## 3. 获取项目 URL 和服务端密钥

1. 项目的 **Connect** 对话框中复制 Project URL（形如 `https://xxxx.supabase.co`）。
2. 打开 **Settings → API Keys**，创建/复制一个 **Secret key**（通常以 `sb_secret_` 开头）。
   该位置也提供旧版 `service_role` key，代码仍兼容，但优先使用新的 Secret key。
3. 不要使用 publishable/anon key 作为后端管理密钥，也不要使用数据库密码代替 API key。

密钥只放在 `backend/.env` 或托管平台的后端环境变量里。
**不要放进 `frontend/.env`、`VITE_` 变量、Git、聊天或截图。**

## 4. 本地安装与配置

需要有效的 Python 3.10+（建议 3.12）和 Node.js。仓库里的旧 `venv` 如果指向已卸载的 Python，
请新建 `.venv`，不要复制旧虚拟环境到另一台机器。

如果 PowerShell 提示找不到 `python`，先从 <https://www.python.org/downloads/windows/>
安装 Python，勾选 **Add python.exe to PATH**，重新打开终端并执行 `python --version` 确认。
如果没有 Node.js，从 <https://nodejs.org/> 安装 LTS，重新开终端确认 `node --version` 和 `npm --version`。

在仓库目录用 PowerShell 执行：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

如果已有 `backend/.env`，直接编辑并增加下列配置，不要覆盖已有管理员凭据：

```dotenv
STORAGE_BACKEND=supabase
SUPABASE_URL=https://你的项目标识.supabase.co
SUPABASE_SECRET_KEY=你的服务端SecretKey
SUPABASE_PENDING_BUCKET=imas-pending
SUPABASE_PUBLIC_BUCKET=imas-public
FLASK_DEBUG=false
```

旧版 key 可填 `SUPABASE_SERVICE_ROLE_KEY`，但不要同时填写两个不同项目的 key。
同名进程环境变量优先于 `.env`，修改后需要重启后端。

没有管理员账号时执行以下命令（已有账号可跳过；再次执行会重置该账号密码）：

```powershell
.\.venv\Scripts\python.exe create_admin.py --username admin
```

命令会把随机签名密钥与密码哈希写入 `.env`，并在你的终端显示一次生成的登录密码，请自行保存。

## 5. 检查云端连接

```powershell
.\.venv\Scripts\python.exe manage_supabase.py check
```

该命令只读：检查数据表、API 访问权限、两个桶是否存在及可见性是否正确，不上传任何图片。
失败时按顺序检查依赖、URL、Secret key、SQL 是否执行、项目网络连通性。
`/api/health` 只检查 Flask 是否运行，不能替代这里的云端连接检查。

## 6. 可选：迁移现有照片和名片

如果 `backend/data/gallery.json`、`business_cards.json` 中已经有要保留的记录，
须同时保留其引用的 `backend/uploads/` 图片。图片被 `.gitignore` 忽略，不能只从 Git 克隆 JSON。

先预检（读取云端与本地，不上传、不删除）：

```powershell
.\.venv\Scripts\python.exe manage_supabase.py migrate
```

显示 `ready` 后再实际导入：

```powershell
.\.venv\Scripts\python.exe manage_supabase.py migrate --apply
```

已审核的直接导入公开桶，待审核的导入私有桶。导入时重新编码图片并清除隐私元数据，
生成新的云端记录 ID；`legacy_key` 用来跳过已导入记录，重跑不会覆盖线上审核结果。
迁移不会删除本地 JSON 或图片。不要在两个本地数据集里复用同一个旧记录 ID 后反复迁移。
先完成迁移再开放投稿；过程中保持同一份本地数据源，不要并行运行迁移。

如果目前记录只用于测试、线上不需要保留，可以跳过本步，云端照片墙和名片墙会从空列表开始。

## 7. 启动并验收完整流程

后端：

```powershell
.\.venv\Scripts\python.exe app.py
```

另开终端，在 `frontend` 下执行 `npm ci`、`npm run dev`，访问 <http://localhost:3000>：

1. 投稿一张小图片。Storage 的私有桶应有图片和缩略图，数据库应出现 `approved=false` 的记录。
2. 打开公开照片墙，未审核图片不应出现；浏览器开发者工具不应出现 Secret key。
3. 进入 `/admin/login`，使用步骤 4 的账号密码，查看待审核图片。
4. 待审核预览使用 15 分钟签名链接，后台会在到期前刷新；也可以点击“刷新列表”。
5. 通过审核后，图片应出现在公开桶和照片墙，私有副本被清理。
6. 上传名片正反面，确认两张都能预览，审核后可在名片墙翻面查看。
7. 驳回一条投稿/下架一张图片，确认记录及云端图片均被删除。
8. 重启 Flask、重新构建前端，确认已通过的投稿仍然存在。

云端不可用时页面显示错误和重试入口，不会静默回落到本地 JSON。
`STORAGE_BACKEND=local` 仅用于继续本地开发，它不会同步或展示云端投稿。

## 8. 发布到生产环境

前后端同域部署，浏览器继续使用 `/api`，无需 Supabase 前端配置。
仓库根目录的 Dockerfile 会构建前端，并使用 Gunicorn + Flask 提供页面和 API。
可在 Render 导入根目录的 `render.yaml` Blueprint，或创建 Docker Web Service：

1. 关联 GitHub 仓库，Dockerfile 路径为 `./Dockerfile`，区域选 Frankfurt。
2. 在后端环境变量中设置 `STORAGE_BACKEND=supabase`、`SUPABASE_URL`、
   `SUPABASE_SECRET_KEY`、`ADMIN_USERNAME`、`ADMIN_PASSWORD_HASH`、`SECRET_KEY`。
   后三项来自你自己的 `backend/.env`，不要提交这个文件。Blueprint 会自动生成新的 `SECRET_KEY`。
3. 保持 `FLASK_DEBUG=false`，健康检查路径 `/api/health`。
4. 先保持一个实例、一个 Gunicorn worker；上传频率限制仍在进程内存，扩容前需要共享限流存储。
5. 不需要给投稿数据挂持久磁盘；活动公告/日历 JSON 仍从代码仓库读取。
6. 在可信反代部署中核对 `X-Forwarded-For`，再设置 `TRUST_PROXY=true`，以免所有访客共用代理 IP 的上传限额。
7. 云端生成的公开图片链接由浏览器直接加载，迁移后不再请求本地 `/uploads/`。
8. 实际部署后重复步骤 7 的验收，再绑定自己的域名。

## 9. 容量、备份及异常清理

- SQL 默认限制已登记图片总量为 **512 MiB**（包括原图和缩略图），所有并发插入通过数据库锁检查。
  同一张图片审批期间暂时有两份、上传失败残留、备份和下载流量不包含在这个数字中，请预留套餐余量。
  扩容后可在 SQL Editor 调整：

  ```sql
  update public.media_settings set max_bytes = 2147483648 where id = true;
  ```

- 图片保存失败、数据库写入失败时会尝试回滚；如果网络中断导致无法判断数据库是否已提交，
  代码保留图片，避免误删已经成功记录的文件。应结合后端日志检查残留对象。
- 删除先把记录设为 `deleting=true` 隐藏，再删公开/私有图片，最后删除记录；清理失败时会返回错误。
  管理员可以在后端终端重试：

  ```powershell
  python manage_supabase.py retry-deletes
  python manage_supabase.py retry-deletes --apply
  ```

- 待审核私有副本清理失败不影响已批准记录，后续删除会同时清理两个桶。
- 公开图片缓存设置为 60 秒，下架不会撤回用户已下载的副本，旧缓存也可能短暂存在。
- **数据库备份不包含 Storage 的实际图片文件**。请分别备份 PostgreSQL 和两个桶的对象，
  并测试恢复；不要只备份 SQL。

## 官方参考

- [服务端 API keys](https://supabase.com/docs/guides/getting-started/api-keys)
- [Storage 公开/私有桶](https://supabase.com/docs/guides/storage/buckets/fundamentals)
- [Python SDK](https://supabase.com/docs/reference/python/introduction)
- [数据库备份与 Storage 的区别](https://supabase.com/docs/guides/platform/backups)

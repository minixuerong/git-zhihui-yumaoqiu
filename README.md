# 多源异构数据驱动岗位和能力图谱构建与动态演化分析研究

## 项目概述

本项目是一个岗位和能力图谱构建与动态演化分析平台，支持多源数据的采集、清洗、分析和可视化展示。

- **后端**: FastAPI + SQLAlchemy + MySQL
- **前端**: Vue 3 + TypeScript + Vite

## 技术栈

### 后端
- **框架**: FastAPI 0.115+
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0+
- **数据验证**: Pydantic 2.0+
- **认证**: JWT (python-jose)
- **密码加密**: passlib (pbkdf2_sha256)
- **文档**: Swagger UI / ReDoc

### 前端
- **框架**: Vue 3 + TypeScript (Composition API + `<script setup>`)
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router (Hash History)
- **UI组件库**: Element Plus
- **HTTP请求**: Axios

## 项目结构

```
backend/                    # 后端（FastAPI）
├── app/
│   ├── main.py              # 入口文件
│   ├── database.py          # 数据库连接配置
│   ├── models.py            # 数据库ORM模型（12张表）
│   ├── schemas.py           # 数据验证模型
│   ├── crud.py              # CRUD操作封装
│   └── routers/
│       ├── __init__.py
│       ├── admin.py         # 后台管理接口（统计/演化/任务）
│       ├── analysis.py      # AI分析结果提交接口
│       ├── cleaner.py       # 智能体清洗数据提交接口
│       ├── crawler.py       # 爬虫数据提交接口
│       ├── jobs.py          # 岗位管理接口
│       ├── match.py         # 人岗匹配接口
│       ├── resumes.py       # 简历解析接口
│       ├── skills.py        # 技能管理接口
│       └── users.py         # 用户认证接口
├── tests/
│   └── test_api.py          # 接口测试（41个测试用例）
├── .env                     # 环境配置
├── .env.example             # 环境配置示例
└── requirements.txt         # 依赖列表

frontend/                   # 前端（Vue 3）
├── src/
│   ├── api/                # API请求封装
│   │   ├── index.ts        # Axios 实例配置
│   │   ├── admin.ts        # 后台管理 API
│   │   ├── jobs.ts         # 岗位 API
│   │   ├── skills.ts       # 技能 API
│   │   └── users.ts        # 用户 API
│   ├── stores/
│   │   └── user.ts         # 用户状态管理（Pinia）
│   ├── router/
│   │   └── index.ts        # 路由配置（/login, /admin, /user）
│   ├── components/
│   │   └── AppSidebar.vue  # 后台管理侧边栏组件
│   ├── views/
│   │   ├── login/
│   │   │   └── LoginView.vue     # 登录/注册页
│   │   ├── admin/
│   │   │   ├── AdminView.vue            # 后台管理主容器
│   │   │   ├── DashboardPanel.vue       # 数据概览面板
│   │   │   ├── JobManagementPanel.vue   # 岗位数据管理面板
│   │   │   ├── SkillManagementPanel.vue # 技能数据管理面板
│   │   │   ├── UserManagementPanel.vue  # 用户管理面板
│   │   │   ├── UpdateConfigPanel.vue    # 更新时间配置面板
│   │   │   └── ScheduleConfigPanel.vue  # 循环任务配置面板
│   │   └── user/
│   │       └── UserView.vue    # 用户端主页面（含我的首页 + 岗位发现）
│   ├── App.vue
│   └── style.css
├── package.json
├── vite.config.ts
└── tsconfig.json

UI/                         # 原始静态 HTML 原型（参考用）
├── assets/                 # 静态资源（auth.js, sidebar.css）
├── admin.html              # 后台管理原型
├── discovery.html          # 岗位发现原型
├── index.html              # 用户首页原型
├── login.html              # 登录页原型
├── resume.html             # 上传简历原型
├── match.html              # 人岗匹配原型
├── graph.html              # 能力图谱原型
├── update.html             # 能力更新原型
├── user-learning.html      # 学习规划原型
└── user-match.html         # 用户匹配分析原型
```

## 数据库模型（12张表）

### 数据库信息
- **数据库名**: `capability_graph`
- **字符集**: utf8mb4
- **排序规则**: utf8mb4_unicode_ci

### 表结构总览

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| users | 用户信息 | id, username, password_hash, email, role |
| jobs | 岗位信息 | id, name, code, category_id, department, core_responsibilities |
| skills | 技能信息 | id, name, code, category, level, description |
| capability_requirements | 岗位能力要求 | id, job_id, skill_id, requirement_type, level_required |
| job_categories | 岗位分类 | id, name, parent_id |
| resumes | 简历信息 | id, filename, file_path, content, parsed_skills |
| resume_skills | 简历技能 | id, resume_id, skill_id, level |
| match_records | 匹配记录 | id, resume_id, job_id, match_score |
| job_evolutions | 岗位演化 | id, job_id, changes_summary, changed_fields |
| jd_data_sources | 数据源配置 | id, name, url, enabled |
| crawl_tasks | 爬取任务 | id, task_id, status, source_name |
| ai_analysis_results | AI分析结果 | id, job_id, analysis_result, confidence |

### 各表详细结构

#### 1. users（用户表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | int(11) | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| username | varchar(100) | NOT NULL, UNIQUE | 用户名 |
| password_hash | varchar(255) | NOT NULL | 密码哈希值 |
| email | varchar(255) | NULL | 邮箱 |
| full_name | varchar(200) | NULL | 真实姓名 |
| role | enum('admin','user') | DEFAULT 'user' | 角色 |
| is_active | tinyint(1) | DEFAULT 1 | 是否激活 |
| created_at | datetime | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 2. jobs（岗位表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | int(11) | PRIMARY KEY, AUTO_INCREMENT | 岗位ID |
| name | varchar(200) | NOT NULL | 岗位名称 |
| code | varchar(100) | NOT NULL, UNIQUE | 岗位编码 |
| category_id | int(11) | FOREIGN KEY | 分类ID |
| department | varchar(200) | NULL | 所属部门 |
| core_responsibilities | text | NULL | 核心职责 |
| typical_scenarios | text | NULL | 典型应用场景 |
| is_new | tinyint(1) | NULL | 是否新岗位 |
| status | enum('draft','active','deprecated') | NULL | 状态 |
| data_source | varchar(500) | NULL | 数据来源 |
| confidence_score | float | NULL | 置信度 |
| is_deleted | tinyint(1) | DEFAULT 0 | 软删除标记 |
| created_at | datetime | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3. skills（技能表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | int(11) | PRIMARY KEY, AUTO_INCREMENT | 技能ID |
| name | varchar(200) | NOT NULL | 技能名称 |
| code | varchar(100) | NOT NULL, UNIQUE | 技能编码 |
| category | varchar(100) | NULL | 技能类别 |
| level | enum('beginner','intermediate','advanced') | NULL | 技能等级 |
| description | text | NULL | 技能描述 |
| created_at | datetime | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 4-12 其余表结构（capability_requirements, job_categories, resumes, resume_skills, match_records, job_evolutions, jd_data_sources, crawl_tasks, ai_analysis_results）保持不变，详细信息参考旧版 README 对应章节。

### ER关系图

```
users ───< resumes ───< resume_skills
                  ───< match_records

jobs ───< capability_requirements
    ───< job_evolutions
    ───< match_records
    ───< ai_analysis_results

skills ───< capability_requirements
        ───< resume_skills

job_categories ───< jobs

jd_data_sources ───< crawl_tasks
```

## 前端页面结构

### 路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/login` | LoginView.vue | 登录/注册 |
| `/admin` | AdminView.vue | 后台管理（管理员） |
| `/user` | UserView.vue | 用户端首页（普通用户） |

### 登录页 (`/login`)
- 左侧 Hero 区 + 右侧登录卡片
- 支持记住密码、验证码登录、忘记密码
- **立即注册**弹窗（调用 `POST /users/register`）

### 后台管理 (`/admin`)
7 个功能面板，通过侧边栏 tab 切换：

| Tab | 面板 | 功能 |
|-----|------|------|
| 数据概览 | DashboardPanel | 岗位/技能/用户统计、更新记录、系统运行状态 |
| 岗位数据管理 | JobManagementPanel | 岗位列表（CRUD）、今日新增筛选、分页 |
| 技能数据管理 | SkillManagementPanel | 技能列表（CRUD） |
| 用户管理 | UserManagementPanel | 用户列表（编辑/禁用） |
| 更新时间配置 | UpdateConfigPanel | 数据更新调度时间配置 |
| 循环任务配置 | ScheduleConfigPanel | 爬取任务管理（添加/删除/批量管理） |

### 用户端 (`/user`)
侧边栏导航 + 内容区，默认展示**岗位发现**页面：

| 导航 | 功能 |
|------|------|
| 我的首页 | 统计卡片、快捷操作、推荐岗位、最近活动、学习进度 |
| 岗位发现 | 发现配置表单 + 实时岗位列表（分页，每页48条）+ 详情弹窗 |
| 上传简历 | 开发中 |
| 匹配分析 | 开发中 |
| 学习规划 | 开发中 |
| 能力图谱 | 开发中 |
| 能力更新 | 开发中 |

## API接口清单

### 基础接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | / | 欢迎页 |
| GET | /health | 健康检查 |

### 用户认证 `/api/v1/users`

**实现文件**: [routers/users.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/users.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| POST | /users/register | 用户注册 | 无 | 接收 `username` + `password` + `role`(user/hr)，pbkdf2_sha256 哈希存库 |
| POST | /users/login | 用户登录 | 无 | 校验密码 → 生成 JWT(30min) → 返回 token；**admin 角色拒绝登录**（返回"账户或密码错误"） |
| GET | /users/me | 当前用户信息 | JWT | 解析 token 中的 sub，查库返回用户信息（含 role） |
| GET | /users/ | 用户列表 | Admin | 分页查询所有用户 |
| GET | /users/{user_id} | 用户详情 | JWT | 按 ID 查用户 |

**实现要点**：
- 密码使用 `pbkdf2_sha256` 不可逆哈希，不存明文
- JWT 使用 `python-jose` 签发，有效期 30 分钟
- `role` 字段区分 `user`(求职者) / `hr`(招聘者) / `admin`(管理员)
- `login` 接口拦截 admin 角色的普通登录，强制走 `/login/admin` 隐藏入口
- 注册仅开放 `user` 和 `hr` 两种角色

### 后台管理员认证 `/api/v1/admin`

**实现文件**: [routers/admin.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/admin.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| POST | /admin/login | 管理员登录 | 无 | 查独立的 `admins` 表 → 返回 JWT(sub=`__backdoor_admin__`) |
| GET | /admin/dashboard/stats | 数据概览统计 | JWT | 聚合查询：岗位数、技能数、用户数、今日新增 |
| GET | /admin/evolutions | 全局演化记录 | JWT | 分页返回所有演化记录，关联岗位名称 |
| GET | /admin/tasks | 任务列表 | JWT | 分页返回爬取任务列表 |
| DELETE | /admin/tasks/{task_id} | 删除任务 | Admin | 按 ID 删除爬取任务 |

**实现要点**：
- 管理员不存储在 `users` 表中，使用独立的 `admins` 表存储
- 访问路径 `/login/admin` 在 URL 层面不可见，需要手动输入触发
- `admins` 表通过后端启动时的 `init_default_admin()` 自动初始化默认管理员 `admin / admin123`
- 管理端接口不依赖 `users` 表的 role 判断，使用独立的 JWT sub 标识 `__backdoor_admin__`

### 岗位管理 `/api/v1/jobs`

**实现文件**: [routers/jobs.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/jobs.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| GET | /jobs/ | 岗位列表 | 可选 | 支持 `data_type`(raw/cleaned) 筛选、`search`(名称/编码)、分页、排序 |
| GET | /jobs/{job_id} | 岗位详情 | 可选 | 返回岗位完整信息（含关联分类） |
| POST | /jobs/ | 创建岗位 | JWT | 创建岗位，支持多 `data_type` 批量创建 |
| PUT | /jobs/{job_id} | 更新岗位 | JWT | `exclude_unset=True` 只更新传入字段 |
| DELETE | /jobs/{job_id} | 删除岗位 | JWT | 软删除（`is_deleted=True`），不物理删除 |
| GET | /jobs/{job_id}/capabilities | 岗位能力要求 | 可选 | 获取该岗位所有技能要求（含技能名称、级别） |
| POST | /jobs/{job_id}/capabilities | 添加能力要求 | JWT | 关联技能到岗位 |
| GET | /jobs/{job_id}/evolutions | 岗位演化记录 | 可选 | 获取该岗位的历史演化记录 |
| POST | /jobs/{job_id}/evolutions | 创建演化记录 | JWT | 记录岗位变化（变化摘要、变化字段） |

**实现要点**：
- `data_type` 字段区分原始数据(`raw`)和清洗后数据(`cleaned`)，管理端和用户端按此字段分流展示
- 全部使用 SQLAlchemy ORM 参数化查询，无原始 SQL 拼接
- 管理员后端管理端添加岗位时可通过复选框选择数据来源

### 技能管理 `/api/v1/skills`

**实现文件**: [routers/skills.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/skills.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| GET | /skills/ | 技能列表 | 可选 | 支持分类筛选、名称搜索 |
| GET | /skills/{skill_id} | 技能详情 | 可选 | 返回技能完整信息 |
| POST | /skills/ | 创建技能 | Admin | 创建技能（名称+编码+分类+等级+描述） |
| PUT | /skills/{skill_id} | 更新技能 | Admin | 部分更新 |
| DELETE | /skills/{skill_id} | 删除技能 | Admin | 物理删除 |

### 简历管理 `/api/v1/resumes`

**实现文件**: [routers/resumes.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/resumes.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| POST | /resumes/upload | 上传简历 | JWT | 接收 PDF/DOCX/TXT，文件白名单校验，`uploader_id` 自动绑定当前用户 |
| GET | /resumes/ | 简历列表 | JWT | **用户隔离**：只返回当前用户的简历 `WHERE uploader_id=当前用户` |
| GET | /resumes/{resume_id} | 简历详情 | JWT | 校验 `uploader_id` 归属，拒绝越权访问 |
| GET | /resumes/{resume_id}/skills | 简历技能 | JWT | 获取该简历关联的技能 |
| POST | /resumes/{resume_id}/skills | 添加简历技能 | JWT | 关联技能到简历 |
| DELETE | /resumes/{resume_id} | 删除简历 | JWT | 校验 `uploader_id` 归属，拒绝跨用户删除 |
| GET | /resumes/{resume_id}/match/{job_id} | 匹配分析 | JWT | 规则匹配分析（关键词提取 + 重合度计算），返回分数/匹配技能/缺失技能 |

**实现要点**：
- 用户数据严格隔离：所有简历操作均校验 `uploader_id == current_user.id`
- 文件上传白名单：仅允许 `application/pdf`、`application/vnd.openxmlformats-officedocument.wordprocessingml.document`、`text/plain`
- 匹配分析当前为规则版，预留接口位置用于后续接入 AI 模型

### 人岗匹配 `/api/v1/match`

**实现文件**: [routers/match.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/match.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| POST | /match/analysis | 匹配度分析 | JWT | 接收 `resume_id` + `job_id`，基于 `capability_requirements` 表的技能要求匹配分析 |
| GET | /match/records | 匹配记录 | JWT | 返回当前用户的匹配历史 |
| GET | /match/records/{record_id} | 匹配详情 | JWT | 单条匹配记录完整信息 |

**实现要点**：
- 分析维度：技能匹配率、要求覆盖率、等级差距
- 返回结构化结果：总体分数 + 详细技能对比 + 改进建议

### 爬虫/智能体/AI 对接

**实现文件**: [routers/crawler.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/crawler.py)、[routers/cleaner.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/cleaner.py)、[routers/analysis.py](file:///c:/Users/23107/Desktop/zhihui/backend/app/routers/analysis.py)

| 方法 | 接口 | 说明 | 鉴权 | 实现 |
|------|------|------|------|------|
| POST | /crawler/submit | 提交爬取数据 | API Key | 爬虫写入 `jobs` 表 (`data_type='raw'`) |
| POST | /cleaner/submit | 提交清洗数据 | API Key | 智能体写入 `jobs` 表 (`data_type='cleaned'`) |
| GET | /analysis/jobs/{job_id}/cleaned | 获取清洗数据 | API Key | 返回已清洗的岗位数据 |
| POST | /analysis/submit | 提交 AI 分析 | API Key | 写入 `ai_analysis_results` 表 |
| GET | /analysis/results | AI 分析结果列表 | JWT | 分页返回分析结果 |
| GET | /analysis/results/{result_id} | AI 分析详情 | JWT | 返回单条分析结果 |

### 用户/HR/管理员权限架构

```
登录 POST /api/v1/users/login
         ↓
    ┌─ role='user'  ─→ 前端跳转 /user → 只能访问求职者接口（简历上传、匹配分析）
    │
    ├─ role='hr'     ─→ 前端跳转 /hr   → 只能访问招聘者接口（岗位发布、简历筛选）
    │
    └─ role='admin'  ─→ 该路径被后端拦截，返回"账户或密码错误"
                        只能通过隐藏入口 `/login/admin` → 查 `admins` 表 → 跳转 /admin

越权防护（三层）：
  第1层 — 前端路由守卫：URL 直接输入其他角色路径时自动跳转对应首页
  第2层 — 后端 Depends：get_current_user → get_hr_user / get_admin_user 按角色授权
  第3层 — 数据隔离：所有简历操作校验 uploader_id，拒绝跨用户访问
```

## 数据流向

```
爬虫 → crawler/submit → jobs (`data_type='**raw**'`)     ← 管理端查看
  ↓
智能体清洗 → cleaner/submit → jobs (`data_type='**cleaned**'`) ← 用户端查看
  ↓
智能体把清洗结果发给AI大模型（直接传，不走后端）
  ↓
AI大模型分析 → analysis/submit → ai_analysis_results表（能力图谱）
  ↓
前端展示 → jobs + ai_analysis_results + capability_requirements
```

> **`jobs` 表 `data_type` 字段说明：**
> - `raw` — 爬虫原始数据，管理端可见（可筛选查看）
> - `cleaned` — 智能体清洗后数据，用户端可见（`is_new` 标记为新发现）

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

修改 `.env` 文件：

```
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/capability_graph
SECRET_KEY=my-secret-key-2026-capability-graph
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
DEBUG=True
```

### 3. 创建数据库

```sql
CREATE DATABASE capability_graph CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 安装前端依赖

```bash
cd frontend
npm install
```

### 5. 启动服务

```bash
# 终端1：启动后端
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2：启动前端
cd frontend
npm run dev
```

### 6. 访问

- 前端页面: http://localhost:5173
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 7. 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | password |
| 普通用户 | 注册新账号 | — |

登录后自动跳转：
- **管理员** → `/admin` 后台管理
- **普通用户** → `/user` 用户端

## 接口测试

```bash
cd backend
python -m pytest tests/test_api.py -v
```

## 认证机制

- 使用 JWT Token，有效期30分钟
- 请求时在 Header 中携带：`Authorization: Bearer <token>`
- 后端自动校验 Token 有效性，401 返回未授权

## 开发说明

### 新增后端接口流程

1. 在 `models.py` 中添加数据库模型
2. 在 `schemas.py` 中添加数据验证模型
3. 在 `crud.py` 中添加CRUD操作
4. 在 `routers/` 中添加路由文件
5. 在 `main.py` 中注册路由

### 新增前端页面流程

1. 在 `views/` 下创建页面组件
2. 在 `router/index.ts` 中注册路由
3. 如果是功能面板，参照 admin/ 拆分模式

## 技术特点

1. **前后端分离**: FastAPI 后端 + Vue 3 前端，通过 RESTful API 通信
2. **ORM操作**: SQLAlchemy 2.0 ORM，避免手写SQL
3. **数据验证**: Pydantic 2.0，自动验证请求参数
4. **密码安全**: pbkdf2_sha256 加密存储
5. **JWT认证**: 无状态认证，便于水平扩展
6. **CORS支持**: 配置允许跨域访问
7. **自动文档**: Swagger UI，零配置生成接口文档
8. **组件化前端**: 后台管理面板拆分为 7 个独立组件

## License

MIT License

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

> 认证说明：标注 **🔒 需登录** 的接口需要在 Header 中携带 `Authorization: Bearer <token>`；未标注的接口为公开访问（爬虫/智能体/AI 对接）。

### 基础接口

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| GET | / | — | 欢迎页 |
| GET | /health | — | 健康检查 |

### 用户认证 `/api/v1/users`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| POST | /users/register | — | 注册（用户名+密码） |
| POST | /users/login | — | 登录（返回JWT Token） |
| GET | /users/ | 🔒 | 用户列表 |
| GET | /users/me | 🔒 | 获取当前登录用户信息 |
| GET | /users/{user_id} | 🔒 | 用户详情 |
| PUT | /users/{user_id} | 🔒 | 更新用户信息 |
| DELETE | /users/{user_id} | 🔒 | 删除用户 |

### 岗位管理 `/api/v1/jobs`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| GET | /jobs/ | 🔒 | 岗位列表（分页、筛选、排序、关键字搜索、今日新增过滤、按 data_type 过滤） |
| GET | /jobs/{job_id} | 🔒 | 岗位详情 |
| POST | /jobs/ | 🔒 | 创建岗位 |
| PUT | /jobs/{job_id} | 🔒 | 更新岗位 |
| DELETE | /jobs/{job_id} | 🔒 | 删除岗位（软删除） |
| GET | /jobs/{job_id}/capabilities | 🔒 | 获取岗位能力要求 |
| POST | /jobs/{job_id}/capabilities | 🔒 | 添加岗位能力要求 |
| GET | /jobs/{job_id}/evolutions | 🔒 | 获取岗位演化记录 |
| POST | /jobs/{job_id}/evolutions | 🔒 | 创建岗位演化记录 |

### 技能管理 `/api/v1/skills`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| GET | /skills/ | 🔒 | 技能列表（分页、分类筛选、关键字搜索） |
| GET | /skills/{skill_id} | 🔒 | 技能详情 |
| POST | /skills/ | 🔒 | 创建技能 |
| PUT | /skills/{skill_id} | 🔒 | 更新技能 |
| DELETE | /skills/{skill_id} | 🔒 | 删除技能 |

### 简历管理 `/api/v1/resumes`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| POST | /resumes/upload | 🔒 | 上传简历（PDF/DOCX/DOC/TXT，限制50MB） |
| GET | /resumes/pending | — | AI 模型拉取待解析简历列表 |
| POST | /resumes/{resume_id}/parse-result | — | AI 模型回写简历解析结果 |
| GET | /resumes/ | 🔒 | 简历列表（普通用户仅看自己的） |
| GET | /resumes/{resume_id} | 🔒 | 简历详情 |
| GET | /resumes/{resume_id}/skills | 🔒 | 获取简历技能 |
| POST | /resumes/{resume_id}/skills | 🔒 | 添加简历技能 |
| DELETE | /resumes/{resume_id} | 🔒 | 删除简历 |
| GET | /resumes/{resume_id}/file | 🔒 | 查看/下载简历原始文件（支持新标签页打开，token 可传 URL 参数） |

### 人岗匹配 `/api/v1/match`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| POST | /match/analysis | 🔒 | 匹配度分析（差距分析+改进建议+学习路径） |
| GET | /match/records | 🔒 | 匹配记录列表（支持按 resume_id / job_id 过滤） |
| GET | /match/records/{match_id} | 🔒 | 匹配记录详情 |

### 爬虫/智能体/AI 对接（公开接口）

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| POST | /crawler/submit | — | 提交爬取的岗位数据（批量，自动创建/更新，生成爬取任务记录） |
| POST | /cleaner/submit | — | 提交清洗后的岗位数据（基于原始岗位创建 cleaned 版本） |
| GET | /analysis/jobs/{job_id}/cleaned | — | 获取清洗后岗位数据（含能力要求） |
| POST | /analysis/submit | — | 提交AI分析结果 |
| GET | /analysis/results | 🔒 | 分析结果列表（支持按 job_id 过滤） |
| GET | /analysis/results/{result_id} | 🔒 | 分析结果详情 |

### 后台管理 `/api/v1/admin`

| 方法 | 接口 | 认证 | 说明 |
|------|------|------|------|
| POST | /admin/login | — | 管理员登录（查 admins 表，返回 JWT Token） |
| GET | /admin/dashboard/stats | 🔒 | 数据概览统计（岗位数/技能数/用户数/待审核更新/今日新增） |
| GET | /admin/evolutions | 🔒 | 全局演化记录列表（含岗位名称，分页） |
| GET | /admin/tasks | 🔒 | 任务列表（爬取任务，分页） |
| DELETE | /admin/tasks/{task_id} | 🔒(admin) | 删除指定任务（仅管理员） |
| GET | /admin/users | 🔒 | 获取用户列表（支持按角色过滤） |
| GET | /admin/admins | 🔒(admin) | 获取管理员列表（仅管理员） |

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

基于 models.py ，每个表的作用：

表名 说明 users 普通用户（注册登录），关联简历上传、人岗匹配
 admins 管理员账号，独立于 users 表 job_categories 岗位分类（如"算法模型""数据"等），支持父子层级，对应图谱 categories jobs 岗位表 ，核心实体。含名称、编码、分类、职责、场景、状态、数据来源等，关联能力需求、演化、匹配记录 skills 技能表 ，核心实体。含名称、编码、分类、描述，被能力需求、简历技能引用 
 capability_requirements 能力需求表 ——岗位与技能的 关联关系 。记录每个岗位需要什么技能、要求类型（必须/优先）、等级、重要度评分。这就是图谱 links 的数据源 
 resumes 简历表。存文件名、路径、解析内容、AI 解析结果、状态 
 resume_skills 简历技能中间表。记录每份简历解析出的技能及熟练度 
 match_records 人岗匹配记录。存简历与岗位的匹配得分、差距分析、学习建议 
 job_evolutions 岗位演化记录。跟踪岗位变更历史（新增/更新/删除/分类变更） 
 jd_data_sources JD 数据源配置。管理从哪些招聘网站抓取岗位描述 
 crawl_tasks 爬虫任务记录。跟踪每个采集任务的来源、状态、时间 
 ai_analysis_results AI 分析结果。存对岗位的 AI 分析结论、置信度、模型版本
# Flask Web Framework

基于 Flask + Jinja2 + Werkzeug 的现代化 Web 应用模板，支持 PostgreSQL 数据库。

## 技术栈

- **Flask** - 轻量级 WSGI Web 框架
- **Jinja2** - Python 模板引擎
- **Werkzeug** - 全面的 WSGI Web 应用程序库
- **PostgreSQL** - 关系型数据库 (psycopg2)

## 项目结构

```
flask-web/
├── app/
│   ├── __init__.py    # 应用工厂
│   ├── routes.py      # 路由定义
│   ├── errors.py      # 错误处理
│   ├── database.py    # 数据库连接
│   └── models.py      # SQLAlchemy 模型
├── static/
│   ├── css/
│   │   └── style.css  # 样式文件
│   └── js/
│       └── main.js    # JavaScript 文件
├── templates/
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页
│   ├── about.html     # 关于页面
│   ├── hello.html     # 问候页面
│   ├── upload.html    # 文件上传
│   ├── form.html      # 表单示例
│   ├── data.html      # 数据展示 ✨新增
│   └── errors/
│       ├── 404.html   # 404 错误页
│       └── 500.html   # 500 错误页
├── config.py          # 配置文件
├── run.py             # 启动脚本
├── requirements.txt   # 依赖列表
├── init_db.sql        # 数据库初始化脚本
└── .env.example       # 环境变量示例
```

## 快速开始

### 1. 安装 PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**或使用 Docker:**
```bash
docker run -d --name postgres -e POSTGRES_DB=flask_app -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
```

### 2. 创建数据库

```bash
# 登录 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE flask_app;

# 退出后执行初始化脚本
psql -U postgres -d flask_app -f init_db.sql
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填写数据库密码等配置
```

### 5. 运行应用

```bash
python run.py
```

### 6. 访问应用

打开浏览器访问: http://localhost:5000

## 数据库功能

### 访问数据

访问 http://localhost:5000/data 查看所有可用表：
- `/data?table=users` - 用户表
- `/data?table=products` - 产品表
- `/data?table=orders` - 订单表
- `/data?table=customers` - 客户表
- `/data?table=tasks` - 任务表

### 自定义查询

通过 POST /data/query 执行自定义 SQL（仅 SELECT）：
```bash
curl -X POST http://localhost:5000/data/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM users LIMIT 10"}'
```

### 数据库状态检查

访问 http://localhost:5000/db-status 查看连接状态

## 功能特性

- ✅ 应用工厂模式
- ✅ 蓝图模块化路由
- ✅ Jinja2 模板继承
- ✅ 错误页面处理
- ✅ 文件上传功能
- ✅ RESTful API
- ✅ PostgreSQL 数据库集成
- ✅ 数据展示页面
- ✅ 多环境配置

## API 端点

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/about` | GET | 关于页面 |
| `/hello/<name>` | GET | 带参数的问候 |
| `/data` | GET | 数据列表 |
| `/data/query` | POST | 自定义查询 |
| `/db-status` | GET | 数据库状态 |
| `/api/data` | GET/POST | API 示例 |
| `/upload` | GET/POST | 文件上传 |
| `/form` | GET/POST | 表单处理 |

## 生产部署

使用 Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

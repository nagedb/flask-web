# Flask Web Framework

基于 Flask + Jinja2 + Werkzeug 的现代化 Web 应用模板。

## 技术栈

- **Flask** - 轻量级 WSGI Web 框架
- **Jinja2** - Python 模板引擎
- **Werkzeug** - 全面的 WSGI Web 应用程序库

## 项目结构

```
flask-web/
├── app/
│   ├── __init__.py    # 应用工厂
│   ├── routes.py      # 路由定义
│   └── errors.py      # 错误处理
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
│   └── errors/
│       ├── 404.html   # 404 错误页
│       └── 500.html   # 500 错误页
├── config.py          # 配置文件
├── run.py             # 启动脚本
└── requirements.txt   # 依赖列表
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python run.py
```

### 3. 访问应用

打开浏览器访问: http://localhost:5000

## 功能特性

- ✅ 应用工厂模式
- ✅ 蓝图模块化路由
- ✅ Jinja2 模板继承
- ✅ 错误页面处理
- ✅ 文件上传功能
- ✅ RESTful API
- ✅ 多环境配置

## 环境配置

| 环境 | 配置值 | 说明 |
|------|--------|------|
| development | 开发环境 | 启用调试模式 |
| production | 生产环境 | 关闭调试 |
| testing | 测试环境 | 禁用 CSRF |

设置环境变量:
```bash
export FLASK_CONFIG=development
```

## API 端点

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/about` | GET | 关于页面 |
| `/hello/<name>` | GET | 带参数的问候 |
| `/api/data` | GET/POST | API 示例 |
| `/upload` | GET/POST | 文件上传 |
| `/form` | GET/POST | 表单处理 |

## 生产部署

使用 Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

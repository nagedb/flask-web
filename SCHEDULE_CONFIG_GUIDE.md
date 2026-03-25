# 调度配置管理功能说明

## 📋 功能概览

schedule_config 表已完整实现增删改查功能，包括 Web UI 和 REST API。

## 🌐 Web 页面

### 1. 调度配置列表页面
**URL**: `http://localhost:5000/schedule`

**功能**:
- ✅ 查看所有调度配置
- ✅ 显示公司简称、工作流名称、调度类型
- ✅ 显示调度配置详情和最后修改时间
- ✅ 编辑和删除按钮

**页面特性**:
- 表格展示所有配置
- 调度类型用 Badge 标记（Cron/Interval/Once）
- 配置内容用 code 标签展示
- 时间戳显示最后修改时间

### 2. 新增调度配置页面
**URL**: `http://localhost:5000/schedule/add`

**表单字段**:
- 公司简称 (必填)
- 工作流名称 (必填)
- 调度类型 (必填) - 下拉选择
  - Cron 表达式
  - 时间间隔
  - 一次性执行

**Cron 类型**:
- Cron 表达式 (如: `0 9 * * MON-FRI`)
- 时区 (默认: `Asia/Shanghai`)

**Interval 类型**:
- 间隔分钟数 (如: 30)
- 开始时间 (如: 08:00)
- 结束时间 (如: 18:00)

**Once 类型**:
- 执行时间 (日期时间选择器)

### 3. 编辑调度配置页面
**URL**: `http://localhost:5000/schedule/<id>/edit`

**功能**:
- ✅ 预填充现有配置
- ✅ 修改所有字段
- ✅ 保存更新

### 4. 删除功能
**方式**: 列表页面的删除按钮

**功能**:
- ✅ 确认对话框
- ✅ 删除后自动刷新列表

## 🔌 REST API

### 获取所有配置
```bash
GET /api/schedule
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "company_short_name": "ABC",
      "workflow_name": "日报生成",
      "schedule_config": {
        "type": "cron",
        "expression": "0 9 * * MON-FRI",
        "timezone": "Asia/Shanghai"
      },
      "last_modified_time": "2026-03-25T18:07:54",
      "created_at": "2026-03-25T18:07:54"
    }
  ],
  "count": 1
}
```

### 按公司筛选
```bash
GET /api/schedule?company=ABC
```

### 按工作流筛选
```bash
GET /api/schedule?workflow=日报生成
```

### 新增配置
```bash
POST /schedule/add
Content-Type: application/x-www-form-urlencoded

company_short_name=ABC&workflow_name=日报生成&schedule_type=cron&cron_expression=0 9 * * MON-FRI&timezone=Asia/Shanghai
```

### 编辑配置
```bash
POST /schedule/<id>/edit
Content-Type: application/x-www-form-urlencoded

company_short_name=ABC&workflow_name=日报生成&schedule_type=cron&cron_expression=0 10 * * MON-FRI
```

### 删除配置
```bash
POST /schedule/<id>/delete
```

**响应**:
```json
{
  "success": true,
  "message": "配置已删除"
}
```

## 📊 数据库表结构

```sql
CREATE TABLE schedule_config (
    id SERIAL PRIMARY KEY,
    company_short_name VARCHAR(50) NOT NULL,
    schedule_config JSONB NOT NULL,
    workflow_name VARCHAR(100) NOT NULL,
    last_modified_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_short_name, workflow_name)
);
```

**字段说明**:
- `id`: 主键
- `company_short_name`: 公司简称
- `schedule_config`: JSON 格式的调度配置
- `workflow_name`: 工作流名称
- `last_modified_time`: 最后修改时间
- `created_at`: 创建时间
- `updated_at`: 更新时间

**约束**:
- 公司简称 + 工作流名称 唯一约束（防止重复）

## 🎯 使用示例

### 示例 1: 创建 Cron 调度
```
公司简称: ABC
工作流名称: 日报生成
调度类型: Cron 表达式
Cron 表达式: 0 9 * * MON-FRI
时区: Asia/Shanghai
```
效果: 每周一到五早上 9 点执行

### 示例 2: 创建间隔调度
```
公司简称: XYZ
工作流名称: 数据同步
调度类型: 时间间隔
间隔分钟数: 30
开始时间: 08:00
结束时间: 18:00
```
效果: 每天 8 点到 18 点，每 30 分钟执行一次

### 示例 3: 创建一次性调度
```
公司简称: DEF
工作流名称: 月度报表
调度类型: 一次性
执行时间: 2026-03-26 10:00:00
```
效果: 2026 年 3 月 26 日 10 点执行一次

## 🔍 查询示例

### 查看 ABC 公司的所有配置
```bash
curl http://localhost:5000/api/schedule?company=ABC
```

### 查看所有日报生成的配置
```bash
curl http://localhost:5000/api/schedule?workflow=日报生成
```

## ✨ 特性

- ✅ 完整的 CRUD 操作
- ✅ 友好的 Web UI
- ✅ RESTful API
- ✅ JSON 格式的灵活配置
- ✅ 时间戳自动管理
- ✅ 唯一性约束防止重复
- ✅ 表单验证
- ✅ 错误处理
- ✅ 响应式设计

## 🚀 快速开始

1. 访问 http://localhost:5000/schedule 查看列表
2. 点击 "+ 新增配置" 添加新配置
3. 填写表单并选择调度类型
4. 点击"保存配置"
5. 在列表中可以编辑或删除配置

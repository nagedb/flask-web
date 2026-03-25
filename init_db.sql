-- PostgreSQL 数据库初始化脚本
-- 创建示例表和测试数据

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建产品表
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(50),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建客户表
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    company VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建任务表
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    assignee VARCHAR(50),
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入示例数据
INSERT INTO users (username, email, password_hash, full_name) VALUES
    ('admin', 'admin@example.com', 'hashed_password_1', '管理员'),
    ('john', 'john@example.com', 'hashed_password_2', 'John Doe'),
    ('jane', 'jane@example.com', 'hashed_password_3', 'Jane Smith')
ON CONFLICT (username) DO NOTHING;

INSERT INTO products (name, description, price, stock, category) VALUES
    ('Python 入门', 'Python 编程入门书籍', 59.99, 100, '书籍'),
    ('Flask 实战', 'Flask Web 开发实战', 79.99, 50, '书籍'),
    ('PostgreSQL 指南', '数据库管理指南', 69.99, 30, '书籍')
ON CONFLICT DO NOTHING;

INSERT INTO customers (name, email, phone, company) VALUES
    ('张三', 'zhangsan@company.com', '13800138000', '示例公司'),
    ('李四', 'lisi@company.com', '13900139000', '另一家公司')
ON CONFLICT DO NOTHING;

INSERT INTO tasks (title, description, status, priority, assignee) VALUES
    ('完成用户模块', '实现用户注册和登录功能', 'in_progress', 'high', 'john'),
    ('修复登录 Bug', '修复用户无法登录的问题', 'pending', 'urgent', 'jane'),
    ('优化数据库查询', '提升查询性能', 'completed', 'medium', 'admin')
ON CONFLICT DO NOTHING;

-- 创建查看表列表的视图
CREATE OR REPLACE VIEW available_tables AS
SELECT 'users' as table_name, '用户表' as description
UNION ALL SELECT 'products', '产品表'
UNION ALL SELECT 'orders', '订单表'
UNION ALL SELECT 'customers', '客户表'
UNION ALL SELECT 'tasks', '任务表';

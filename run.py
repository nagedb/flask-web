#!/usr/bin/env python3
"""
Flask 应用启动脚本
"""
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db

def check_database():
    """检查数据库连接"""
    try:
        result = db.execute_query("SELECT version()", fetch='one')
        if result:
            version = result.get('version', 'Unknown') if isinstance(result, dict) else str(result)
            print(f"✅ 数据库连接成功")
            print(f"   {version}")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print(f"\n请确保:")
        print(f"   1. PostgreSQL 已安装并运行")
        print(f"   2. 已创建数据库: {db.config.get('database', 'flask_app')}")
        print(f"   3. 环境变量已配置 (参考 .env.example)")
        return False

# 从环境变量获取配置，或使用默认配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app()

if __name__ == '__main__':
    # 创建上传目录
    os.makedirs('uploads', exist_ok=True)
    
    print("=" * 50)
    print("Flask Web Application")
    print("=" * 50)
    
    # 检查数据库连接
    check_database()
    print("=" * 50)
    
    # 运行开发服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

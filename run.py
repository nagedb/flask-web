#!/usr/bin/env python3
"""
Flask 应用启动脚本
"""
import os
from app import create_app

# 从环境变量获取配置，或使用默认配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app()

if __name__ == '__main__':
    # 创建上传目录
    os.makedirs('uploads', exist_ok=True)
    
    # 运行开发服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

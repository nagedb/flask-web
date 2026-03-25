"""
Flask Web Application Factory
"""
import os
from flask import Flask
from config import Config


def create_app(config_class=Config):
    """应用工厂函数"""
    # 获取应用根目录
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object(config_class)
    
    # 初始化扩展
    # from flask_sqlalchemy import SQLAlchemy
    # db = SQLAlchemy(app)
    
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)
    
    # 注册错误处理器
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)
    
    return app

"""
配置文件
"""
import os


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置（可选，取消注释启用）
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB
    UPLOAD_FOLDER = 'uploads'
    
    # Jinja2 配置
    TEMPLATES_AUTO_RELOAD = True
    Jinja2_AUTO_STRIP_EXTENSIONS = ['.html', '.jinja']


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    WTF_CSRF_ENABLED = False


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

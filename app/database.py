"""
PostgreSQL 数据库连接模块
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os


class Database:
    """数据库连接管理类"""
    
    def __init__(self):
        self.config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432'),
            'database': os.environ.get('DB_NAME', 'flask_app'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', '')
        }
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            conn = psycopg2.connect(**self.config)
            return conn
        except psycopg2.Error as e:
            print(f"数据库连接错误: {e}")
            return None
    
    @contextmanager
    def get_cursor(self, cursor_type=RealDictCursor):
        """
        上下文管理器，自动管理连接的打开和关闭
        使用方式:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
        """
        conn = self.get_connection()
        if conn is None:
            raise ConnectionError("无法连接到数据库")
        
        try:
            cursor = conn.cursor(cursor_factory=cursor_type)
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def execute_query(self, query, params=None, fetch='all'):
        """
        执行查询并返回结果
        
        Args:
            query: SQL 查询语句
            params: 查询参数 (元组或字典)
            fetch: 'all' 返回所有结果, 'one' 返回第一条, 'dict' 返回字典格式
        
        Returns:
            查询结果列表或字典
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch == 'one':
                    result = cursor.fetchone()
                    # 如果需要字典格式
                    if result and isinstance(result, tuple):
                        # 获取列名
                        col_names = [desc[0] for desc in cursor.description]
                        return dict(zip(col_names, result))
                    return result
                else:
                    results = cursor.fetchall()
                    # 转换为字典列表
                    if results and isinstance(results[0], tuple):
                        col_names = [desc[0] for desc in cursor.description]
                        return [dict(zip(col_names, row)) for row in results]
                    return results
        except Exception as e:
            print(f"查询错误: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """
        执行更新/插入/删除操作
        
        Args:
            query: SQL 语句
            params: 参数
        
        Returns:
            影响的行数
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except Exception as e:
            print(f"更新错误: {e}")
            return 0


# 创建全局数据库实例
db = Database()

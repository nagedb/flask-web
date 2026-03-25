"""
蓝图路由
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """首页"""
    return render_template('index.html', title='首页')


@main.route('/about')
def about():
    """关于页面"""
    return render_template('about.html', title='关于')


@main.route('/hello/<name>')
def hello(name):
    """带参数的问候页面"""
    return render_template('hello.html', name=name, title=f'Hello {name}')


@main.route('/api/data', methods=['GET', 'POST'])
def api_data():
    """API 示例"""
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'status': 'success', 'data': data})
    return jsonify({'status': 'ok', 'message': 'Hello from API'})


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    """文件上传示例"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))
        
        return jsonify({'success': True, 'filename': filename})
    
    return render_template('upload.html', title='文件上传')


@main.route('/form', methods=['GET', 'POST'])
def form():
    """表单处理示例"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        # 处理表单数据
        return jsonify({
            'success': True,
            'name': name,
            'email': email
        })
    
    return render_template('form.html', title='表单示例')


# ==================== 数据库相关路由 ====================

@main.route('/data')
def data_list():
    """
    数据展示页面
    支持通过 ?table=表名 参数指定要查询的表
    默认列出所有可用表
    """
    from app.database import db
    
    # 获取要查询的表名
    table_name = request.args.get('table', None)
    
    # 可访问的表（白名单，防止 SQL 注入）
    allowed_tables = ['users', 'products', 'orders', 'customers', 'tasks', 'articles']
    
    if table_name:
        if table_name not in allowed_tables:
            return render_template('data.html', 
                                 title='数据列表',
                                 error=f'表 "{table_name}" 不在允许访问列表中',
                                 tables=allowed_tables)
        
        # 查询指定表的数据
        try:
            query = f"SELECT * FROM {table_name} LIMIT 100"
            results = db.execute_query(query, fetch='all')
            
            if results is None:
                return render_template('data.html',
                                     title='数据列表',
                                     error='无法连接到数据库或查询失败',
                                     tables=allowed_tables,
                                     table_name=table_name)
            
            return render_template('data.html',
                                 title=f'{table_name} - 数据',
                                 tables=allowed_tables,
                                 table_name=table_name,
                                 data=results)
        except Exception as e:
            return render_template('data.html',
                                 title='数据列表',
                                 error=f'查询错误: {str(e)}',
                                 tables=allowed_tables)
    
    # 没有指定表，显示所有可用表
    return render_template('data.html', 
                         title='数据列表',
                         tables=allowed_tables)


@main.route('/data/query', methods=['POST'])
def data_query():
    """
    自定义 SQL 查询接口
    仅支持 SELECT 查询
    """
    from app.database import db
    
    data = request.get_json()
    query = data.get('query', '').strip().lower()
    
    # 安全检查：只允许 SELECT 查询
    if not query.startswith('select'):
        return jsonify({'error': '只允许 SELECT 查询'}), 403
    
    # 禁止危险关键字
    dangerous_keywords = ['drop', 'truncate', 'delete', 'insert', 'update', 'alter', 'create', 'grant', 'revoke']
    for keyword in dangerous_keywords:
        if keyword in query.split()[:2]:
            return jsonify({'error': f'不允许使用 {keyword} 操作'}), 403
    
    results = db.execute_query(query, fetch='all')
    
    if results is None:
        return jsonify({'error': '查询失败'}), 500
    
    return jsonify({'success': True, 'data': results, 'count': len(results)})


@main.route('/db-status')
def db_status():
    """数据库连接状态检查"""
    from app.database import db
    
    try:
        result = db.execute_query("SELECT version()", fetch='one')
        return jsonify({
            'status': 'connected',
            'version': result.get('version', 'Unknown') if isinstance(result, dict) else str(result)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==================== 调度配置相关路由 ====================

@main.route('/schedule')
def schedule_list():
    """调度配置列表页面"""
    from app.database import db
    
    try:
        # 获取查询参数
        company = request.args.get('company', '').strip()
        workflow = request.args.get('workflow', '').strip()
        schedule_type = request.args.get('schedule_type', '').strip()
        
        # 构建查询
        query = """
            SELECT id, company_short_name, workflow_name, 
                   schedule_config, updated_at 
            FROM schedule_config 
            WHERE 1=1
        """
        params = []
        
        # 添加查询条件
        if company:
            query += " AND company_short_name ILIKE %s"
            params.append(f"%{company}%")
        
        if workflow:
            query += " AND workflow_name ILIKE %s"
            params.append(f"%{workflow}%")
        
        if schedule_type:
            query += " AND schedule_config->>'type' = %s"
            params.append(schedule_type)
        
        query += " ORDER BY updated_at DESC"
        
        configs = db.execute_query(query, tuple(params) if params else None, fetch='all')
        
        return render_template('schedule.html',
                             title='调度配置',
                             configs=configs,
                             search_params={
                                 'company': company,
                                 'workflow': workflow,
                                 'schedule_type': schedule_type
                             })
    except Exception as e:
        return render_template('schedule.html',
                             title='调度配置',
                             error=f'查询失败: {str(e)}')


@main.route('/schedule/add', methods=['GET', 'POST'])
def schedule_add():
    """添加调度配置"""
    from app.database import db
    import json
    
    if request.method == 'POST':
        try:
            company = request.form.get('company_short_name')
            workflow = request.form.get('workflow_name')
            schedule_type = request.form.get('schedule_type')
            
            # 构建调度配置 JSON
            if schedule_type == 'cron':
                schedule_config = {
                    'type': 'cron',
                    'expression': request.form.get('cron_expression'),
                    'timezone': request.form.get('timezone', 'Asia/Shanghai')
                }
            elif schedule_type == 'interval':
                schedule_config = {
                    'type': 'interval',
                    'interval_minutes': int(request.form.get('interval_minutes', 30)),
                    'start_time': request.form.get('start_time'),
                    'end_time': request.form.get('end_time')
                }
            else:  # once
                schedule_config = {
                    'type': 'once',
                    'execute_time': request.form.get('execute_time')
                }
            
            query = """
                INSERT INTO schedule_config 
                (company_short_name, workflow_name, schedule_config)
                VALUES (%s, %s, %s)
                ON CONFLICT (company_short_name, workflow_name) 
                DO UPDATE SET 
                    schedule_config = EXCLUDED.schedule_config,
                    updated_at = CURRENT_TIMESTAMP
            """
            
            db.execute_update(query, (company, workflow, json.dumps(schedule_config)))
            
            return jsonify({'success': True, 'message': '配置保存成功'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('schedule_form.html', title='添加调度配置')


@main.route('/schedule/<int:config_id>/edit', methods=['GET', 'POST'])
def schedule_edit(config_id):
    """编辑调度配置"""
    from app.database import db
    import json
    
    if request.method == 'POST':
        try:
            company = request.form.get('company_short_name')
            workflow = request.form.get('workflow_name')
            schedule_type = request.form.get('schedule_type')
            
            # 构建调度配置 JSON
            if schedule_type == 'cron':
                schedule_config = {
                    'type': 'cron',
                    'expression': request.form.get('cron_expression'),
                    'timezone': request.form.get('timezone', 'Asia/Shanghai')
                }
            elif schedule_type == 'interval':
                schedule_config = {
                    'type': 'interval',
                    'interval_minutes': int(request.form.get('interval_minutes', 30)),
                    'start_time': request.form.get('start_time'),
                    'end_time': request.form.get('end_time')
                }
            else:  # once
                schedule_config = {
                    'type': 'once',
                    'execute_time': request.form.get('execute_time')
                }
            
            query = """
                UPDATE schedule_config 
                SET company_short_name = %s,
                    workflow_name = %s,
                    schedule_config = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            
            db.execute_update(query, (company, workflow, json.dumps(schedule_config), config_id))
            
            return jsonify({'success': True, 'message': '配置更新成功'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # GET 请求：获取配置详情
    try:
        query = "SELECT * FROM schedule_config WHERE id = %s"
        config = db.execute_query(query, (config_id,), fetch='one')
        
        if not config:
            return render_template('errors/404.html'), 404
        
        return render_template('schedule_form.html',
                             title='编辑调度配置',
                             config=config)
    except Exception as e:
        return render_template('schedule_form.html',
                             title='编辑调度配置',
                             error=f'查询失败: {str(e)}')


@main.route('/schedule/<int:config_id>/delete', methods=['POST'])
def schedule_delete(config_id):
    """删除调度配置"""
    from app.database import db
    
    try:
        query = "DELETE FROM schedule_config WHERE id = %s"
        db.execute_update(query, (config_id,))
        
        return jsonify({'success': True, 'message': '配置已删除'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main.route('/api/schedule', methods=['GET'])
def api_schedule_list():
    """获取调度配置 API"""
    from app.database import db
    
    try:
        company = request.args.get('company')
        workflow = request.args.get('workflow')
        
        query = "SELECT * FROM schedule_config WHERE 1=1"
        params = []
        
        if company:
            query += " AND company_short_name = %s"
            params.append(company)
        
        if workflow:
            query += " AND workflow_name = %s"
            params.append(workflow)
        
        query += " ORDER BY updated_at DESC"
        
        configs = db.execute_query(query, tuple(params) if params else None, fetch='all')
        
        if configs is None:
            configs = []
        
        return jsonify({
            'success': True,
            'data': configs,
            'count': len(configs) if configs else 0
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

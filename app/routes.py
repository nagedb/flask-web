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


@main.route('/portal')
def portal():
    """业务数据监控中心"""
    from app.database import db
    from datetime import datetime
    
    try:
        stats = {}
        
        # 获取各表数据量
        tables = ['customers', 'orders', 'products', 'tasks', 'users']
        
        for table in tables:
            try:
                # 获取总数
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                count_result = db.execute_query(count_query, fetch='one')
                count = count_result['count'] if count_result else 0
                
                # 获取最近5条
                recent_query = f"SELECT * FROM {table} ORDER BY id DESC LIMIT 5"
                recent = db.execute_query(recent_query, fetch='all') or []
                
                stats[table] = {
                    'count': count,
                    'recent': recent
                }
            except Exception as e:
                stats[table] = {'count': 0, 'recent': [], 'error': str(e)}
        
        return render_template('portal.html',
                             title='数据监控',
                             stats=stats,
                             last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        return render_template('portal.html',
                             title='数据监控',
                             error=str(e),
                             stats={},
                             last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
            schedule_config_json = request.form.get('schedule_config_json')
            
            # 解析 JSON 配置
            try:
                schedule_config = json.loads(schedule_config_json)
            except json.JSONDecodeError as e:
                return jsonify({'success': False, 'error': f'JSON 格式错误: {str(e)}'}), 400
            
            # 验证必填字段
            if not schedule_config.get('type'):
                return jsonify({'success': False, 'error': '缺少 type 字段'}), 400
            
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
            schedule_config_json = request.form.get('schedule_config_json')
            
            # 解析 JSON 配置
            try:
                schedule_config = json.loads(schedule_config_json)
            except json.JSONDecodeError as e:
                return jsonify({'success': False, 'error': f'JSON 格式错误: {str(e)}'}), 400
            
            # 验证必填字段
            if not schedule_config.get('type'):
                return jsonify({'success': False, 'error': '缺少 type 字段'}), 400
            
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


# ==================== 库存管理模块 ====================

@main.route('/inventory')
def inventory_list():
    """库存列表"""
    from app.database import db
    
    try:
        # 获取查询参数
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        alert_only = request.args.get('alert', '').strip()
        
        # 构建查询
        query = "SELECT * FROM inventory WHERE 1=1"
        params = []
        
        if search:
            query += " AND (product_code ILIKE %s OR product_name ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if alert_only == '1':
            query += " AND current_stock <= min_stock"
        
        query += " ORDER BY updated_at DESC"
        
        items = db.execute_query(query, tuple(params) if params else None, fetch='all')
        
        # 获取分类列表
        categories = db.execute_query("SELECT DISTINCT category FROM inventory WHERE category IS NOT NULL ORDER BY category", fetch='all')
        
        # 统计
        stats = {
            'total': db.execute_query("SELECT COUNT(*) as count FROM inventory", fetch='one')['count'],
            'low_stock': db.execute_query("SELECT COUNT(*) as count FROM inventory WHERE current_stock <= min_stock", fetch='one')['count'],
            'total_value': db.execute_query("SELECT SUM(current_stock) as total FROM inventory", fetch='one')['total'] or 0
        }
        
        return render_template('inventory_list.html',
                             title='库存管理',
                             items=items or [],
                             categories=[c['category'] for c in (categories or [])],
                             stats=stats,
                             search=search,
                             category=category,
                             alert_only=alert_only)
    except Exception as e:
        return render_template('inventory_list.html',
                             title='库存管理',
                             error=str(e),
                             items=[],
                             categories=[],
                             stats={'total': 0, 'low_stock': 0, 'total_value': 0})


@main.route('/inventory/add', methods=['GET', 'POST'])
def inventory_add():
    """添加入库"""
    from app.database import db
    import json
    
    if request.method == 'POST':
        try:
            product_code = request.form.get('product_code')
            product_name = request.form.get('product_name')
            category = request.form.get('category')
            unit = request.form.get('unit', '件')
            current_stock = int(request.form.get('current_stock', 0))
            min_stock = int(request.form.get('min_stock', 10))
            max_stock = int(request.form.get('max_stock', 1000))
            location = request.form.get('location')
            supplier = request.form.get('supplier')
            remark = request.form.get('remark')
            
            # 检查是否已存在
            existing = db.execute_query(
                "SELECT id, current_stock FROM inventory WHERE product_code = %s",
                (product_code,), fetch='one'
            )
            
            if existing:
                return jsonify({'success': False, 'error': '该产品编码已存在'}), 400
            
            # 插入新记录
            query = """
                INSERT INTO inventory 
                (product_code, product_name, category, unit, current_stock, min_stock, max_stock, location, supplier, remark)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_update(query, (product_code, product_name, category, unit, current_stock, min_stock, max_stock, location, supplier, remark))
            
            # 记录流水
            if current_stock > 0:
                transaction_query = """
                    INSERT INTO inventory_transaction 
                    (product_code, transaction_type, quantity, stock_before, stock_after, operator, reason)
                    VALUES (%s, 'in', %s, 0, %s, %s, %s)
                """
                db.execute_update(transaction_query, (product_code, current_stock, current_stock, 'admin', '初始入库'))
            
            return jsonify({'success': True, 'message': '添加成功'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    categories = db.execute_query("SELECT DISTINCT category FROM inventory WHERE category IS NOT NULL ORDER BY category", fetch='all')
    return render_template('inventory_form.html', title='添加库存', categories=[c['category'] for c in (categories or [])])


@main.route('/inventory/<int:item_id>/in', methods=['GET', 'POST'])
def inventory_in(item_id):
    """入库操作"""
    from app.database import db
    
    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity'))
            reason = request.form.get('reason', '入库')
            order_no = request.form.get('order_no')
            
            if quantity <= 0:
                return jsonify({'success': False, 'error': '数量必须大于0'}), 400
            
            # 获取当前库存
            item = db.execute_query("SELECT * FROM inventory WHERE id = %s", (item_id,), fetch='one')
            if not item:
                return jsonify({'success': False, 'error': '产品不存在'}), 404
            
            stock_before = item['current_stock']
            stock_after = stock_before + quantity
            
            # 更新库存
            db.execute_update(
                "UPDATE inventory SET current_stock = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (stock_after, item_id)
            )
            
            # 记录流水
            db.execute_update("""
                INSERT INTO inventory_transaction 
                (product_code, transaction_type, quantity, stock_before, stock_after, operator, reason, order_no)
                VALUES (%s, 'in', %s, %s, %s, %s, %s, %s)
            """, (item['product_code'], quantity, stock_before, stock_after, 'admin', reason, order_no))
            
            return jsonify({'success': True, 'message': f'入库成功 +{quantity}'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    item = db.execute_query("SELECT * FROM inventory WHERE id = %s", (item_id,), fetch='one')
    return render_template('inventory_transaction.html', title='入库', item=item, action='in')


@main.route('/inventory/<int:item_id>/out', methods=['GET', 'POST'])
def inventory_out(item_id):
    """出库操作"""
    from app.database import db
    
    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity'))
            reason = request.form.get('reason', '出库')
            order_no = request.form.get('order_no')
            
            if quantity <= 0:
                return jsonify({'success': False, 'error': '数量必须大于0'}), 400
            
            # 获取当前库存
            item = db.execute_query("SELECT * FROM inventory WHERE id = %s", (item_id,), fetch='one')
            if not item:
                return jsonify({'success': False, 'error': '产品不存在'}), 404
            
            if item['current_stock'] < quantity:
                return jsonify({'success': False, 'error': f'库存不足，当前库存: {item["current_stock"]}'}), 400
            
            stock_before = item['current_stock']
            stock_after = stock_before - quantity
            
            # 更新库存
            db.execute_update(
                "UPDATE inventory SET current_stock = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (stock_after, item_id)
            )
            
            # 检查是否需要预警
            if stock_after <= item['min_stock']:
                db.execute_update("""
                    INSERT INTO inventory_alert (product_code, alert_type, current_stock, threshold, remark)
                    VALUES (%s, 'low_stock', %s, %s, '库存低于最小值')
                """, (item['product_code'], stock_after, item['min_stock']))
            
            # 记录流水
            db.execute_update("""
                INSERT INTO inventory_transaction 
                (product_code, transaction_type, quantity, stock_before, stock_after, operator, reason, order_no)
                VALUES (%s, 'out', %s, %s, %s, %s, %s, %s)
            """, (item['product_code'], quantity, stock_before, stock_after, 'admin', reason, order_no))
            
            return jsonify({'success': True, 'message': f'出库成功 -{quantity}'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    item = db.execute_query("SELECT * FROM inventory WHERE id = %s", (item_id,), fetch='one')
    return render_template('inventory_transaction.html', title='出库', item=item, action='out')


@main.route('/inventory/<int:item_id>/edit', methods=['GET', 'POST'])
def inventory_edit(item_id):
    """编辑库存信息"""
    from app.database import db
    
    if request.method == 'POST':
        try:
            product_name = request.form.get('product_name')
            category = request.form.get('category')
            unit = request.form.get('unit', '件')
            min_stock = int(request.form.get('min_stock', 10))
            max_stock = int(request.form.get('max_stock', 1000))
            location = request.form.get('location')
            supplier = request.form.get('supplier')
            remark = request.form.get('remark')
            
            db.execute_update("""
                UPDATE inventory SET 
                    product_name = %s, category = %s, unit = %s,
                    min_stock = %s, max_stock = %s, location = %s,
                    supplier = %s, remark = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (product_name, category, unit, min_stock, max_stock, location, supplier, remark, item_id))
            
            return jsonify({'success': True, 'message': '更新成功'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    item = db.execute_query("SELECT * FROM inventory WHERE id = %s", (item_id,), fetch='one')
    if not item:
        return render_template('errors/404.html'), 404
    
    categories = db.execute_query("SELECT DISTINCT category FROM inventory WHERE category IS NOT NULL ORDER BY category", fetch='all')
    return render_template('inventory_form.html', title='编辑库存', item=item, categories=[c['category'] for c in (categories or [])])


@main.route('/inventory/transaction')
def inventory_transaction():
    """库存流水"""
    from app.database import db
    
    try:
        product_code = request.args.get('product_code', '').strip()
        transaction_type = request.args.get('type', '').strip()
        
        query = "SELECT * FROM inventory_transaction WHERE 1=1"
        params = []
        
        if product_code:
            query += " AND product_code = %s"
            params.append(product_code)
        
        if transaction_type:
            query += " AND transaction_type = %s"
            params.append(transaction_type)
        
        query += " ORDER BY created_at DESC LIMIT 100"
        
        transactions = db.execute_query(query, tuple(params) if params else None, fetch='all')
        
        return render_template('inventory_transaction_list.html',
                             title='库存流水',
                             transactions=transactions or [],
                             product_code=product_code,
                             transaction_type=transaction_type)
    except Exception as e:
        return render_template('inventory_transaction_list.html',
                             title='库存流水',
                             error=str(e),
                             transactions=[])

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

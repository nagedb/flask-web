"""
错误处理
"""
from flask import Blueprint, render_template, jsonify

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    """404 错误页面"""
    from flask import request
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('errors/404.html', title='页面未找到'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    """500 错误页面"""
    from flask import request
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('errors/500.html', title='服务器错误'), 500


@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    """403 错误页面"""
    from flask import request
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': 'Forbidden'}), 403
    return render_template('errors/403.html', title='禁止访问'), 403

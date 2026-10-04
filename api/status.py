from flask import Blueprint, render_template, jsonify
from api.sysinfo import collect_status

status_bp = Blueprint("status", __name__)


@status_bp.route("/")
def index():
    """主布局页面"""
    return render_template("index.html")


@status_bp.route("/pages/status")
def page_status():
    """iframe 内容：系统状态"""
    return render_template("status.html")


@status_bp.route("/api/status")
def api_status():
    """纯 JSON 接口"""
    return jsonify(collect_status())
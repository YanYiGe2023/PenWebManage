import json
import os
from flask import Blueprint, render_template, jsonify

tools_bp = Blueprint("tools", __name__)

SCAN_FILE = "/sys_data/fatfs/answer_word/scanWordRecord.json"


@tools_bp.route("/pages/tools")
def page_tools():
    return render_template("tools.html")


@tools_bp.route("/api/scan-history")
def api_scan_history():
    """读取扫描历史。文件不存在或格式错误时返回 supported=False"""
    if not os.path.exists(SCAN_FILE):
        return jsonify({
            "supported": False,
            "msg": "未检测到扫描记录文件，可能不是支持的设备",
            "path": SCAN_FILE,
        })

    try:
        with open(SCAN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return jsonify({
            "supported": False,
            "msg": f"读取失败: {e}",
            "path": SCAN_FILE,
        })

    en = data.get("en", [])
    cn = data.get("cn", [])

    return jsonify({
        "supported": True,
        "path": SCAN_FILE,
        "count": {"en": len(en), "cn": len(cn)},
        "en": en,
        "cn": cn,
    })
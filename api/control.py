import os
import sys
import signal
import threading
import time
from flask import Blueprint, jsonify

control_bp = Blueprint("control", __name__)


def _delay_shutdown():
    time.sleep(1)
    os.kill(os.getpid(), signal.SIGTERM)


def _delay_restart():
    time.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)


@control_bp.route("/shutdown", methods=["POST"])
def shutdown():
    threading.Thread(target=_delay_shutdown, daemon=True).start()
    return jsonify({"ok": True, "msg": "服务即将停止"})


@control_bp.route("/restart", methods=["POST"])
def restart():
    threading.Thread(target=_delay_restart, daemon=True).start()
    return jsonify({"ok": True, "msg": "服务即将重启"})
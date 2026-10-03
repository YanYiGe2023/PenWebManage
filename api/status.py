from flask import Blueprint, render_template
from api.sysinfo import collect_status

status_bp = Blueprint("status", __name__)


@status_bp.route("/")
def index():
    return render_template("status.html", **collect_status())
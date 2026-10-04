from flask import Blueprint, render_template

files_bp = Blueprint("files", __name__)


@files_bp.route("/pages/files")
def page_files():
    return render_template("files.html")
from flask import Flask
from api.status import status_bp
from api.control import control_bp
# 以后加新功能，只需再 import 一个蓝图

app = Flask(
    __name__,
    template_folder="www",
    static_folder="www/static",
)

app.register_blueprint(status_bp)
app.register_blueprint(control_bp)
# app.register_blueprint(tools_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
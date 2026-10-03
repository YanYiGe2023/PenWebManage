#!/bin/sh
# 设备端部署脚本：解压 penplus.tar.gz 并启动 app
# 用法：
#   sh deploy.sh              解压 + 启动
#   sh deploy.sh --no-start   只解压，不启动
#   sh deploy.sh nostart      同上（简写）

APP_DIR="/sys_data/penplus"
TAR_FILE="$APP_DIR/penplus.tar.gz"
PID_FILE="/tmp/penweb.pid"
LOG_FILE="/tmp/penweb.log"

# 解析参数
NO_START=0
case "$1" in
    --no-start|nostart|-n)
        NO_START=1
        ;;
    "")
        ;;
    *)
        echo "用法: $0 [--no-start|nostart]"
        exit 1
        ;;
esac

cd "$APP_DIR" || { echo "❌ 无法进入 $APP_DIR"; exit 1; }

# 1. 检查压缩包
if [ ! -f "$TAR_FILE" ]; then
    echo "❌ 找不到 $TAR_FILE"
    exit 1
fi

# 2. 停止旧进程（--no-start 时也停，避免解压时文件被占用）
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "🛑 停止旧进程 (PID: $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null
        sleep 1
        kill -9 "$OLD_PID" 2>/dev/null
    fi
    rm -f "$PID_FILE"
fi

# 兜底：扫一遍残留的 app.py 进程
pkill -f "python3 app.py" 2>/dev/null

# 3. 解压覆盖
echo "📂 解压 $TAR_FILE..."
tar -xzf "$TAR_FILE" -C "$APP_DIR"
if [ $? -ne 0 ]; then
    echo "❌ 解压失败"
    exit 1
fi
echo "✅ 解压完成"

# 4. 是否启动
if [ "$NO_START" -eq 1 ]; then
    echo "⏸  已跳过启动 (--no-start)"
    echo "   手动前台运行: cd $APP_DIR && /opt/bin/python3 app.py"
    echo "   手动后台运行: cd $APP_DIR && nohup /opt/bin/python3 app.py > $LOG_FILE 2>&1 &"
    exit 0
fi

echo "🚀 启动 app..."
nohup /opt/bin/python3 "$APP_DIR/app.py" > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

sleep 1
if kill -0 "$NEW_PID" 2>/dev/null; then
    echo "✅ 启动成功 (PID: $NEW_PID)"
    echo "   日志: $LOG_FILE"
    echo "   访问: http://<设备IP>:5000"
else
    echo "❌ 启动失败，请查看日志:"
    cat "$LOG_FILE"
    exit 1
fi
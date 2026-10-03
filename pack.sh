#!/bin/bash
# Mac 端打包脚本
set -e

cd "$(dirname "$0")"

TAR_NAME="penplus.tar.gz"

if [ ! -f "app.py" ]; then
    echo "❌ 当前目录没有 app.py"
    exit 1
fi

# 禁用 macOS 的 AppleDouble 元数据
export COPYFILE_DISABLE=1

echo "🧹 清理旧的压缩包..."
rm -f "$TAR_NAME"

echo "📦 打包项目文件..."
tar --exclude=".venv" \
    --exclude="venv" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".idea" \
    --exclude=".git" \
    --exclude=".DS_Store" \
    --exclude="__MACOSX" \
    --exclude="._*" \
    --exclude="$TAR_NAME" \
    --exclude="pack.sh" \
    --exclude="deploy.sh" \
    -czf "$TAR_NAME" .

echo ""
echo "✅ 打包完成: $(pwd)/$TAR_NAME"
ls -lh "$TAR_NAME"
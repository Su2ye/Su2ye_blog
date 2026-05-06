#!/bin/bash
# =============================================
# su2ye 博客部署脚本
# 宝塔面板终端中执行: bash deploy.sh
# =============================================

set -e

# 找到 Python 管理器安装的 Python 3
if [ -f /www/server/panel/pyenv/bin/python3 ]; then
    PYTHON=/www/server/panel/pyenv/bin/python3
    PIP=/www/server/panel/pyenv/bin/pip3
elif [ -f /usr/bin/python3 ]; then
    PYTHON=/usr/bin/python3
    PIP=/usr/bin/pip3
else
    echo "请先确认 Python 3 已安装"
    exit 1
fi

echo ">>> 使用 Python: $PYTHON"
echo ">>> 安装依赖..."
$PIP install -r requirements.txt

echo ">>> 生成数据库..."
$PYTHON manage.py makemigrations blog
$PYTHON manage.py migrate

echo ">>> 收集静态文件..."
$PYTHON manage.py collectstatic --noinput

echo ">>> 创建超级管理员..."
echo "请按提示设置管理员账号和密码："
$PYTHON manage.py createsuperuser

echo ">>> 部署完成！"

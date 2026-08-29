#!/bin/bash
# 多Agent协同看板 - 停止脚本
# 双击即可停止服务器

echo "正在停止服务器..."

if lsof -ti:8766 > /dev/null 2>&1; then
    lsof -ti:8766 | xargs kill -9
    echo "服务器已停止"
else
    echo "服务器未在运行"
fi

read -p "按回车键退出..."

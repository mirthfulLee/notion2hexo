#! /bin/bash
# 切换至本项目工作目录
cd "$(dirname "$0")"
# 选择conda 环境
conda activate your_pyenv
# 设置notion token
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 执行notion导出为markdown的脚本
python exporter.py
# 更新到 github blog 仓库
git add .
git commit -m "new post from notion $(date +%m-%d" "%H:%M)"
git push origin master
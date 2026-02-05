#!/bin/bash

# YouTube Influencer Analyzer - Quick GitHub Setup Script
# 快速上传到 GitHub 的脚本

echo "=========================================="
echo "YouTube Influencer Analyzer"
echo "GitHub 快速上传脚本"
echo "=========================================="
echo ""

# 检查是否已经安装 git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git:"
    echo "   macOS: brew install git"
    echo "   Ubuntu: sudo apt-get install git"
    exit 1
fi

# 询问 GitHub 用户名
read -p "请输入你的 GitHub 用户名: " github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub 用户名不能为空"
    exit 1
fi

echo ""
echo "📝 步骤说明："
echo "1. 请先在 GitHub 上创建仓库: https://github.com/new"
echo "   - Repository name: youtube-influencer-analyzer"
echo "   - 可以选择 Public 或 Private"
echo "   - 不要勾选 'Initialize this repository with a README'"
echo ""
read -p "已经创建好仓库了吗？(y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "请先创建仓库，然后重新运行此脚本"
    exit 0
fi

# 创建工作目录
WORK_DIR=~/github-projects/youtube-influencer-analyzer
echo ""
echo "📁 创建工作目录: $WORK_DIR"
mkdir -p ~/github-projects
cd ~/github-projects

# 如果目录已存在，先删除
if [ -d "youtube-influencer-analyzer" ]; then
    echo "⚠️  目录已存在，删除旧目录..."
    rm -rf youtube-influencer-analyzer
fi

# 初始化 Git 仓库
echo "🔧 初始化 Git 仓库..."
mkdir youtube-influencer-analyzer
cd youtube-influencer-analyzer
git init

# 复制文件
echo "📋 复制 skill 文件..."
cp -r ~/.claude/skills/youtube-influencer-analyzer/* .

# 创建 .gitignore
echo "📝 创建 .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test
test_output/
*.log
EOF

# 添加文件
echo "➕ 添加文件到 Git..."
git add .

# 提交
echo "💾 创建初始提交..."
git commit -m "Initial commit: YouTube Influencer Analyzer skill

Features:
- Automatic extraction of YouTube channel data
- Subscriber count and view statistics
- Update frequency analysis
- HappyCapy collaboration fit evaluation
- CSV export for business proposals
- Support for AI tools, learning/productivity, side hustle, and developer content categories"

# 添加远程仓库
echo "🔗 添加远程仓库..."
git branch -M main
git remote add origin https://github.com/$github_username/youtube-influencer-analyzer.git

# 推送
echo ""
echo "🚀 推送到 GitHub..."
echo "⚠️  如果提示需要认证，请使用 Personal Access Token"
echo "   获取 Token: https://github.com/settings/tokens"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 上传成功！"
    echo "=========================================="
    echo ""
    echo "📦 你的仓库地址："
    echo "   https://github.com/$github_username/youtube-influencer-analyzer"
    echo ""
    echo "🎉 现在可以分享你的 skill 了！"
    echo ""
    echo "📚 其他人可以这样安装："
    echo "   git clone https://github.com/$github_username/youtube-influencer-analyzer.git"
    echo "   cp -r youtube-influencer-analyzer ~/.claude/skills/"
    echo ""
    echo "🔄 以后更新只需运行："
    echo "   cd $WORK_DIR"
    echo "   cp -r ~/.claude/skills/youtube-influencer-analyzer/* ."
    echo "   git add ."
    echo "   git commit -m '更新说明'"
    echo "   git push"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo "请检查："
    echo "1. GitHub 仓库是否已创建"
    echo "2. 网络连接是否正常"
    echo "3. Git 认证是否配置正确"
    echo ""
    echo "手动推送命令："
    echo "   cd $WORK_DIR"
    echo "   git push -u origin main"
fi

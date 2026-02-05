# GitHub 上传指南

完整教程：如何将 YouTube Influencer Analyzer Skill 上传到 GitHub

## 准备工作

### 1. 安装 Git（如果还没安装）

**macOS:**
```bash
brew install git
```

**Ubuntu/Debian:**
```bash
sudo apt-get install git
```

**Windows:**
下载并安装：https://git-scm.com/download/win

### 2. 配置 Git

首次使用需要配置用户信息：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

## 上传步骤

### 步骤一：在 GitHub 上创建新仓库

1. 登录 GitHub (https://github.com)
2. 点击右上角的 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `youtube-influencer-analyzer`
   - **Description**: `YouTube博主分析工具，自动提取数据生成合作表单 | YouTube Influencer Analyzer for Collaboration Assessment`
   - **Public** 或 **Private**（选择公开或私有）
   - ✅ **勾选** "Add a README file"
   - **Add .gitignore**: 选择 "Python"
   - **Choose a license**: 选择 "MIT License"（推荐）
4. 点击 "Create repository"

### 步骤二：将 Skill 文件复制到本地目录

```bash
# 创建工作目录
mkdir -p ~/github-projects
cd ~/github-projects

# 克隆刚创建的仓库
git clone https://github.com/你的用户名/youtube-influencer-analyzer.git

# 进入目录
cd youtube-influencer-analyzer

# 复制 skill 文件
cp -r ~/.claude/skills/youtube-influencer-analyzer/* .

# 查看文件
ls -la
```

你应该看到：
- `SKILL.md`
- `analyze_channel.py`
- `README.md`
- `GITHUB_UPLOAD_GUIDE.md`

### 步骤三：提交并推送到 GitHub

```bash
# 添加所有文件到 Git
git add .

# 查看将要提交的文件
git status

# 提交更改
git commit -m "Initial commit: YouTube Influencer Analyzer skill

- Added SKILL.md with AI instructions
- Added analyze_channel.py with data extraction logic
- Added README.md with usage documentation
- Added HappyCapy collaboration fit evaluation
- Supports subscriber count, view statistics, and update frequency analysis"

# 推送到 GitHub
git push origin main
```

如果提示需要认证：
- **使用 Personal Access Token（推荐）**
  1. 访问 https://github.com/settings/tokens
  2. 点击 "Generate new token (classic)"
  3. 勾选 "repo" 权限
  4. 生成并复制 token
  5. 在命令行输入 token 作为密码

### 步骤四：验证上传成功

访问你的 GitHub 仓库：
```
https://github.com/你的用户名/youtube-influencer-analyzer
```

你应该看到所有文件已经上传成功！

## 后续更新

当你修改了 skill 文件后，使用以下命令更新到 GitHub：

```bash
# 进入仓库目录
cd ~/github-projects/youtube-influencer-analyzer

# 从 skill 目录复制最新文件
cp -r ~/.claude/skills/youtube-influencer-analyzer/* .

# 查看更改
git status

# 添加更改
git add .

# 提交更改
git commit -m "更新说明：描述你做了什么修改"

# 推送到 GitHub
git push origin main
```

## 快捷脚本

创建一个更新脚本方便以后使用：

```bash
# 创建更新脚本
cat > ~/update-youtube-analyzer.sh << 'EOF'
#!/bin/bash
echo "正在更新 YouTube Influencer Analyzer 到 GitHub..."

cd ~/github-projects/youtube-influencer-analyzer
cp -r ~/.claude/skills/youtube-influencer-analyzer/* .

git add .
git status

read -p "输入提交说明: " commit_msg
git commit -m "$commit_msg"
git push origin main

echo "更新完成！"
EOF

# 添加执行权限
chmod +x ~/update-youtube-analyzer.sh

# 以后只需运行：
~/update-youtube-analyzer.sh
```

## 从 GitHub 安装 Skill

其他人可以这样安装你的 skill：

```bash
# 克隆仓库
git clone https://github.com/你的用户名/youtube-influencer-analyzer.git

# 复制到 Claude skills 目录
cp -r youtube-influencer-analyzer ~/.claude/skills/

# 给脚本添加执行权限
chmod +x ~/.claude/skills/youtube-influencer-analyzer/analyze_channel.py

# 完成！重启 Claude Code 即可使用
```

## 添加 GitHub Badges（可选）

在 README.md 顶部添加漂亮的徽章：

```markdown
# YouTube Influencer Analyzer Skill

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)

专业的 YouTube 博主分析工具...
```

## 常见问题

### Q: 推送时提示 "Permission denied"
A: 需要设置 SSH key 或使用 Personal Access Token

### Q: 如何设置 SSH key？
A:
```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 访问 https://github.com/settings/ssh/new 添加公钥
```

### Q: 如何让仓库更容易被发现？
A: 在 GitHub 仓库页面添加 Topics：
- `claude-code`
- `youtube-analyzer`
- `influencer-marketing`
- `python`
- `data-analysis`

### Q: 如何创建 Release？
A:
1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本号（如 v1.0.0）和说明
4. 点击 "Publish release"

## 进阶：添加 GitHub Actions

自动测试和发布（可选）：

创建 `.github/workflows/test.yml`：

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Test script
        run: |
          python analyze_channel.py https://www.youtube.com/@MoeLueker
```

## 分享你的 Skill

上传后，你可以：
1. 在 Claude Code 社区分享链接
2. 提交到 awesome-claude-skills 列表
3. 在社交媒体分享
4. 写一篇博客介绍你的 skill

祝你 GitHub 之旅愉快！🎉

# YouTube Influencer Analyzer Skill

专业的 YouTube 博主分析工具，自动提取频道数据并生成详细的合作提案表单。

## 功能特点

- 自动提取订阅者数量（Subscriber Count）
- 分析最近5条视频的观看数据
- 计算平均观看量
- 判断更新频率（3天/条、7天+/条、14天+/条、4-7天/条）
- 识别AI/技术相关内容
- 计算粉丝互动率（观看数/订阅数比例）
- 生成完整的合作表单填写建议

## 使用方法

### 方式一：直接调用 skill

在 Claude Code 中使用：

```
分析这个 YouTube 频道：https://www.youtube.com/@MoeLueker
```

或者：

```
帮我分析 YouTube 博主 @MoeLueker 并生成合作表单
```

### 方式二：使用 Python 脚本

在命令行直接运行：

```bash
python3 ~/.claude/skills/youtube-influencer-analyzer/analyze_channel.py https://www.youtube.com/@MoeLueker
```

输出 JSON 格式：

```bash
python3 ~/.claude/skills/youtube-influencer-analyzer/analyze_channel.py https://www.youtube.com/@MoeLueker --json
```

## 输出内容

该 skill 会生成以下完整信息：

### 基础数据
- 达人名称
- YouTube ID
- 频道主页链接
- Follower数量（订阅者）
- 近五条平均观看量

### 内容分析
- 更新频率
- 是否提及AI/Claude Code相关话题
- 是否有Instagram账号
- 内容风格分类
- 受众群体分析

### 商务评估
- 详细评论（包含内容特点、爆款视频、互动率等）
- 联系方式建议
- 合作价值评估
- 优先级推荐

### 数据洞察
- 粉丝活跃度分析
- 爆款视频识别
- 内容相关度评分
- 受众匹配度评估

## 表单字段对应

该 skill 的输出直接对应以下表单字段：

| 表单字段 | 对应数据 |
|---------|---------|
| 达人名称 | 从频道名称提取 |
| Youtube ID | 频道 @ 标识 |
| Youtube 主页 | 完整频道 URL |
| Follower数量 | 订阅者数（数字格式） |
| 近五条平均观看量 | 最新5条视频平均观看数 |
| 更新频率 | 3天/条、7天+/条、14天+/条、4-7天/条 |
| 是否提及相关话题 | AI/Claude Code 相关内容检测 |
| 是否有IG | Instagram 账号检测 |
| Comment | 综合分析评论 |
| 内容风格 | 教程型、评测型等 |
| 受众风格 | 目标受众描述 |

## 技术实现

### 数据来源
- YouTube 频道主页（订阅者数据）
- YouTube /videos 页面（视频列表和观看数）
- YouTube /about 页面（联系方式和社交媒体）

### 数据提取方法
- 使用 Python urllib 发送 HTTP 请求
- 正则表达式解析 ytInitialData JSON 数据
- 智能解析数字（K、M、B 后缀）
- 时间间隔计算（days/weeks/months ago）

### 频率判断逻辑
```
最近3条视频间隔：
- 0-3天 → 3天/条
- 4-7天 → 4-7天/条
- 8-14天 → 7天+/条
- 15天+ → 14天+/条
```

### AI内容识别
检测关键词：ai, gpt, claude, machine learning, automation, 等

阈值：60% 以上视频包含相关关键词即判定为 AI 相关

## 示例输出

```
======================================================================
YouTube Channel Analysis Report
======================================================================

Channel: @MoeLueker
URL: https://www.youtube.com/@MoeLueker

METRICS:
- Subscribers: 35.9K (35,900)
- Average Views (Recent 5): 32,218
- Update Frequency: 3天/条
- AI/Tech Related: Yes ✓

RECENT VIDEOS:

1. Grok AI Video Generator Tutorial
   Views: 1,960 (1,960 views)
   Published: 3 days ago

2. Make Epic AI Videos in 10 Minutes
   Views: 1,036 (1,036 views)
   Published: 6 days ago

[...]

======================================================================
KEY INSIGHTS:
- Engagement Rate: 89.7% (views/subscribers)
- Content Focus: AI/Tech Tools
- Publishing Consistency: 3天/条
```

## 注意事项

1. **YouTube 限制**：YouTube 可能会对频繁请求进行限制，建议合理使用
2. **数据准确性**：数据来自公开页面，某些信息（如联系邮箱）可能不公开
3. **时效性**：YouTube 页面结构可能变化，如遇问题请更新脚本
4. **网络要求**：需要能够访问 YouTube 的网络环境

## 更新日志

### v1.0.0 (2025-02-05)
- 初始版本发布
- 支持订阅者、观看量、更新频率分析
- 支持 AI 内容识别
- 生成完整合作表单建议

## 贡献

如需改进此 skill，请：
1. 修改 `SKILL.md` 调整分析逻辑
2. 修改 `analyze_channel.py` 优化数据提取
3. 更新 `README.md` 文档

## 许可

本 skill 为 Claude Code 社区开源项目，可自由使用和修改。

# Vibe Integrity

[English](./README.md)

Vibe Integrity 是专为 AI 辅助开发设计的 **AI 项目记忆与安全系统**。 它可以防止 AI 虚假声称完成,并提供结构化的项目知识供 AI 快速理解。

## 概述

Vibe Integrity 解决了 AI 辅助开发中的两个关键问题：

1. **完成守卫** - 检测 AI 是否虚假声称工作已完成
2. **架构记忆** - 结构化的项目知识供 AI 快速理解

## 快速开始

```bash
# 初始化项目
vic init --name "My Project" --tech "Node.js,Vue,PostgreSQL"

# 记录技术决策
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# 验证
vic validate

# 查看状态
vic status
```

## 命令

| 命令 | 别名 | 描述 |
|------|------|------|
| `vic init` | - | 初始化 .vibe-integrity/ |
| `vic rt` | `record-tech` | 记录技术决策 |
| `vic rr` | `record-risk` | 记录风险 |
| `vic rd` | `record-dep` | 记录依赖 |
| `vic check` | - | 检查代码对齐 |
| `vic validate` | - | 完整验证 |
| `vic status` | - | 查看项目状态 |
| `vic search` | - | 搜索记录 |
| `vic history` | - | 查看历史 |
| `vic export` | - | 导出数据 |
| `vic import` | - | 导入数据 |

完整文档：[cmd/vic/README_cn.md](./cmd/vic/README_cn.md)

## 目录结构

```
D:\Code\aaa\
├── cmd/
│   └── vic/                    # CLI 工具
│       ├── vic                 # 主程序
│       ├── README.md           # 英文文档
│       └── README_cn.md        # 中文文档
│
├── skills-base/                # Skills 定义
│   ├── vibe-integrity/         # 核心记忆系统
│   ├── vibe-think/             # 思考澄清
│   └── vibe-debug/             # 调试方法论
│
├── .vibe-integrity/            # 项目数据
│   ├── project.yaml
│   ├── tech-records.yaml
│   ├── risk-zones.yaml
│   ├── dependency-graph.yaml
│   ├── events.yaml
│   └── state.yaml
│
├── docs/                       # 设计文档
│
├── .pre-commit-config.yaml
└── requirements.txt
```

## 核心文件

| 文件 | 目的 |
|------|------|
| `project.yaml` | 项目元信息,技术栈 |
| `tech-records.yaml` | 技术决策记录 |
| `risk-zones.yaml` | 高风险区域 |
| `dependency-graph.yaml` | 模块依赖关系 |
| `events.yaml` | 事件历史 (追加) |
| `state.yaml` | 当前状态 (自动生成) |

## AI 快速开始

当 AI 开始在这个项目上工作时,请按此顺序阅读:

```
1. .vibe-integrity/project.yaml    → 项目状态,技术栈
2. .vibe-integrity/risk-zones.yaml → 高风险区域
3. .vibe-integrity/tech-records.yaml → 理解系统为何如此设计
```

**结果**: AI 能在大约 15 秒内理解项目。

## 典型工作流

### 开始新项目
```bash
vic init --name "My App" --tech "React,Node,PostgreSQL"
```

### 做技术决策时
```bash
vic rt --id FE-001 --title "Use React Query" --decision "Data fetching" --reason "Caching"
```

### 发现风险时
```bash
vic rr --id RISK-001 --area payment --desc "No idempotency key" --impact high
```

### AI 说"完成了"时
```bash
vic check
```

### 提交代码前
```bash
vic validate
```

### 备份/迁移项目记忆
```bash
vic export -o backup.json
# 在新项目中
vic import backup.json
```

## 相关 Skills

| Skill | 用途 |
|------|------|
| `vibe-integrity` | 项目记忆与验证 |
| `vibe-think` | 需求澄清、增强提问 |
| `vibe-debug` | 系统性调试方法论 |

## 安装

```bash
# 依赖
pip install pyyaml filelock

# Linux/macOS - 添加到 PATH
chmod +x cmd/vic/vic
sudo ln -s $(pwd)/cmd/vic/vic /usr/local/bin/vic

# Windows PowerShell
Set-Alias vic "python D:\Code\aaa\cmd\vic\vic"
```

## 许可证

MIT License

# VIBE-SDD

[English](./README.md)

VIBE-SDD 是一个结合了结构化 SDD (Spec-Driven Development) 与灵活 Vibe Coding 的**Vibe 驱动软件开发系统**。它为 AI 辅助开发提供了完整的流程，包含规范的检查点和文档管理。

## 概述

VIBE-SDD 解决了 AI 辅助开发中的三个关键问题：

1. **规范** - 结构化的需求和架构文档
2. **门禁** - 推进前的质量检查点
3. **记忆** - 项目知识供 AI 快速理解

## 快速开始

```bash
# 初始化项目
vic init --name "My Project" --tech "React,Node,PostgreSQL"

# 运行 Gate 检查（阻止提交直到通过）
vic spec gate 0  # 需求完整性
vic spec gate 1  # 架构完整性
vic spec gate 2  # 代码对齐
vic spec gate 3  # 测试覆盖

# 推进阶段（自动运行 Gate 检查）
vic phase advance --to 1

# 记录决策
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database"
vic rr --id RISK-001 --area auth --desc "JWT not validated"
```

## 命令

| 命令 | 描述 |
|------|------|
| `vic init` | 初始化 .vic-sdd/ |
| `vic spec init` | 初始化 SPEC 文档 |
| `vic spec status` | 查看 SPEC 状态 |
| `vic spec gate [0-3]` | 运行 Gate 检查（验证） |
| `vic spec hash` | 检查 SPEC Hash 并检测变更 |
| `vic phase advance` | 推进阶段（自动验证 gates） |
| `vic gate check --blocking` | Pre-commit 钩子检查 |
| `vic rt` | 记录技术决策 |
| `vic rr` | 记录风险 |
| `vic check` | 检查代码对齐 |
| `vic validate` | 完整验证 |

完整文档：[cmd/vic-go/README.md](./cmd/vic-go/README.md)

## 开发流程

```
定图纸 (需求)              打地基 (架构)              立规矩 (实现)
     │                         │                        │
requirements           architecture           sdd-orchestrator
     │                         │                        │
     ▼                         ▼                        ▼
SPEC-REQUIREMENTS.md ─▶ SPEC-ARCHITECTURE.md ─▶ 实现代码
     │                         │                        │
     ▼                         ▼                        ▼
    Gate 0                  Gate 1                  Gate 2 + 3
 (需求完整)              (架构完整)              (代码 + 测试)
```

## 目录结构

```
project/
├── cmd/vic-go/                 # Go CLI（编译后更快）
│   ├── internal/
│   │   └── commands/          # Gate 实现
│   │       ├── gate0.go       # 需求验证
│   │       ├── gate1.go       # 架构验证
│   │       ├── gate2.go       # 代码对齐检查
│   │       ├── gate3.go       # 测试覆盖检查
│   │       └── ...
│   └── README.md
│
├── skills/                     # 10 个核心 skills（从 19 精简）
│   ├── constitution-check/     # 合规检查（新增）
│   ├── context-tracker/       # 自我认知（4→1）
│   ├── requirements/           # 需求分析（2→1）
│   ├── architecture/           # 技术架构
│   ├── design-review/          # 设计系统
│   ├── debugging/             # 调试（2→1）
│   ├── qa/                     # 测试（3→1）
│   ├── sdd-orchestrator/       # SDD 流水线
│   ├── spec-architect/         # 规范合约
│   ├── spec-contract-diff/     # 漂移检测
│   └── spec-traceability/      # 追溯追踪
│
├── docs/                       # 文档
├── .vic-sdd/                  # 项目记忆
│   ├── SPEC-REQUIREMENTS.md    # 需求规范
│   ├── SPEC-ARCHITECTURE.md    # 架构规范
│   ├── PROJECT.md              # 项目状态
│   ├── agent-prompt.md        # AI 工作流提示
│   └── context.yaml            # 统一上下文
└── .pre-commit-config.yaml     # Gate 强制执行
```

## 核心理念

### 定图纸 (需求)
- 定义用户故事和验收标准
- 规划开发阶段
- 创建 SPEC-REQUIREMENTS.md

### 打地基 (架构)
- 评估技术选型
- 设计系统架构
- 创建 SPEC-ARCHITECTURE.md

### 立规矩 (实现)
- 小步迭代
- 门禁检查推进
- 收敛到 PRD/ARCH/PROJECT

### 自我认知 (Self-Awareness)
VIBE-SDD 通过统一上下文追踪赋予 AI"自知之明"：
- **Context Tracker** — 知道/推断/假设/不知 + 信号 + 信心度

## AI 快速开始

当 AI 在这个项目上开始工作时，请按以下顺序阅读：

```
1. .vic-sdd/agent-prompt.md      → 工作流概览（会话开始时显示）
2. .vic-sdd/PROJECT.md            → 项目状态、里程碑
3. .vic-sdd/SPEC-REQUIREMENTS.md → 需求、验收标准
4. .vic-sdd/SPEC-ARCHITECTURE.md → 架构、技术栈
```

**结果**: AI 能在约 15 秒内理解项目上下文。

## Skills 参考（10 个核心 Skills）

| 类别 | Skill | 用途 |
|------|-------|------|
| 自我认知 | `context-tracker` | 统一：知道/推断/假设/不知 + 信号 |
| Vibe | `requirements` | 用户故事、验收标准 |
| Vibe | `architecture` | 技术选型、系统设计 |
| Vibe | `design-review` | 设计系统、AI Slop 检测 |
| Vibe | `debugging` | 根因分析 (SURVEY→PATTERN→HYPOTHESIS→IMPLEMENT) |
| QA | `qa` | TDD、测试覆盖、E2E |
| SDD | `sdd-orchestrator` | 状态机、Gate 执行 |
| SDD | `spec-architect` | 将需求凝固为合约 |
| SDD | `spec-contract-diff` | 检测规范漂移 |
| SDD | `spec-traceability` | 故事→合约→代码→测试追溯 |

## Gate 强制执行

### 自动 Gate 检查

```bash
# 声称"完成"前运行
vic spec gate 0   # 验证 SPEC-REQUIREMENTS.md 结构
vic spec gate 1   # 验证 SPEC-ARCHITECTURE.md 结构
vic spec gate 2   # 检查代码与规范对齐
vic spec gate 3   # 验证测试覆盖
```

### Pre-commit 钩子

`.pre-commit-config.yaml` 包含 `vic gate check --blocking`，在 Gate 通过前阻止提交。

### 阶段推进

```bash
vic phase advance --to 1  # 先自动运行所有必需的 Gate
```

## 典型工作流

| 场景 | 命令 |
|------|------|
| 开始新项目 | `vic init` |
| 检查需求 | `vic spec gate 0` |
| 检查架构 | `vic spec gate 1` |
| 检查代码对齐 | `vic spec gate 2` |
| 检查测试覆盖 | `vic spec gate 3` |
| 推进阶段 | `vic phase advance --to N` |
| Pre-commit 检查 | `vic gate check --blocking` |

## 安装

```bash
# 从源码构建
cd cmd/vic-go
make build

# 添加到 PATH
sudo ln -s $(pwd)/vic /usr/local/bin/vic

# 或者使用 Go
go install github.com/vic-sdd/vic@latest
```

## 许可证

MIT License. See [LICENSE](./LICENSE).

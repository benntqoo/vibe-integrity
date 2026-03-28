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

# 语义搜索（需要 embedding 支持）
vic ask "认证系统是如何工作的？"
```

## 命令

| 命令 | 描述 |
|------|------|
| `vic init` | 初始化 .vic-sdd/ |
| `vic status` | 显示项目状态 |
| `vic spec init` | 初始化 SPEC 文档 |
| `vic spec status` | 查看 SPEC 状态 |
| `vic spec gate [0-3]` | 运行 Gate 检查（验证） |
| `vic spec hash` | 检查 SPEC Hash 并检测变更 |
| `vic spec diff` | 检测自上次检查以来的 SPEC 变更 |
| `vic phase advance` | 推进阶段（自动验证 gates） |
| `vic gate check --blocking` | Pre-commit 钩子检查 |
| `vic rt` / `vic record tech` | 记录技术决策 |
| `vic rr` / `vic record risk` | 记录风险 |
| `vic check` | 检查代码对齐 |
| `vic validate` | 完整验证 |
| `vic ask <查询>` | 代码库语义搜索 |

完整文档：[docs/VIC-CLI-GUIDE.md](./docs/VIC-CLI-GUIDE.md)

## 开发流程

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
    │         │            │             │        │          │
    └─────────┴────────────┘             └────────┴──────────┘
         spec-workflow                        implementation
                                              unified-workflow
```

### 5 个核心 Skills

| Skill | 自动激活 | 职责 |
|-------|----------|------|
| `context-tracker` | ✅ 是 | AI 自我认知、信心度追踪 |
| `spec-workflow` | 否 | 需求分析 → 架构设计 → SPEC 冻结 |
| `implementation` | 否 | 代码/调试/测试/SPEC 对齐 |
| `unified-workflow` | 否 | SDD 编排/宪法规则/追溯 |
| `quick` | 否 | 简单单文件变更 |

## 目录结构

```
project/
├── cmd/vic-go/                 # Go CLI（编译后更快）
│   ├── main.go
│   └── internal/
│       ├── commands/           # CLI 命令实现
│       │   ├── root.go
│       │   ├── spec.go
│       │   ├── gate.go
│       │   ├── gate0-3.go      # Gate 实现
│       │   └── ...
│       ├── config/             # 配置管理 (Viper)
│       ├── checker/            # 代码对齐检查
│       ├── types/              # 类型定义
│       └── embedding/          # 语义搜索
│           ├── store.go        # SQLite 向量存储
│           ├── embedder.go     # 嵌入生成
│           └── chunker/        # 代码分块
│
├── skills/                     # 5 个核心 skills
│   ├── context-tracker/        # 自我认知（自动激活）
│   ├── spec-workflow/          # 需求/架构/SPEC
│   ├── implementation/         # 代码/调试/测试
│   ├── unified-workflow/       # SDD 编排
│   └── quick/                  # 简单变更
│
├── docs/                       # 文档
│   ├── VIC-CLI-GUIDE.md        # CLI 参考
│   ├── SDD-PROCESS-CN.md       # SDD 流程规范
│   └── ...
│
├── .vic-sdd/                   # 项目记忆
│   ├── SPEC-REQUIREMENTS.md    # 需求规范
│   ├── SPEC-ARCHITECTURE.md    # 架构规范
│   ├── PROJECT.md              # 项目状态
│   ├── constitution.yaml       # 不可违反规则
│   ├── context.yaml            # AI 自我认知状态
│   ├── agent-prompt.md         # AI 工作流提示
│   └── status/
│       ├── spec-hash.json      # SPEC 文件哈希
│       ├── gate-status.yaml    # Gate 检查状态
│       └── state.yaml          # 系统状态
│
└── .pre-commit-config.yaml     # Gate 强制执行
```

## 核心概念

### SDD 状态机

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
              │              │              │        │
        spec-workflow     implementation    unified-workflow
```

### 4 个 Gate

| Gate | 名称 | 检查内容 |
|------|------|---------|
| Gate 0 | 需求完整性 | SPEC-REQUIREMENTS.md 完整性 |
| Gate 1 | 架构完整性 | SPEC-ARCHITECTURE.md 完整性 |
| Gate 2 | 代码对齐 | 代码与 SPEC 一致性 |
| Gate 3 | 测试覆盖 | 测试覆盖率验证 |

### 宪法规则

定义在 `.vic-sdd/constitution.yaml`：

| 规则 | 描述 |
|------|------|
| `SPEC-FIRST` | 更改功能时先更新 SPEC |
| `SPEC-ALIGNED` | 代码必须匹配 SPEC |
| `GATE-BEFORE-COMMIT` | 提交前必须通过所有 Gate |
| `NO-TODO-IN-CODE` | 禁止 TODO/FIXME 注释 |
| `NO-CONSOLE-IN-PROD` | 禁止生产环境 console.log |
| `TESTS-REQUIRED` | 新功能必须有测试 |

## AI 快速开始

当 AI 在这个项目上开始工作时，请按以下顺序阅读：

```
1. AGENTS.md                  → 入口点，Skills 概览
2. .vic-sdd/PROJECT.md        → 项目状态、里程碑
3. .vic-sdd/SPEC-REQUIREMENTS.md → 需求、验收标准
4. .vic-sdd/SPEC-ARCHITECTURE.md → 架构、技术栈
```

**结果**: AI 能在约 15 秒内理解项目上下文。

## Pre-commit 钩子

配置在 `.pre-commit-config.yaml`：

```bash
pre-commit install
pre-commit run --all-files
```

包含的钩子：
- `vic-gate-check`: 在 Gate 通过前阻止提交
- `vic-spec-drift`: 检测代码与 SPEC 的漂移

## 安装

```bash
# 从源码构建
cd cmd/vic-go
make build

# 安装到 PATH
make install

# 直接运行
make run ARGS="--help"
```

## 构建命令

```bash
cd cmd/vic-go

# 构建当前平台
make build

# 构建所有平台
make build-all

# 运行测试
make test

# 安装到 PATH
make install

# 带参数运行
make run ARGS="--help"
```

## 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `VIC_DIR` | `.vic-sdd` | VIC 目录名 |
| `VIC_PROJECT_DIR` | 当前目录 | 项目目录 |
| `VIC_OUTPUT` | `plain` | 输出格式 (json/yaml/plain) |
| `VIC_VERBOSE` | `false` | 详细输出 |

## 许可证

MIT License. See [LICENSE](./LICENSE).

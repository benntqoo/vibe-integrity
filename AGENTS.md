# VIBE-SDD Agent Collaboration Guide

> **简化版** — 详细说明见各 SKILL.md

## 系统状态

| 特性 | 状态 |
|------|------|
| 多Agent支持 | ✅ Git分支工作流 |
| 结构化开发 | ✅ .vic-sdd/ SPEC工作流 |
| AI自我认知 | ✅ context-tracker |
| Gate检查 | ✅ vic spec gate 0-3 |

## 技能一览 (10个核心)

| 类别 | 技能 | 何时用 |
|------|------|--------|
| **合规检查** | `constitution-check` | 计划/审查/提交前必检 |
| **自我认知** | `context-tracker` | 任务开始/每个动作后/结束 |
| **需求** | `requirements` | 需求模糊，需要澄清 |
| **架构** | `architecture` | 需要技术选型 |
| **设计** | `design-review` | UI/UX设计 |
| **调试** | `debugging` | Bug修复 |
| **测试** | `qa` | 测试/TDD |
| **编排** | `sdd-orchestrator` | SDD状态机入口 |
| **规范** | `spec-architect` | 需求冻结为合约 |
| **差异** | `spec-contract-diff` | 检测代码与合约漂移 |
| **追溯** | `spec-traceability` | 需求→代码→测试链路 |

---

## 决策树：何时用哪个技能？

```
你的任务是什么？
│
├─ 🤔 需求不清晰 → requirements
│
├─ 🏗️ 技术选型/架构 → architecture
│
├─ 🎨 UI设计/AI风格检测 → design-review
│
├─ 🐛 Bug修复 → debugging
│
├─ 🧪 测试/红绿重构 → qa
│
├─ 📋 跨模块/多文件改动 → sdd-orchestrator (进入SDD流程)
│   │
│   ├─ 需求模糊 → spec-architect
│   ├─ 实现完成 → spec-contract-diff
│   └─ 测试完成 → spec-traceability
│
└─ 🚀 简单单文件改动 → 直接做！
```

---

## 开发流程

### SDD vs TDD 选择

```
你的任务涉及：
├─ 跨模块接口/API/合约？ → SDD流程 (sdd-orchestrator)
│
└─ 单模块内部逻辑？ → TDD流程 (qa)
```

### SDD 状态机

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
    │         │            │             │        │          │            │
    ▼         ▼            ▼             ▼        ▼          ▼            ▼
spec-   spec-         spec-       spec-    spec-      sdd-        
architect architect   to-codebase contract- driven-   release-
                     (SDD内部)     diff      test      guard
```

### SDD 技能路由

| 当前状态 | 调用技能 | 目的 |
|---------|---------|------|
| Ideation/Explore | `spec-architect` | 创建规范和合约 |
| SpecCheckpoint | `spec-to-codebase` | 生成实现 |
| Build | `spec-contract-diff` | 检测漂移 |
| Build/Verify | `spec-driven-test` | 运行验证测试 |
| Verify | `sdd-release-guard` | 最终发布门控 |

---

## 快速命令

```bash
# 初始化
vic init
vic spec init

# Gate 检查
vic spec gate 0    # 需求完整性
vic spec gate 1    # 架构完整性
vic spec gate 2    # 代码对齐
vic spec gate 3    # 测试覆盖

# 记录决策
vic rt --id DB-001 --title "选择PostgreSQL" --decision "主数据库"
vic rr --id RISK-001 --area auth --desc "JWT未验证"
```

---

## 质量红线

详见 `skills/context-tracker/SKILL.md`

| 红线 | 说明 |
|------|------|
| `no_todo_in_code` | 代码里不能有 TODO/FIXME |
| `no_console_in_prod` | 生产代码不能有 console.log |
| `no_hardcoded_secrets` | 不能有硬编码密钥 |
| `tests_required` | 新功能必须有测试 |
| `spec_aligned` | 必须与 SPEC 对齐 |

---

## 信心度

详见 `skills/context-tracker/SKILL.md`

```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals

> 0.7    → 🟢 HIGH   → 继续
0.4-0.7 → 🟡 MODERATE → 继续，关注警告
< 0.4   → 🔴 LOW   → 暂停，解决阻塞
blockers >= 2 → 🛑 STOP → 停止，等待人类
```

---

## 目录结构

```
.vic-sdd/
├── SPEC-REQUIREMENTS.md    # 需求规范
├── SPEC-ARCHITECTURE.md    # 架构规范
├── PROJECT.md              # 项目状态
├── agent-prompt.md        # AI工作流提示（含强制确认清单）
├── agent-card.yaml        # A2A Agent Card (多Agent协作)
├── context.yaml           # 统一上下文 (合并4个YAML)
├── constitution.yaml       # 不可违反规则清单（Constitution）
│
├── status/
│   ├── events.yaml         # 事件历史
│   ├── state.yaml          # 当前状态
│   └── spec-hash.json      # SPEC文件Hash追踪
├── tech/
│   └── tech-records.yaml  # 技术决策
├── risk-zones.yaml         # 风险区域
└── dependency-graph.yaml  # 模块依赖

skills/                    # 11个核心技能 (Google Cloud Agent Skills 规范)
├── registry.yaml          # Skill Registry (能力发现注册表)
├── _template/             # Skill 标准模板
│   └── SKILL.md
├── constitution-check/    # 合规检查 (critical)
│   ├── SKILL.md          # L1 + L2 指令
│   └── references/       # L3 按需资源
├── context-tracker/       # 自我认知 (critical, auto_activate)
│   ├── SKILL.md
│   └── references/
├── requirements/          # 需求分析 (high)
│   ├── SKILL.md
│   └── references/
├── architecture/          # 架构设计 (high)
│   ├── SKILL.md
│   └── references/
├── design-review/         # 设计审查 (medium)
│   ├── SKILL.md
│   └── references/
├── debugging/             # 调试 (high)
│   ├── SKILL.md
│   └── references/
├── qa/                     # 测试 (high)
│   ├── SKILL.md
│   └── references/
├── sdd-orchestrator/      # SDD编排 (critical)
│   ├── SKILL.md
│   └── references/
├── spec-architect/         # 规范编写 (high)
│   ├── SKILL.md
│   └── references/
├── spec-contract-diff/    # 差异检测 (high)
│   ├── SKILL.md
│   └── references/
└── spec-traceability/     # 追溯追踪 (medium)
    ├── SKILL.md
    └── references/

cmd/vic-go/               # vic CLI
```

---

## 详细文档索引

| 主题 | 文档 |
|------|------|
| **自我认知机制** | `skills/context-tracker/SKILL.md` |
| **需求分析** | `skills/requirements/SKILL.md` |
| **架构设计** | `skills/architecture/SKILL.md` |
| **SDD编排** | `skills/sdd-orchestrator/SKILL.md` |
| **规范编写** | `skills/spec-architect/SKILL.md` |
| **CLI命令** | `docs/VIC-CLI-GUIDE.md` |
| **团队采纳** | `docs/TEAM_ADOPTION_GUIDE.md` |

---

## 技能合并记录 (19→10)

| 原技能 | 现技能 | 说明 |
|--------|--------|------|
| knowledge-boundary, pre-decision-check, signal-register, exploration-journal | context-tracker | 合并4→1 |
| vibe-think, vibe-redesign | requirements | 合并2→1 |
| vibe-architect | architecture | 保持 |
| vibe-design | design-review | 改名 |
| vibe-debug, adaptive-planning | debugging | 合并2→1 |
| vibe-qa, spec-driven-test, test-driven-development | qa | 合并3→1 |
| sdd-orchestrator, spec-to-codebase, sdd-release-guard | sdd-orchestrator | 合并3→1 |
| spec-architect, spec-contract-diff, spec-traceability | 保持 | 保持 |

---

> 详细说明请查阅各 SKILL.md 文件

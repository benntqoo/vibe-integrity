# VIC CLI 操作指南

> 本文档是 VIC CLI 命令的完整参考手册。

---

## 快速开始

```bash
# 初始化项目
vic init --name "My Project" --tech "Go,PostgreSQL"

# 记录技术决策
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# 查看状态
vic status

# 运行Gate检查
vic spec gate 0

# 语义搜索
vic ask "认证系统是如何工作的？"
```

---

## 命令总览

### 基础命令

| 命令 | 别名 | 功能 |
|------|------|------|
| `vic init` | - | 初始化项目 |
| `vic status` | - | 显示项目状态 |
| `vic check` | - | 代码对齐检查 |
| `vic validate` | - | 完整验证 (check + fold) |
| `vic fold` | - | 折叠事件到状态 |
| `vic search` | - | 搜索记录 |
| `vic history` | - | 查看历史 |
| `vic export` | - | 导出数据 |
| `vic import` | - | 导入数据 |

### 记录命令

| 命令 | 别名 | 功能 |
|------|------|------|
| `vic record tech` | `vic rt` | 记录技术决策 |
| `vic record risk` | `vic rr` | 记录风险 |
| `vic record dep` | `vic rd` | 记录依赖 |

### SPEC命令

| 命令 | 功能 |
|------|------|
| `vic spec init` | 初始化SPEC文档 |
| `vic spec status` | 查看SPEC状态 |
| `vic spec gate [0-3\|1.5]` | 运行Gate检查 |
| `vic spec hash` | 检查SPEC Hash并检测变更 |
| `vic spec diff` | 检测自上次检查以来的SPEC变更 |
| `vic spec changes` | 显示SPEC变更历史 |
| `vic spec watch` | 监控SPEC变更并自动运行漂移检测 |
| `vic spec merge` | 合并SPEC到最终文档 |

### Phase/Gate命令

| 命令 | 别名 | 功能 |
|------|------|------|
| `vic phase status` | `vic phase show` | 查看当前阶段 |
| `vic phase advance` | - | 推进阶段 |
| `vic phase check` | - | 检查阶段要求 |
| `vic gate status` | - | 查看所有Gate |
| `vic gate pass` | - | 标记Gate通过 |
| `vic gate check` | - | 检查Gate |
| `vic gate smart` | - | 智能选择Gate（基于风险评估） |

### 语义搜索

| 命令 | 功能 |
|------|------|
| `vic ask <查询>` | 代码库语义搜索 |
| `vic sync` | 同步嵌入索引 |
| `vic assess` | 智能变更评估 |

### 自主模式

| 命令 | 功能 |
|------|------|
| `vic auto start` | 启动自主模式 |
| `vic auto status` | 查看自主状态 |
| `vic auto pause` | 暂停自主模式 |
| `vic auto resume` | 恢复自主模式 |
| `vic auto stop` | 停止自主模式 |

### 成本追踪

| 命令 | 功能 |
|------|------|
| `vic cost init` | 初始化成本追踪 |
| `vic cost status` | 查看成本状态 |
| `vic cost set-budget <金额>` | 设置预算上限 |
| `vic cost add` | 添加成本记录 |

### 产品与规划

| 命令 | 功能 |
|------|------|
| `vic product record` | 记录产品重塑决策 |
| `vic product list` | 列出产品决策 |
| `vic product modes` | 显示四种模式 |
| `vic replan trigger` | 触发自适应重规划 |
| `vic replan list` | 列出重规划历史 |
| `vic replan show` | 显示重规划详情 |

### 测试与调试

| 命令 | 功能 |
|------|------|
| `vic tdd start` | 启动TDD会话 |
| `vic tdd red` | RED阶段 - 写失败测试 |
| `vic tdd green` | GREEN阶段 - 使测试通过 |
| `vic tdd refactor` | REFACTOR阶段 |
| `vic tdd status` | 查看TDD状态 |
| `vic tdd checkpoint` | 保存TDD检查点 |
| `vic tdd history` | 显示TDD历史 |
| `vic debug start` | 启动调试会话 |
| `vic debug survey` | 收集证据 |
| `vic debug pattern` | 找相似问题 |
| `vic debug hypothesis` | 形成并测试假设 |
| `vic debug implement` | 实现修复 |
| `vic debug status` | 查看调试状态 |
| `vic debug report` | 生成调试报告 |

### 设计与依赖

| 命令 | 功能 |
|------|------|
| `vic design init` | 初始化设计系统 |
| `vic design consultation` | 设计咨询模式 |
| `vic design review` | 设计审查模式 |
| `vic design audit` | 运行设计审计 |
| `vic deps scan` | 扫描并生成依赖图 |
| `vic deps list` | 列出所有模块 |
| `vic deps search <模式>` | 按模式搜索模块 |
| `vic deps impact <模块>` | 显示模块变更影响 |
| `vic deps callers <模块>` | 显示模块调用者 |
| `vic sync` | 同步嵌入索引 |

### 技能文档

| 命令 | 功能 |
|------|------|
| `vic skill list` | 列出可用技能 |
| `vic skill show <名称>` | 显示技能文档 |
| `vic skill activate <名称>` | 显示如何激活技能 |

### AI Slop 检测

| 命令 | 功能 |
|------|------|
| `vic slop scan` | 扫描AI Slop模式 |
| `vic slop report` | 显示上次扫描报告 |
| `vic slop list` | 列出配置的检测模式 |
| `vic slop fix` | 自动修复AI Slop |

### E2E 测试

| 命令 | 功能 |
|------|------|
| `vic qa init` | 初始化QA设置 |
| `vic qa quick` | 快速冒烟测试 (~30秒) |
| `vic qa full` | 完整应用测试 (5-15分钟) |
| `vic qa screenshot` | 捕获截图 |
| `vic qa report` | 显示QA报告 |

---

## Phase流程

```
Phase 0: 需求凝固     → Gate 0, Gate 1
     ↓
Phase 1: 架构设计     → Gate 2, Gate 3
     ↓
Phase 2: 代码实现     → Gate 4, Gate 5
     ↓
Phase 3: 验证发布     → Gate 6, Gate 7
```

### 阶段推进示例

```bash
# 1. 需求凝固完成后，通过Gate 0-1
vic gate pass --gate 0 --notes "需求完整"
vic gate pass --gate 1

# 2. 推进到架构设计阶段
vic phase advance --to 1

# 3. 架构设计完成后，通过Gate 2-3
vic gate pass --gate 2 --notes "技术栈确定"
vic gate pass --gate 3

# 4. 推进到代码实现阶段
vic phase advance --to 2

# ... 继续
```

---

## Gate参考

| Gate | 名称 | 检查内容 |
|------|------|---------|
| Gate 0 | 需求完整性 | SPEC-REQUIREMENTS.md 结构检查 |
| Gate 1 | 架构完整性 | SPEC-ARCHITECTURE.md 结构检查 |
| Gate 1.5 | 设计完整性 | DESIGN.md 完整性（可选，用于UI项目） |
| Gate 2 | 代码对齐 | 代码与SPEC一致性 |
| Gate 3 | 测试覆盖 | 测试覆盖率验证 |

---

## 目录结构

```
.vic-sdd/
├── SPEC-REQUIREMENTS.md    # 需求规范
├── SPEC-ARCHITECTURE.md    # 架构规范
├── PROJECT.md              # 项目状态
├── constitution.yaml       # 宪法规则
├── context.yaml            # AI自我认知状态
├── status/
│   ├── events.yaml         # 事件历史
│   ├── state.yaml          # 当前状态
│   ├── phase.yaml          # Phase状态
│   ├── gate-status.yaml    # Gate状态
│   ├── spec-hash.json      # SPEC文件哈希
│   └── change-log.yaml     # SPEC变更历史
├── tech/
│   └── tech-records.yaml   # 技术决策
├── risk-zones.yaml         # 风险记录
├── project.yaml            # 项目元数据
└── dependency-graph.yaml   # 依赖图
```

---

## 常见用法

### 记录技术决策

```bash
vic rt --id DB-001 \
  --title "选择 PostgreSQL" \
  --decision "使用 PostgreSQL 作为主数据库" \
  --reason "需要 ACID 事务支持" \
  --category database \
  --impact high
```

### 记录风险

```bash
vic rr --id RISK-001 \
  --area auth \
  --desc "JWT token 过期处理不完善" \
  --impact medium
```

### 检查代码对齐

```bash
vic check
vic check --category database
vic check --json
```

### 查看Phase状态

```bash
vic phase status
vic phase check
vic phase advance --to 1
```

### 查看Gate状态

```bash
vic gate status
vic gate check --phase 0
vic gate pass --gate 0 --notes "需求完整"
```

### 语义搜索

```bash
vic ask "认证系统是如何工作的？"
vic ask "数据库连接池配置"
```

### 智能Gate选择

```bash
# 查看将要运行的Gate
vic gate smart

# 执行选中的Gate
vic gate smart --execute
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|-------|------|
| `VIC_DIR` | `.vic-sdd` | VIC目录名 |
| `VIC_PROJECT_DIR` | 当前目录 | 项目目录 |
| `VIC_OUTPUT` | `plain` | 输出格式 (json/yaml/plain) |
| `VIC_VERBOSE` | `false` | 详细输出 |

---

## Pre-commit 钩子

在 `.pre-commit-config.yaml` 中添加：

```yaml
repos:
  - repo: local
    hooks:
      - id: vic-gate-check
        name: VIBE-SDD Gate Check
        entry: vic gate check --blocking
        language: system
```

---

## 相关文档

- [SDD-PROCESS-CN.md](./SDD-PROCESS-CN.md) - SDD流程规范

---

**版本**: 1.1.0
**更新**: 2026-03-28

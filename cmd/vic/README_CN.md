# vic - Vibe Integrity CLI

统一的 AI 项目记忆与验证命令行工具。

## 安装

```bash
# 依赖
pip install pyyaml filelock

# Linux/macOS - 添加到 PATH
chmod +x vic
sudo ln -s $(pwd)/vic /usr/local/bin/vic

# Windows PowerShell
Set-Alias vic "python D:\path\to\cmd\vic\vic"
```

## 快速开始

```bash
# 初始化项目
vic init --name "My Project" --tech "Node.js,Vue,PostgreSQL"

# 记录技术决策
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# 查看状态
vic status

# 验证
vic validate
```

---

## 命令列表

| 命令 | 别名 | 用途 |
|------|------|------|
| `record-tech` | `rt` | 记录技术决策 |
| `record-risk` | `rr` | 记录风险 |
| `record-dep` | `rd` | 记录依赖关系 |
| `check` | - | 检查代码对齐 |
| `validate` | - | 完整验证 (check + fold) |
| `fold` | - | 折叠事件到状态 |
| `status` | - | 查看项目状态 |
| `init` | - | 初始化 .vibe-integrity/ |
| `search` | - | 搜索记录 |
| `history` | - | 查看事件历史 |
| `export` | - | 导出数据 |
| `import` | - | 导入数据 |

---

## 命令详解

### vic init

初始化项目的 `.vibe-integrity/` 目录。

```bash
vic init --name "项目名称" --tech "技术栈"
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--name` | 否 | 项目名称 |
| `--tech` | 否 | 技术栈，逗号分隔 |

**示例：**
```bash
vic init --name "my-saas" --tech "Node.js,Vue,PostgreSQL,Redis"
```

---

### vic record-tech (rt)

记录技术决策。

```bash
vic rt --id <ID> --title <标题> --decision <决策> [选项]
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--id` | 是 | 决策 ID，如 `DB-001`, `AUTH-002` |
| `--title` | 是 | 决策标题 |
| `--decision` | 是 | 决策内容 |
| `--category` | 否 | 分类：database, auth, frontend, backend 等 |
| `--reason` | 否 | 决策原因 |
| `--impact` | 否 | 影响级别：low, medium, high |
| `--status` | 否 | 状态：planned, in_progress, completed, deprecated |
| `--files` | 否 | 相关文件，逗号分隔 |

**示例：**
```bash
# 基础用法
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database"

# 完整用法
vic rt --id AUTH-001 \
  --title "JWT Authentication" \
  --decision "Use JWT with refresh tokens" \
  --category auth \
  --reason "Stateless, scalable" \
  --impact high \
  --status in_progress \
  --files "src/auth/,src/middleware/auth.ts"
```

---

### vic record-risk (rr)

记录风险区域。

```bash
vic rr --id <ID> --area <区域> --desc <描述> [选项]
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--id` | 是 | 风险 ID，如 `RISK-001` |
| `--area` | 是 | 风险区域 |
| `--desc` | 是 | 风险描述 |
| `--category` | 否 | 分类 |
| `--impact` | 否 | 影响级别：low, medium, high, critical |
| `--status` | 否 | 状态：identified, mitigating, resolved, accepted |

**示例：**
```bash
vic rr --id RISK-001 \
  --area auth-service \
  --desc "JWT token not properly validated" \
  --impact critical \
  --status identified
```

---

### vic record-dep (rd)

记录模块依赖关系。

```bash
vic rd --module <模块> --deps <依赖列表>
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--module` | 是 | 模块名称 |
| `--deps` | 是 | 依赖的模块，逗号分隔 |

**示例：**
```bash
vic rd --module auth-service --deps user-service,jwt-service,cache-service
```

---

### vic check

检查代码是否与技术决策对齐。

```bash
vic check
```

检测项目代码中是否存在与 `.vibe-integrity/tech-records.yaml` 中记录的技术决策不一致的地方。

**示例输出：**
```
✅ All decisions align with code
   total: 9
   pass: 5
   fail: 0
   skip: 1
   unknown: 3
```

---

### vic validate

运行完整验证流程（代码对齐检查 + 事件折叠）。

```bash
vic validate
```

**执行步骤：**
1. 代码对齐检查
2. 折叠事件到状态

**示例输出：**
```
🔍 Step 1: Code Alignment Check
----------------------------------------
✅ Code alignment OK

📦 Step 2: Fold Events
----------------------------------------

========================================
✅ All validations passed!
```

---

### vic fold

将事件历史折叠为当前状态快照。

```bash
vic fold
```

将 `events.yaml` 中的事件流处理并更新 `state.yaml`。

---

### vic status

查看项目当前状态。

```bash
vic status
```

**示例输出：**
```
📊 Project Status
========================================
Last folded: 2026-03-17
Active decisions: 1
Active risks: 1

Tech records: 10
Risks recorded: 0

📋 Recent Tech Records:
   [FE-002] 使用 Pinia 进行状态管理
   [DB-001] Use PostgreSQL
```

---

### vic search

搜索技术记录和风险记录。

```bash
vic search <查询词>
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `query` | 是 | 搜索关键词 |

**示例：**
```bash
vic search postgres
vic search authentication
```

---

### vic history

查看事件历史记录。

```bash
vic history [--type <类型>] [--limit <数量>]
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--type` | 否 | 按事件类型过滤 |
| `--limit` | 否 | 显示数量，默认 10 |

**示例：**
```bash
# 显示最近 5 条事件
vic history --limit 5

# 只显示决策类型事件
vic history --type decision_made
```

---

### vic export

导出 `.vibe-integrity/` 数据为 JSON 文件。

```bash
vic export [--output <文件>] [--type <类型>]
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `--output`, `-o` | 否 | 输出文件，默认 `vibe-integrity-export.json` |
| `--type` | 否 | 导出类型：tech, risks, events |

**示例：**
```bash
# 导出全部
vic export --output backup.json

# 只导出技术记录
vic export --type tech -o tech-decisions.json
```

---

### vic import

从 JSON 文件导入数据。

```bash
vic import <输入文件>
```

**参数：**
| 参数 | 必需 | 说明 |
|------|------|------|
| `input` | 是 | 输入 JSON 文件 |

**示例：**
```bash
vic import backup.json
```

导入时会自动跳过已存在的记录（按 ID 判断），事件始终追加。

---

## 数据文件

```
.vibe-integrity/
├── events.yaml          # 所有事件 (追加写入)
├── state.yaml           # 当前状态 (fold 生成)
├── tech-records.yaml    # 技术决策
├── risk-zones.yaml      # 风险区域
├── project.yaml         # 项目信息
└── dependency-graph.yaml # 依赖关系
```

---

## 典型工作流

### 开始新项目
```bash
vic init --name "My App" --tech "React,Node,PostgreSQL"
```

### 做技术决策时
```bash
vic rt --id FE-001 --title "Use React Query" --decision "Data fetching layer" --reason "Caching, dedup"
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

### 迁移/备份项目记忆
```bash
vic export -o project-memory.json
# ... 在新项目中 ...
vic import project-memory.json
```

---

## 退出码

| 退出码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 失败/错误 |

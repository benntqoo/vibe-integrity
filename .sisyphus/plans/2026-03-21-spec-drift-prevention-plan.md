# VIBE-SDD SPEC 偏移预防改善计划

> **生成时间**: 2026-03-21  
> **状态**: 待执行  
> **目标**: 解决 AI 认知膨胀导致的 SPEC 偏移问题，让 AI 快速理解状态且不随意开发

---

## 问题总结

基于 Oracle + 深度分析，SPEC 漂移有三个根本原因：

```
上下文饥饿 → AI 用假设填充 → 小改动积累 → SPEC 过时 → 偏移固化
    ↑                                              ↓
会话断裂（不读/不遵守 SPEC） ← ← ← ← ← ← ← ← ← ← ← ┘
```

**VIBE-SDD 现有机制**: Gate 检查（事后检测）、context-tracker（软性警告）、文件持久化  
**缺失环节**: 硬性阻断、双向同步、强制确认

---

## 改善方案

### 核心理念

把"建议性机制"变为"不可绕过机制"。

| 维度 | 当前 | 改善后 |
|------|------|------|
| SPEC 遵守 | warning（可忽略） | **blocker（不可绕过）** |
| 会话开始 | 提示读文件 | **强制确认清单 + SPEC Hash 检查** |
| 文档同步 | SPEC → 代码单向 | **双向同步（代码变更 → 反向更新 SPEC）** |
| 漂移检测 | 手动运行 gate | **CI 自动触发 + diff 摘要注入** |

---

## 实施阶段

### 阶段 1：硬性阻断机制（P0，立即可做）

#### 1.1 将 `spec_aligned` 升级为 Blocker

**文件**: `skills/context-tracker/SKILL.md`

**改动**: 在 blocker 列表中增加 `spec_unaligned`

```yaml
# 当前（软性警告）
signals:
  warnings:
    - spec_unaligned: "Code diverged from SPEC"

# 改为（硬性阻断）
signals:
  blockers:
    - spec_unaligned: "Code vs SPEC mismatch → must fix or update SPEC before continuing"
```

**验收**: 
- [ ] `context-tracker` 运行后，若 `spec_unaligned=true`，confidence 自动 < 0.4
- [ ] AI 无法继续工作直到解决
- [ ] 运行测试验证行为

#### 1.2 会话开始强制清单

**文件**: `.vic-sdd/agent-prompt.md`

**改动**: 将 agent-prompt.md 从"提示"升级为"必须确认的清单"

```markdown
# 在开始前，你必须确认以下事项：
# 
# □ 我已运行 vic spec status 并确认当前 Gate 状态
# □ 我已读取 .vic-sdd/context.yaml（known/inferred/assumed）
# □ 我没有任何未解决的 assumed（假设）
# □ 如果有 assumed → 我已标记为 blocker 并请求确认
#
# ⚠️ 如果你跳过以上确认继续工作，你违反了 VIBE-SDD 流程。
```

**新增**: SPEC Hash 检查逻辑

```markdown
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPEC Hash 检查
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 运行: vic spec status --hash
# 
# 如果显示 "SPEC changed since last session":
# → 你必须先阅读 vic spec diff
# → 确认本次工作涉及的 SPEC 章节
# → 在继续前更新 context.yaml
```

**验收**:
- [ ] agent-prompt.md 包含强制确认清单
- [ ] SPEC Hash 检查逻辑已添加
- [ ] AI 会话开始时必须确认清单

---

### 阶段 2：SPEC Hash 追踪增强（P0）

#### 2.1 实现 SPEC Hash 检查命令

**文件**: `cmd/vic-go/internal/commands/hash.go` (新增)

**功能**:
```go
// vic spec hash
// 1. 计算当前 SPEC 文件的 hash
// 2. 与 .vic-sdd/status/spec-hash.json 对比
// 3. 如果不同 → 输出 "SPEC changed since last session"
// 4. 如果不同 → 显示 diff 摘要（变化的章节列表）
// 5. 更新 spec-hash.json
```

**spec-hash.json 格式**:
```json
{
  "last_check": "2026-03-21T10:00:00Z",
  "hashes": {
    "SPEC-REQUIREMENTS.md": "abc123",
    "SPEC-ARCHITECTURE.md": "def456"
  }
}
```

#### 2.2 在 agent-prompt.md 中集成 Hash 检查

**改动**: 会话开始时自动运行 hash 检查

```markdown
# 会话开始自动执行:
# 1. vic spec hash
# 2. 如果 hash 变化 → vic spec diff
# 3. AI 必须确认后继续
```

**验收**:
- [ ] `vic spec hash` 命令正常工作
- [ ] hash 变化时正确显示 diff
- [ ] spec-hash.json 正确更新

---

### 阶段 3：Constitution 机制（P1）

#### 3.1 创建 Constitution 文件

**文件**: `.vic-sdd/constitution.yaml` (新增)

```yaml
# VIBE-SDD Constitution
# 不可违反的规则清单

version: "1.0"
created: "2026-03-21"

principles:
  - id: SPEC-FIRST
    rule: "功能变更必须先更新 SPEC，再修改代码"
    verifiable: false
    blocker_id: spec_update_required
    
  - id: SPEC-ALIGNED
    rule: "代码必须与 SPEC 对齐"
    verifiable: true
    checker: vic check
    blocking: true
    
  - id: NO-TODO-IN-CODE
    rule: "代码中不允许 TODO/FIXME"
    verifiable: true
    checker: grep -r "TODO\\|FIXME" src/
    blocking: false
    
  - id: NO-CONSOLE-IN-PROD
    rule: "生产代码不允许 console.log"
    verifiable: true
    checker: grep -r "console\\.log" src/
    blocking: false
    
  - id: TESTS-REQUIRED
    rule: "新功能必须包含测试"
    verifiable: true
    checker: vic spec gate 3
    blocking: true
    
  - id: GATE-BEFORE-COMMIT
    rule: "提交前必须通过所有相关 Gate"
    verifiable: true
    checker: vic gate check --blocking
    blocking: true

enforcement:
  on_plan: check_constitution    # 每次 plan 生成前
  on_commit: verify_gates_passed  # 每次提交前
  on_phase_change: full_review    # 阶段推进前
```

#### 3.2 创建 Constitution 检查 Skill

**文件**: `skills/constitution-check/SKILL.md` (新增)

**功能**: 
- 每次 plan 生成时检查 constitution
- 输出合规性报告
- 标记违规项为 blocker

```markdown
## Constitution Check Skill

### 何时使用
- 每次生成实现计划前
- 每次代码审查前
- 每次阶段推进前

### 检查流程
1. 读取 .vic-sdd/constitution.yaml
2. 逐项检查规则
3. 输出检查报告
4. 如有违规 → 标记为 blocker

### 输出格式
```yaml
constitution_report:
  checked_at: "2026-03-21T10:00:00Z"
  total_rules: 6
  passed: 5
  failed: 1
  blockers: ["SPEC-ALIGNED"]
```

### Blocker 规则
- `SPEC-ALIGNED` → 代码与 SPEC 不对齐
- `SPEC-FIRST` → 功能变更未先更新 SPEC
- `GATE-BEFORE-COMMIT` → Gate 未通过就提交
```

**验收**:
- [ ] constitution.yaml 存在且格式正确
- [ ] constitution-check skill 可以运行
- [ ] 违规项正确标记为 blocker

---

### 阶段 4：双向 SPEC 同步（P1）

#### 4.1 在 spec-contract-diff 中追加自动更新逻辑

**文件**: `skills/spec-contract-diff/SKILL.md`

**改动**: 检测到 drift 后，追加选项让 AI 选择更新 SPEC

```markdown
## Drift 检测后的选项

当 `requires_spec_update: true` 时，AI 必须选择以下之一：

1. **更新 SPEC**（推荐）
   - 在 SPEC 中记录本次变更
   - 运行 vic spec diff 确认变更范围
   - 继续工作

2. **回退代码**
   - 将代码改回符合 SPEC 的状态
   - 继续工作

3. **记录为风险**
   - 在 risk-zones.yaml 中记录本次 drift
   - 获得人工确认后继续
   - ⚠️ 仅用于紧急修复
```

#### 4.2 在 vic check 中追加 SPEC 更新建议

**文件**: `cmd/vic-go/internal/commands/check.go`

**功能**: 检测到 drift 时，显示"建议更新 SPEC"的命令

```go
// vic check 输出增强
// 当检测到代码 vs SPEC drift 时：
// 
// 检测到 drift: UserService.update 方法签名变更
// 建议操作:
//   1. 更新 SPEC: vic spec update --file SPEC-ARCHITECTURE.md --section "模块设计"
//   2. 或者回退代码变更
//   3. 或者记录为风险: vic rr --id DRIFT-001 --desc "..."
```

**验收**:
- [ ] spec-contract-diff 包含自动更新选项
- [ ] vic check 显示 SPEC 更新建议
- [ ] drift 后 AI 知道如何处理

---

### 阶段 5：CI 自动漂移检测（P2）

#### 5.1 添加 GitHub Actions 工作流

**文件**: `.github/workflows/spec-drift.yml` (新增)

```yaml
name: SPEC Drift Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  spec-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        
      - name: Run SPEC Drift Check
        run: |
          # 1. 运行 Gate 2（代码对齐）
          vic spec gate 2
          
          # 2. 如果失败，输出 drift 报告
          if [ $? -ne 0 ]; then
            echo "## SPEC Drift Detected" >> $GITHUB_STEP_SUMMARY
            vic spec diff >> $GITHUB_STEP_SUMMARY
            exit 1
          fi

      - name: Run Gate Checks
        run: |
          vic gate check --blocking
```

**验收**:
- [ ] GitHub Actions workflow 存在
- [ ] push/PR 时自动运行 drift 检测
- [ ] drift 存在时 PR 构建失败

---

## 文件变更清单

### 新增文件

| 文件 | 阶段 | 说明 |
|------|------|------|
| `skills/constitution-check/SKILL.md` | P1 | Constitution 检查技能 |
| `.vic-sdd/constitution.yaml` | P1 | 不可违反规则清单 |
| `cmd/vic-go/internal/commands/hash.go` | P0 | SPEC hash 检查命令 |
| `.github/workflows/spec-drift.yml` | P2 | CI drift 检测 |

### 修改文件

| 文件 | 阶段 | 改动 |
|------|------|------|
| `skills/context-tracker/SKILL.md` | P0 | `spec_aligned` → blocker |
| `.vic-sdd/agent-prompt.md` | P0 | 强制确认清单 + SPEC Hash 检查 |
| `skills/spec-contract-diff/SKILL.md` | P1 | 追加自动更新逻辑 |
| `cmd/vic-go/internal/commands/check.go` | P1 | 显示 SPEC 更新建议 |

---

## 优先级与工作量

| 阶段 | 任务 | 优先级 | 工作量 | 效果 |
|------|------|--------|--------|------|
| P0 | `spec_aligned` → blocker | 🔴 必须 | 10min | 高 |
| P0 | agent-prompt.md 强制清单 | 🔴 必须 | 15min | 高 |
| P0 | `vic spec hash` 命令 | 🔴 必须 | 2h | 高 |
| P1 | constitution.yaml | 🟡 推荐 | 1h | 中 |
| P1 | constitution-check skill | 🟡 推荐 | 2h | 中 |
| P1 | SPEC 更新建议 | 🟡 推荐 | 1h | 中 |
| P2 | CI drift 检测 | 🟢 可选 | 2h | 低 |

---

## 验收标准

### P0 验收（必须通过）
- [ ] `spec_aligned` 是 blocker，AI 无法绕过
- [ ] agent-prompt.md 有强制确认清单
- [ ] `vic spec hash` 正确检测 SPEC 变化

### P1 验收
- [ ] constitution.yaml 存在且可执行
- [ ] drift 检测后 AI 知道更新 SPEC
- [ ] CI 自动运行 drift 检测

### 测试场景

| 场景 | 预期行为 |
|------|---------|
| AI 改代码不更新 SPEC | `spec_aligned` blocker 触发，confidence < 0.4，AI 停止 |
| 新会话，SPEC 已更新 | Hash 检查 → diff 摘要 → AI 必须确认 |
| Drift 已发生 | spec-contract-diff 报告 → 显示更新 SPEC 的选项 |
| PR 时有 drift | GitHub Actions 失败，显示 drift 报告 |

---

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| Blocker 太多，AI 无法工作 | 体验差 | `blockers >= 2` 才真正 STOP，少量可继续 |
| Constitution 规则太严格 | 用户绕过 | 初期只启用 2-3 条核心规则 |
| SPEC 更新循环 | AI 无穷更新 SPEC | 设置更新上限（每次最多更新 3 处） |

---

## 实施顺序

```
Day 1:
  ├── 阶段 1.1: spec_aligned → blocker (10min)
  └── 阶段 1.2: agent-prompt.md 强制清单 (15min)

Day 2:
  └── 阶段 2: vic spec hash 命令 (2h)

Day 3:
  ├── 阶段 3.1: constitution.yaml (1h)
  └── 阶段 3.2: constitution-check skill (2h)

Day 4:
  ├── 阶段 4: SPEC 更新建议 (1h)
  └── 测试 + 文档更新 (2h)

Day 5 (可选):
  └── 阶段 5: CI drift 检测 (2h)
```

---

**下一步**: 开始阶段 1.1 — 将 `spec_aligned` 升级为 blocker

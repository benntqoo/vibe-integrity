# 智能判断系统设计

> VIBE-SDD 灵活性改进方案 - 让系统自动适应，而非增加用户选择

---

## 设计原则

1. **零认知负担** - 用户不需要选择模式或判断用哪个 skill
2. **渐进式严格** - 风险低时宽松，风险高时严格
3. **自动流转** - skill 切换自动发生，无需显式调用
4. **透明可追溯** - 判断逻辑清晰，决策可解释

---

## 核心组件：智能判断引擎

### 1. 变更类型检测

```yaml
# 自动检测变更类型
change_detection:
  methods:
    - git_diff_analysis:      # 分析 git diff
    - file_path_patterns:     # 文件路径模式匹配
    - content_keywords:       # 内容关键词检测
    - spec_file_changes:      # SPEC 文件变更检测

  types:
    typo_fix:
      indicators:
        - files_changed: 1
        - lines_changed: < 10
        - no_logic_change: true
      risk: minimal
      gates_required: []

    rename_refactor:
      indicators:
        - files_changed: <= 5
        - change_type: "rename"
        - no_logic_change: true
      risk: low
      gates_required: [gate_2]

    bug_fix:
      indicators:
        - keywords: ["fix", "bug", "issue", "error"]
        - test_added: true
      risk: medium
      gates_required: [gate_2, gate_3]

    feature_addition:
      indicators:
        - keywords: ["feat", "add", "new", "implement"]
        - new_functions: true
      risk: high
      gates_required: [gate_0, gate_2, gate_3]

    architecture_change:
      indicators:
        - files_changed: > 10
        - spec_files_affected: true
        - keywords: ["refactor", "restructure", "migrate"]
      risk: critical
      gates_required: [gate_0, gate_1, gate_2, gate_3]
```

### 2. 风险等级评估

```yaml
# 风险评估矩阵
risk_assessment:
  factors:
    - scope:              # 影响范围
        single_file: 1
        single_module: 2
        multiple_modules: 3
        cross_cutting: 4

    - complexity:         # 复杂度
        trivial: 1
        simple: 2
        moderate: 3
        complex: 4

    - spec_impact:        # SPEC 影响度
        none: 0
        minor: 1
        moderate: 2
        major: 3

    - test_coverage:      # 测试覆盖需求
        existing_sufficient: 0
        needs_update: 1
        needs_new_tests: 2
        needs_integration: 3

  formula: |
    risk_score = (scope + complexity + spec_impact + test_coverage) / 4

  levels:
    minimal:   0.0 - 0.5  # 快速通道
    low:       0.5 - 1.5  # 简化检查
    medium:    1.5 - 2.5  # 标准流程
    high:      2.5 - 3.5  # 完整流程
    critical:  3.5 - 4.0  # 严格流程 + 人工确认
```

### 3. Gate 智能选择

```yaml
# 根据风险自动选择需要的 Gate
gate_selection:
  rules:
    - condition: "risk == minimal"
      gates: []
      workflow: quick

    - condition: "risk == low"
      gates: [gate_2]
      workflow: quick

    - condition: "risk == medium and spec_exists"
      gates: [gate_2, gate_3]
      workflow: implementation

    - condition: "risk == medium and !spec_exists"
      gates: [gate_0, gate_2, gate_3]
      workflow: spec_workflow_then_implementation

    - condition: "risk == high"
      gates: [gate_0, gate_2, gate_3]
      workflow: full_sdd

    - condition: "risk == critical"
      gates: [gate_0, gate_1, gate_2, gate_3]
      workflow: full_sdd + human_checkpoint
```

### 4. 自动 Skill 切换

```yaml
# context-tracker 自动切换逻辑
skill_transition:
  triggers:
    # 从任意状态检测到需求不清晰
    - condition: "requirements_vague or spec_not_exists"
      from: any
      to: spec-workflow
      auto: true
      notify: "检测到需求不清晰，自动切换到 spec-workflow"

    # SPEC 已冻结，准备实现
    - condition: "spec_frozen and confidence >= 0.7"
      from: spec-workflow
      to: implementation
      auto: true
      notify: "SPEC 已冻结，自动切换到 implementation"

    # 代码完成，准备提交
    - condition: "code_complete and gates_passed"
      from: implementation
      to: unified-workflow
      auto: true
      notify: "代码完成且 Gates 通过，自动切换到 unified-workflow"

    # 检测到简单变更
    - condition: "risk == minimal or risk == low"
      from: any
      to: quick
      auto: true
      notify: "检测到简单变更，使用 quick 流程"
```

---

## 实现方案

### Phase 1: 增强 context-tracker

修改 `context-tracker/SKILL.md`，添加智能判断逻辑：

```yaml
## L2: Intelligent Assessment (New)

### Step 1: Detect Change Type
Automatic detection based on:
- git diff analysis
- file path patterns
- content keywords

### Step 2: Assess Risk Level
Formula: (scope + complexity + spec_impact + test_coverage) / 4

### Step 3: Select Required Gates
Based on risk level:
- Minimal/Low: Skip or minimal gates
- Medium: Standard gates
- High/Critical: Full gates + checkpoints

### Step 4: Auto-transition
Automatically switch to appropriate skill without user decision
```

### Phase 2: 修改 vic CLI

添加智能判断命令：

```bash
# 新命令：智能判断当前任务
vic assess
# 输出：
# Change Type: feature_addition
# Risk Level: medium (2.1)
# Gates Required: [gate_0, gate_2, gate_3]
# Recommended Skill: implementation
# Auto-switch: yes

# 新命令：自动模式（根据判断自动执行）
vic auto-assess --execute
# 自动切换到推荐的 skill 并开始工作
```

### Phase 3: 修改 Gate 检查

让 Gate 检查更智能：

```bash
# 当前：必须显式运行所有 Gate
vic spec gate 0
vic spec gate 1
vic spec gate 2
vic spec gate 3

# 改进：智能 Gate 检查
vic gate smart
# 根据风险自动选择需要的 Gate
# 跳过不必要的 Gate
# 输出跳过原因
```

---

## 用户体验对比

### 改进前

```
用户: 我要修一个 bug

AI: 请选择你要使用的 skill:
    1. quick - 简单修改
    2. implementation - 完整实现流程

用户: implementation

AI: 请运行以下命令:
    vic spec gate 2
    vic spec gate 3

用户: (运行命令)

AI: 好的，开始修复...
```

### 改进后

```
用户: 我要修一个 bug

AI: [自动检测]
    - 变更类型: bug_fix
    - 风险等级: medium
    - 需要 Gate: [gate_2, gate_3]
    - 自动切换到: implementation

    开始修复...

    [修复完成]
    [自动运行 gate_2, gate_3]

    ✅ 修复完成，Gates 通过
```

---

## 文件修改清单

| 文件 | 修改内容 |
|------|---------|
| `context-tracker/SKILL.md` | 添加智能判断章节 |
| `context-tracker/references/change-detection.md` | 新建：变更检测算法 |
| `context-tracker/references/risk-assessment.md` | 新建：风险评估矩阵 |
| `cmd/vic-go/internal/commands/assess.go` | 新建：vic assess 命令 |
| `cmd/vic-go/internal/commands/gate.go` | 修改：添加 smart 模式 |
| `AGENTS.md` | 更新：智能判断说明 |

---

## 实施优先级

| 优先级 | 任务 | 工作量 |
|--------|------|--------|
| P1 | 增强 context-tracker SKILL.md | 小 |
| P1 | 创建 change-detection.md | 小 |
| P1 | 创建 risk-assessment.md | 小 |
| P2 | 实现 vic assess 命令 | 中 |
| P2 | 实现 vic gate smart | 中 |
| P3 | 添加 auto-assess --execute | 中 |

---

## 预期效果

| 指标 | 改进前 | 改进后 |
|------|--------|--------|
| 用户决策次数 | 3-5 次/任务 | 0-1 次/任务 |
| 简单任务耗时 | 5-10 分钟 | 1-2 分钟 |
| 学习曲线 | 中等 | 低 |
| 灵活性 | 低 | 高 |
| 质量保障 | 高 | 高（不变） |

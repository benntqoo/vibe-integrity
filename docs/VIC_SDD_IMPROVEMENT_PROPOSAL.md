# VIC-SDD 改进提案：结合 Superpowers、gstack、GSD-2 的优点

## 一、VIC-SDD 当前架构分析

### 1.1 核心优势

VIC-SDD 的核心优势在于其结构化方法和项目记忆系统：

- **三阶段命名**：定图纸 → 打地基 → 立规矩，符合开发直觉
- **Gate 检查点**：强制质量门禁
- **.vic-sdd/ 记忆系统**：完整的项目状态持久化
- **团队协作支持**：决策记录、风险追踪、依赖图谱
- **CLI 工具驱动**：vic 命令统一操作入口
- **AI 快速理解机制**：15秒理解项目上下文

### 1.2 核心不足

与 Superpowers、gstack、GSD-2 相比，VIC-SDD 在以下方面存在明显不足：

| 不足领域 | VIC-SDD 现状 | 最佳参照 |
|----------|-------------|---------|
| 自主执行 | 需人工推进每个 Gate | GSD-2 的状态机驱动 |
| 产品思维 | 无专门产品重塑 | gstack 的 /plan-ceo-review |
| 设计系统 | 无设计能力 | gstack 的 design skills |
| 浏览器测试 | 无端到端测试 | gstack 的 /browse + /qa |
| TDD 强制 | 无 TDD 流程 | Superpowers 的 TDD skill |
| 系统化调试 | 无调试方法论 | Superpowers 的 systematic-debugging |
| 成本追踪 | 无 | GSD-2 的完整成本账本 |
| 崩溃恢复 | 有限 | GSD-2 的状态机恢复 |
| 自适应重规划 | 无 | GSD-2 的切片后重评估 |
| AI 垃圾检测 | 无 | gstack 的 80 项审计 |

---

## 二、改进提案

### 2.1 增强自主执行能力

#### 问题

VIC-SDD 目前需要人工推进每个 Gate，无法实现「设置后离开」的体验。

#### 改进方案：引入 GSD-2 的状态机模式

**新增文件：** `.vic-sdd/auto-state.yaml`

```yaml
auto_mode:
  enabled: true
  current_phase: Implementation
  current_slice: S01
  current_task: T03
  last_dispatch: 2026-03-19T10:30:00Z
  dispatch_count: 47
  total_cost: 12.50
  
recovery:
  last_saved: 2026-03-19T10:25:00Z
  pending_artifacts: []
  stuck_detection_count: 0
```

**新增命令：** `vic auto`

```bash
# 启动自主模式，AI 自动推进项目
vic auto

# 查看自主模式状态
vic auto status

# 暂停自主模式
vic auto pause

# 恢复自主模式
vic auto resume
```

**状态机流程：**

```
定图纸 → 打地基 → 立规矩
    │          │         │
    ▼          ▼         ▼
Gate 0    Gate 1    Gate 2-3
    │          │         │
    ▼          ▼         ▼
  AUTO      AUTO      AUTO
```

#### 预期效果

- 用户可以「设置 vic auto 后离开」
- AI 自动推进项目，减少人工干预
- 崩溃后可从最后一个有效状态恢复

---

### 2.2 引入产品思维流程

#### 问题

VIC-SDD 缺少 gstack 的「Brian Chesky 模式」——在写代码前重塑产品。

#### 改进方案：新增 vibe-redesign skill

**新增文件：** `skills/vibe-redesign/SKILL.md`

```
skills/
├── vibe-redesign/           # 新增：产品重塑
│   └── SKILL.md
```

**SKILL.md 核心内容：**

```markdown
# Vibe Redesign

## 何时使用
当用户提出功能需求时，首先激活此技能进行产品思维。

## 核心原则
**不按字面意思实现。** 先问：「这个产品真正是为了什么？」

## 四模式

### 1. EXPANSION - 范围扩展
AI 热情推荐雄心勃勃的版本。每个扩展作为单独决策供用户选择。

示例：
用户：「让卖家上传照片」
AI：「如果真正的产品是帮助卖家创建能卖出去的列表，
      那我们应该考虑：
      - 从照片自动识别产品
      - 推断 SKU/型号
      - 自动生成标题描述
      - 建议最佳主图
      - 检测低质量照片
      - 提升体验质感」

### 2. SELECTIVE - 选择性扩展
中立地呈现机会，用户选择要追求哪些。

### 3. HOLD - 保持范围
严格审查现有计划，不呈现任何扩展。

### 4. REDUCTION - 范围缩减
找到最小可行版本。

## 输出
生成 `docs/PRODUCT-REDESIGN.md`，包含：
- 当前理解 vs 真正产品
- 扩展选项（带 Effort/Impact）
- 用户决策记录
```

#### 与 VIC-SDD 整合

**工作流变更：**

```
用户需求 → vibe-redesign (四模式) → 产品重塑文档
    ↓
定图纸 (vibe-think) → SPEC-REQUIREMENTS.md
```

**决策记录：**

```yaml
# tech-records.yaml 新增类型
decisions:
  - id: PROD-001
    type: product-redesign
    trigger: "用户说：让卖家上传照片"
    real_product: "帮助卖家创建能卖出去的列表"
    mode: expansion
    options:
      - feature: 从照片识别产品
        effort: high
        impact: high
      - feature: 提升体验质感
        effort: medium
        impact: medium
    decision: selected:auto-enrichment
```

---

### 2.3 增强设计系统能力

#### 问题

VIC-SDD 缺少 gstack 的设计能力——无法从零构建设计系统或进行视觉审查。

#### 改进方案：新增 vibe-design skill

**新增文件：** `skills/vibe-design/SKILL.md`

**核心能力：**

1. **design-consultation 模式**
   - 从零构建设计系统
   - 字体选择、颜色调色板、布局策略
   - 提出「创意风险」而非仅「安全选择」

2. **design-review 模式**
   - 80 项视觉审计
   - AI 垃圾检测（渐变英雄区、三栏图标网格等）
   - 修复循环 + 前后截图

3. **AI 垃圾检测标准**

| 检测项 | AI 垃圾模式 | 替代方案 |
|--------|-----------|---------|
| 英雄区 | 渐变背景 | 粗体排版或真实图片 |
| 布局 | 三栏图标网格 | 非对称布局 |
| 圆角 | 统一 8px 圆角 | 按元素角色变化 |
| 排版 | 纯 sans-serif | 混合衬线字体 |

#### 与 VIC-SDD 整合

**新增文档类型：**

```yaml
# project.yaml 新增字段
design:
  system: "docs/DESIGN.md"  # 设计系统文档
  last_review: 2026-03-19
  ai_slop_score: A  # A/B/C/D
```

**工作流：**

```
产品重塑 → 定图纸 → 打地基
    ↓                    ↓
vibe-design          包含设计规范
    ↓                    ↓
docs/DESIGN.md ───→ SPEC-ARCHITECTURE.md
```

---

### 2.4 引入 TDD 强制循环

#### 问题

VIC-SDD 缺少 Superpowers 的 TDD 强制流程，AI 可能跳过测试直接写实现。

#### 改进方案：新增 spec-test skill

**新增文件：** `skills/spec-test/SKILL.md`

```markdown
# Spec Test - TDD 强制循环

## 铁律
**在任何测试通过之前，禁止编写实现代码。**

## 红-绿-重构循环

### 1. 红（Red）
```bash
# 写一个失败的测试
# 运行确认它失败
npm test
# 预期：测试失败，错误信息明确
```

### 2. 绿（Green）
```bash
# 编写最小代码使测试通过
# 运行确认通过
npm test
# 预期：所有测试通过
```

### 3. 重构（Refactor）
```bash
# 改进代码结构，不改变行为
# 运行确认测试仍然通过
npm test
```

## 验证标准

每个功能必须有对应测试：

| 功能类型 | 最低测试覆盖 |
|----------|-------------|
| API 端点 | 集成测试 |
| 业务逻辑 | 单元测试 |
| UI 组件 | 组件测试 |
| 关键流程 | E2E 测试 |

## Gate 3 增强

```yaml
# gate-status.yaml 新增
gate_3:
  status: pending
  tdd_enforcement: required
  test_coverage:
    unit: 80%
    integration: 70%
    e2e: 50%
```

---

### 2.5 引入系统化调试方法论

#### 问题

VIC-SDD 缺少 Superpowers 的系统化调试流程，AI 可能「打补丁」而非根因修复。

#### 改进方案：新增 vibe-debug skill

**新增文件：** `skills/vibe-debug/SKILL.md`

```markdown
# Vibe Debug - 系统化调试

## 四阶段流程

### 1. 根因调查（必须完成才能进入下一阶段）
- 收集证据：日志、错误信息、复现步骤
- 建立假设
- **禁止：** 在未完成根因调查前提出修复

### 2. 模式分析
- 找到代码库中工作的类似示例
- 比较差异
- 识别「为什么这个工作了，那个没工作」

### 3. 假设与测试
- 形成单一假设
- 最小化测试：只改变一个变量
- 验证或推翻假设

### 4. 实现修复
- 修复根因，而非症状
- 验证修复
- 防止回归

## 硬性约束

**如果已尝试三个以上的修复但都失败：**
```
STOP.
质疑架构本身，而非继续打补丁。
```

## 与 VIC-SDD 整合

```yaml
# risk-zones.yaml 新增
debug_session:
  started: 2026-03-19T10:00:00
  attempts: 4
  recommendation: |
    已尝试4种修复方案都失败。
    建议重新评估架构设计。
```

---

### 2.6 增强验证与测试能力

#### 问题

VIC-SDD 缺少 gstack 的真正浏览器自动化和端到端测试能力。

#### 改进方案：新增 vibe-qa skill

**新增文件：** `skills/vibe-qa/SKILL.md`

**核心能力：**

1. **浏览器自动化**（基于 Playwright）
   - 真实 Chromium 浏览器
   - 页面快照 + 元素引用
   - 表单填写、点击、截图

2. **四种 QA 模式**

| 模式 | 用途 | 时间 |
|------|------|------|
| diff-aware | 自动识别功能分支变更 | 5-10 分钟 |
| full | 全面探索整个应用 | 5-15 分钟 |
| quick | 烟雾测试 | 30 秒 |
| regression | 与基准对比 | 依赖规模 |

3. **自动回归测试生成**
   - 每次修复后自动生成回归测试
   - 包含完整归因追踪

#### 与 VIC-SDD 整合

**新增 Gate：**

```yaml
# gate-status.yaml 新增
gate_4:
  name: E2E Verification
  status: pending
  requirements:
    browser_test: required
    regression_tests: required
    screenshots: required
```

**工作流：**

```
实现完成 → Gate 3 (测试覆盖)
    ↓
Gate 4 (E2E 验证) → vibe-qa
    ↓
生成回归测试 → vic check
    ↓
通过 → 准备发布
```

---

### 2.7 引入成本追踪系统

#### 问题

VIC-SDD 缺少 GSD-2 的完整成本追踪，无法了解「用 AI 构建这个功能实际花了多少钱」。

#### 改进方案：增强 vic status

**增强后的 vic status 输出：**

```bash
$ vic status

═══════════════════════════════════════════════════════
  VIBE-SDD Project Status: my-project
═══════════════════════════════════════════════════════

📦 当前阶段: Phase 1 - MVP
🎯 Milestone: M2 - MVP 功能完成
📊 进度: 45% (8/18 验收标准通过)

───────────────────────────────────────────────────────
  💰 成本追踪
───────────────────────────────────────────────────────

  本次会话:
    Token (输入):  125,430
    Token (输出):   43,210
    成本:          $2.34

  项目总计:
    Token (输入):  892,340
    Token (输出):  312,450
    成本:          $18.72

  预算状态:
    预算上限:     $50.00
    已使用:       37%
    预计完成:     $22.50

───────────────────────────────────────────────────────
  📋 Gate 状态
───────────────────────────────────────────────────────

  Gate 0: ✅ 需求完整性      (passed)
  Gate 1: ✅ 架构完整性      (passed)
  Gate 2: ⏳ 代码对齐        (3/5 检查通过)
  Gate 3: ⏳ 测试覆盖        (70% - 需要 80%)
  Gate 4: ⏳ E2E 验证        (未开始)

───────────────────────────────────────────────────────
  🔧 活跃 Skills
───────────────────────────────────────────────────────

  • spec-architect     [加载中]
  • spec-to-codebase   [已就绪]
  • vibe-qa           [可用]
```

**数据存储：**

```yaml
# .vic-sdd/status/cost.yaml
cost_tracking:
  session:
    start: 2026-03-19T09:00:00Z
    input_tokens: 125430
    output_tokens: 43210
    cost: 2.34
    
  project_total:
    input_tokens: 892340
    output_tokens: 312450
    cost: 18.72
    
  budget:
    ceiling: 50.00
    alert_threshold: 0.80
    auto_pause: true
```

---

### 2.8 增强崩溃恢复能力

#### 问题

VIC-SDD 当前的状态持久化是基本的，无法像 GSD-2 那样从崩溃中完全恢复。

#### 改进方案：增强 auto-recovery 机制

**新增文件：** `.vic-sdd/status/recovery.yaml`

```yaml
recovery:
  enabled: true
  checkpoint_interval: 300  # 每5分钟保存检查点
  
  last_checkpoint: 2026-03-19T10:25:00Z
  pending_operations: []
  
  dispatch_history:
    - id: DISPATCH-047
      timestamp: 2026-03-19T10:30:00Z
      skill: spec-to-codebase
      task: "实现用户认证 API"
      status: in_progress
      artifacts_written:
        - src/auth/login.ts
        - tests/auth/login.test.ts
      tool_calls_made: 23
      
  crash_sessions:
    - timestamp: 2026-03-19T09:15:00Z
      reason: "Connection lost"
      recovered: true
      recovered_at: 2026-03-19T09:16:30Z
```

**恢复流程：**

```bash
$ vic auto resume

检测到上次会话在 DISPATCH-047 处中断
正在从检查点恢复...

✅ 已恢复：src/auth/login.ts (部分完成)
✅ 已恢复：tests/auth/login.test.ts (部分完成)

📍 继续任务：实现用户认证 API
⏳ 需要完成：
   1. 完成 login.ts 实现
   2. 编写 logout 功能
   3. 添加注册端点
```

---

### 2.9 引入自适应重规划

#### 问题

VIC-SDD 一旦 SPEC 锁定就无法调整，无法像 GSD-2 那样在切片完成后重新评估。

#### 改进方案：新增 adaptive-planning 机制

**触发条件：**

- 每个功能/模块完成后
- Research 发现与原假设矛盾时
- 用户明确要求调整

**工作流程：**

```bash
$ vic replan

📋 自适应重规划检查

检测到：用户认证模块已完成
新的研究发现：建议使用 NextAuth 而非原生 JWT

选项：
  [1] 保持当前设计（JWT）
  [2] 切换到 NextAuth（需要重构认证模块）
  [3] 评估后决定（查看影响分析）

请选择：2

⚠️ 影响分析：
  - 需要重构：auth/ 目录
  - 估计额外时间：2 小时
  - 收益：更好的安全性、减少维护负担

确认切换到 NextAuth？[y/N]
```

**变更记录：**

```yaml
# .vic-sdd/status/replan-log.yaml
replan_history:
  - timestamp: 2026-03-19T10:30:00Z
    trigger: research_discrepancy
    original: JWT authentication
    new: NextAuth
    reason: |
      NextAuth 提供开箱即用的安全最佳实践，
      减少约 40% 的认证代码维护工作。
    user_approved: true
    impact:
      estimated_hours: 2
      modules_affected: [auth]
```

---

### 2.10 AI 垃圾检测集成

#### 问题

VIC-SDD 缺少 gstack 的 AI 垃圾检测机制，无法识别和避免 AI 生成的代码模式。

#### 改进方案：增强 vic check

**新增检测规则：**

```yaml
# .vic-sdd/config/ai-slop-detector.yaml
ai_slop_detection:
  enabled: true
  severity_threshold: medium
  
  design_patterns:
    - id: D001
      pattern: "渐变 hero 区域"
      ai_score: high
      recommendation: "使用粗体排版或真实图片"
      
    - id: D002
      pattern: "三栏图标网格"
      ai_score: high
      recommendation: "非对称布局"
      
    - id: D003
      pattern: "统一圆角 (8px)"
      ai_score: medium
      recommendation: "按元素角色变化"
      
  code_patterns:
    - id: C001
      pattern: "// TODO: implement later"
      ai_score: high
      recommendation: "完成实现或创建 ticket"
      
    - id: C002
      pattern: "console.log 调试代码"
      ai_score: medium
      recommendation: "移除或替换为日志库"
      
    - id: C003
      pattern: "as any 类型断言"
      ai_score: high
      recommendation: "使用正确的类型定义"
```

**vic check 输出增强：**

```bash
$ vic check

───────────────────────────────────────────────────────
  📋 代码对齐检查报告
───────────────────────────────────────────────────────

  ✅ 规范对齐: 95%
  ⚠️  AI 垃圾检测: 发现 3 处问题

  [D001] 渐变 hero 区域
    文件: src/components/Hero.tsx
    建议: 使用粗体排版或真实图片

  [C002] 调试代码残留
    文件: src/utils/auth.ts:42
    建议: 移除 console.log

  [D002] 三栏图标网格
    文件: src/components/Features.tsx
    建议: 考虑非对称布局

───────────────────────────────────────────────────────
  建议操作: 
    $ vic fix --ai-slop  # 自动修复可安全修复的问题
    $ vic check --report  # 生成完整报告
```

---

## 三、整合后的 VIC-SDD 工作流

### 3.1 增强后的完整工作流

```
用户需求
    ↓
┌─────────────────────────────────────────────────────────────┐
│  vibe-redesign (产品重塑)                                    │
│  • 四模式探索：EXPANSION / SELECTIVE / HOLD / REDUCTION    │
│  • 找到「10星产品」                                          │
└─────────────────────────────────────────────────────────────┘
    ↓ 产品决策记录
┌─────────────────────────────────────────────────────────────┐
│  定图纸 (vibe-think)                                         │
│  • 需求澄清                                                   │
│  • 创建 SPEC-REQUIREMENTS.md                                 │
│  • Gate 0: 需求完整性检查                                     │
└─────────────────────────────────────────────────────────────┘
    ↓ 批准
┌─────────────────────────────────────────────────────────────┐
│  打地基 (vibe-architect)                                      │
│  • 技术选型                                                   │
│  • SPEC-ARCHITECTURE.md                                     │
│  • Gate 1: 架构完整性检查                                     │
└─────────────────────────────────────────────────────────────┘
    ↓ 批准
┌─────────────────────────────────────────────────────────────┐
│  vibe-design (可选)                                           │
│  • design-consultation: 从零构建设计系统                      │
│  • 生成 docs/DESIGN.md                                      │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  立规矩 (多个 skills 并行/顺序)                               │
│                                                              │
│  spec-test (TDD 强制)                                        │
│  • 红-绿-重构循环                                            │
│  • 每个功能必须先有测试                                       │
│                                                              │
│  spec-to-codebase (代码生成)                                  │
│  • 从 SPEC 生成实现                                          │
│  • Gate 2: 代码对齐检查                                       │
│                                                              │
│  vibe-qa (端到端测试)                                         │
│  • 浏览器自动化                                              │
│  • 自动回归测试                                              │
│  • Gate 4: E2E 验证                                         │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  adaptive-planning (自适应重规划)                             │
│  • 完成后重新评估计划                                        │
│  • 根据新信息调整                                            │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  Gate 3: 测试覆盖                                            │
│  • spec-driven-test                                         │
│  • 覆盖率检查                                                │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│  sdd-release-guard (发布守卫)                                │
│  • 最终检查                                                  │
│  • 准备发布                                                  │
└─────────────────────────────────────────────────────────────┘
    ↓
    合并 → PRD.md / ARCH.md / PROJECT.md
```

### 3.2 增强后的命令集

| 命令 | 别名 | 功能 | 来源 |
|------|------|------|------|
| `vic auto` | - | 启动自主模式 | 新增 (GSD-2) |
| `vic auto status` | - | 查看自主状态 | 新增 (GSD-2) |
| `vic auto pause` | - | 暂停自主模式 | 新增 (GSD-2) |
| `vic auto resume` | - | 恢复自主模式 | 新增 (GSD-2) |
| `vic replan` | - | 触发重规划 | 新增 (GSD-2) |
| `vic cost` | - | 查看成本追踪 | 新增 (GSD-2) |
| `vic qa` | - | 运行 QA 测试 | 新增 (gstack) |
| `vic qa --browser` | - | 浏览器测试 | 新增 (gstack) |
| `vic design review` | - | 设计审查 | 新增 (gstack) |
| `vic check --ai-slop` | - | AI 垃圾检测 | 新增 (gstack) |
| `vic fix --ai-slop` | - | 修复 AI 垃圾 | 新增 (gstack) |
| `vic debug` | - | 系统化调试 | 新增 (Superpowers) |
| `vic tdd` | - | 启用 TDD 模式 | 新增 (Superpowers) |

### 3.3 增强后的目录结构

```
project/
├── .vic-sdd/
│   ├── SPEC-REQUIREMENTS.md
│   ├── SPEC-ARCHITECTURE.md
│   ├── PROJECT.md
│   │
│   ├── status/
│   │   ├── state.yaml
│   │   ├── events.yaml
│   │   ├── gate-status.yaml
│   │   ├── cost.yaml          # 新增：成本追踪
│   │   ├── recovery.yaml      # 新增：崩溃恢复
│   │   └── replan-log.yaml    # 新增：重规划记录
│   │
│   ├── config/
│   │   ├── ai-slop-detector.yaml  # 新增：AI 垃圾检测
│   │   └── preferences.yaml
│   │
│   └── ...
│
├── docs/
│   ├── DESIGN.md              # 新增：设计系统
│   ├── PRODUCT-REDESIGN.md    # 新增：产品重塑
│   └── ...
│
└── skills/
    ├── sdd-orchestrator/
    ├── spec-architect/
    ├── spec-to-codebase/
    ├── spec-contract-diff/
    ├── spec-traceability/
    ├── spec-driven-test/
    ├── sdd-release-guard/
    │
    ├── vibe-think/            # 已有
    ├── vibe-architect/        # 已有
    ├── vibe-redesign/         # 新增 (gstack)
    ├── vibe-design/           # 新增 (gstack)
    ├── vibe-debug/            # 新增 (Superpowers)
    ├── vibe-qa/               # 新增 (gstack)
    ├── spec-test/             # 新增 (Superpowers)
    └── adaptive-planning/     # 新增 (GSD-2)
```

---

## 四、实施路线图

### Phase 1: 核心增强（1-2周）

1. **vic auto** - 自主执行模式
2. **cost tracking** - 成本追踪
3. **crash recovery** - 崩溃恢复

### Phase 2: 产品思维（2-3周）

4. **vibe-redesign** - 产品重塑
5. **adaptive-planning** - 自适应重规划
6. **tech-records 增强** - 产品决策记录

### Phase 3: 设计能力（2-3周）

7. **vibe-design** - 设计系统
8. **AI 垃圾检测** - vic check 增强
9. **design review** - 设计审查

### Phase 4: 测试增强（2-3周）

10. **spec-test** - TDD 强制
11. **vibe-debug** - 系统化调试
12. **vibe-qa** - 端到端测试

---

## 五、总结

通过结合三个开源项目的优点，VIC-SDD 可以进化为一个更加完善的 vibe coding 工作流系统：

| 改进项 | 来源 | 价值 |
|--------|------|------|
| 自主执行 | GSD-2 | 「设置后离开」体验 |
| 产品思维 | gstack | 找到真正产品 |
| 设计系统 | gstack | 避免 AI 垃圾 |
| TDD 强制 | Superpowers | 代码质量保证 |
| 系统化调试 | Superpowers | 根因修复 |
| 端到端测试 | gstack | 真实浏览器验证 |
| 成本追踪 | GSD-2 | 成本透明度 |
| 崩溃恢复 | GSD-2 | 可靠性 |
| 自适应重规划 | GSD-2 | 灵活性 |

最终，VIC-SDD 将成为一个兼具 **结构化纪律**（Gate 检查）、**产品思维**（重塑设计）、**设计美学**（设计系统）、**工程质量**（TDD/调试）、**自主能力**（状态机）和 **成本控制**（追踪账本）的完整 vibe coding 工作流系统。

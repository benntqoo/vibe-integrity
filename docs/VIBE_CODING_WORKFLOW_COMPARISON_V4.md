# Vibe Coding 工作流完整对比：Superpowers vs gstack vs GSD-2 vs VIC-SDD

## 一、共同的 Vibe Coding 工作流特性

尽管这四个项目的技术架构和使用形态不同，但它们在 vibe coding（氛围编程）工作流上存在显著的共性。这些共性代表了 AI 辅助开发的最佳实践。

### 1.1 需求理解 → 产品思维

所有四个系统都强调在写代码之前先理解「为什么」，而非「做什么」。

**Superpowers** 通过 **brainstorming** 技能实现。AI 不会直接开始写代码，而是通过结构化对话理解用户的真实需求。即使是看似简单的任务，也必须经过「设计阶段」，这基于一个核心认知：「未经验证的假设在最简单的项目中造成最大的浪费」。

**gstack** 的 **/plan-ceo-review** 进一步强化了这一理念。Garry Tan 将其称为「Brian Chesky 模式」—— AI 不仅要理解用户「说要什么」，还要帮助用户发现他们「真正需要什么」。

**GSD-2** 通过 **Research** 阶段实现。在每个切片（Slice）开始前，系统会研究代码库和相关文档，确保在开始实现前对项目有充分的理解。

**VIC-SDD** 通过 **定图纸** 阶段实现。系统使用 vibe-think skill 进行需求澄清，创建 SPEC-REQUIREMENTS.md 文档，包含用户故事、验收标准和 Phase 规划。

**共同价值：** 在 vibe coding 中，用户往往用模糊的自然语言描述需求。这四个系统都强制 AI 在实现前进行需求澄清，避免「用户说 A，AI 做成 B」的常见问题。

### 1.2 任务规划 → 分解与验证

四个系统都认为详细的规划是成功的基础。

**Superpowers** 的 **writing-plans** 要求生成的计划足够详细。每个任务被分解为 2-5 分钟的原子步骤，包含精确的文件路径、完整代码和验证命令。

**gstack** 有两个专门的规划技能：**/plan-eng-review** 负责技术架构设计，强制 AI 绘制系统图；**/plan-design-review** 负责设计审查。

**GSD-2** 将规划分为两层：Slice 层面分解为多个任务（Task），每个任务必须适合一个上下文窗口。任务包含 must-haves——可机械验证的结果。

**VIC-SDD** 使用 **打地基** 阶段。通过 vibe-architect skill 创建 SPEC-ARCHITECTURE.md，包含技术选型、模块划分、API 设计。每个功能都有明确的 Gate 检查点。

**共同价值：** 详细的规划不仅让执行更可控，也让审查和验证更容易。在 vibe coding 中，AI 容易「跑偏」，详细的规划提供了纠正的锚点。

### 1.3 验证 → 证据驱动

四个系统都强调「没有验证就不能声称成功」。

**Superpowers** 的 **verification-before-completion** 制定了铁律：任何完成声明必须伴随新鲜的验证证据。

**gstack** 的 **/review** 寻找那些「能通过 CI 但在生产中仍然会出问题」的 bug。同时 **/qa** 提供端到端测试能力。

**GSD-2** 的验证系统分为层级：静态检查 → 命令执行 → 行为测试 → 人工审查。配置 `verification_commands` 后，系统会在每个任务自动运行。

**VIC-SDD** 通过 **vic check** 和 **vic validate** 命令实现代码对齐检查。每个 Gate 有明确的验收标准矩阵。

**共同价值：** AI 容易对自己的工作过度自信。这四个系统都强制 AI 独立验证其输出，而非依赖「应该没问题」的假设。

### 1.4 审查 → 质量门禁

四个系统都设置了多层次的质量审查。

**Superpowers** 有完整的代码审查流程：两阶段审查（规范合规性 → 代码质量），requesting-code-review 在任务间触发。

**gstack** 的 **/review** 由「偏执的高级工程师」模式运行，会追踪每个新增的枚举值通过所有 switch 语句。

**GSD-2** 在所有切片完成后运行 `validate-milestone` 门控，比较路线图成功标准与实际结果。

**VIC-SDD** 使用 Gate 检查系统：Gate 0（需求完整性）、Gate 1（架构完整性）、Gate 2（代码对齐）、Gate 3（测试覆盖）。

**共同价值：** 在 vibe coding 中，AI 可能在不了解代码库复杂性的情况下写出「能工作但有隐患」的代码。审查流程提供了额外的安全网。

---

## 二、各自的独特 Vibe Coding 流程

### 2.1 Superpowers 独特流程

#### 2.1.1 TDD 强制循环

Superpowers 的 **test-driven-development** 技能是 vibe coding 中的独特存在。它强制 AI 遵循红-绿-重构循环。

#### 2.1.2 系统化调试方法论

**systematic-debugging** 技能提供四阶段调试流程：根因调查 → 模式分析 → 假设与测试 → 实现修复。

关键约束：如果已尝试三个以上的修复但都失败，AI 必须停下来质疑架构本身而非继续打补丁。

#### 2.1.3 硬性门槛机制

Superpowers 设置了多个不可绕过的硬性门槛：

- **brainstorming 门槛**：不批准设计就不能写代码
- **TDD 门槛**：测试不通过就不能写实现
- **verification 门槛**：没有验证证据就不能声称完成

### 2.2 gstack 独特流程

#### 2.2.1 产品重塑四模式

**/plan-ceo-review** 的独特之处在于其四工作模式：

- **SCOPE EXPANSION**：热情推荐雄心勃勃的版本
- **SELECTIVE EXPANSION**：中立地呈现机会
- **HOLD SCOPE**：严格审查现有计划
- **SCOPE REDUCTION**：找到最小可行版本

#### 2.2.2 设计系统从零构建

**/design-consultation** 是 gstack 独有的能力。当项目还没有设计系统时，AI 可以从零开始构建完整的设计系统。

#### 2.2.3 AI 垃圾检测

**/plan-design-review** 和 **/design-review** 包含 80 项设计审计，特别关注「AI 垃圾」模式。

#### 2.2.4 真正的浏览器自动化

gstack 的 **/browse** 和 **/qa** 技能提供了真正的端到端测试能力。

#### 2.2.5 工程回顾

**/retro** 每周分析提交历史，提供团队级别的回顾报告。

### 2.3 GSD-2 独特流程

#### 2.3.1 状态机驱动的自主执行

GSD-2 的 **/gsd auto** 是最独特的流程——完全由磁盘文件驱动的状态机。用户可以「设置后离开」。

#### 2.3.2 里程碑与切片层次

GSD-2 的工作层次是独特的：

- **Milestone（里程碑）**：可发运的版本，包含 4-10 个切片
- **Slice（切片）**：一个可演示的垂直能力，包含 1-7 个任务
- **Task（任务）**：适合一个上下文窗口的工作单元

#### 2.3.3 Git Worktree 隔离

每个里程碑在独立的 Git worktree 中运行。

#### 2.3.4 崩溃恢复 + 成本追踪

GSD-2 的状态持久化到磁盘，使得真正的崩溃恢复和完整成本追踪成为可能。

### 2.4 VIC-SDD 独特流程

#### 2.4.1 三阶段命名体系

VIC-SDD 最大的独特之处在于使用中国软件开发中常见的三阶段命名：

- **定图纸 (Requirements)**：需求澄清和凝固
- **打地基 (Architecture)**：技术架构设计
- **立规矩 (Implementation)**：代码实现和验证

这种命名方式更符合中文开发团队的直觉，也体现了「先想清楚再做」的理念。

#### 2.4.2 Gate 检查点系统

VIC-SDD 实现了完整的 Gate 检查机制：

| Gate | 名称 | 功能 |
|------|------|------|
| Gate 0 | 需求完整性 | 检查 SPEC-REQUIREMENTS.md 的完整性 |
| Gate 1 | 架构完整性 | 检查 SPEC-ARCHITECTURE.md 的完整性 |
| Gate 2 | 代码对齐 | 检查实现是否符合 SPEC 设计 |
| Gate 3 | 测试覆盖 | 检查测试是否覆盖关键路径 |

每个 Gate 都有明确的验收标准矩阵。

#### 2.4.3 状态持久化

VIC-SDD 的 `.vic-sdd/` 目录结构提供了完整的项目记忆：

```
.vic-sdd/
├── SPEC-REQUIREMENTS.md    # 需求规范
├── SPEC-ARCHITECTURE.md    # 架构规范
├── PROJECT.md              # 项目状态追踪
├── status/
│   ├── events.yaml        # 事件历史
│   ├── state.yaml         # 当前状态
│   ├── gate-status.yaml   # Gate 状态
│   └── progress.yaml      # 进度追踪
├── tech/
│   └── tech-records.yaml  # 技术决策记录
├── risk-zones.yaml        # 风险区域
├── project.yaml           # AI 快速参考
└── dependency-graph.yaml  # 模块依赖图
```

#### 2.4.4 CLI 工具驱动

VIC-SDD 提供完整的 CLI 工具（vic 命令）来驱动整个流程：

```bash
vic init                      # 初始化项目
vic spec init                 # 初始化 SPEC 文档
vic rt / vic record tech      # 记录技术决策
vic rr / vic record risk     # 记录风险
vic status                   # 显示项目状态
vic spec gate [0-3]          # 运行 Gate 检查
vic check                    # 代码对齐检查
vic validate                 # 完整验证
vic phase advance            # 推进阶段
```

#### 2.4.5 单入口编排器

VIC-SDD 的 **sdd-orchestrator** skill 是整个系统的单一入口控制器：

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
```

所有其他 SDD skills 必须通过编排器调用，确保严格的状态转换和审计追踪。

#### 2.4.6 AI 快速理解机制

VIC-SDD 设计了一套 AI 快速理解机制：当 AI 开始项目时，只需读取以下文件即可快速理解项目上下文：

```
1. .vic-sdd/PROJECT.md          → 项目状态、里程碑
2. .vic-sdd/SPEC-REQUIREMENTS.md → 需求、验收标准
3. .vic-sdd/SPEC-ARCHITECTURE.md → 架构、技术栈
4. .vic-sdd/risk-zones.yaml    → 高风险区域
```

这使得 AI 能在约 15 秒内理解项目背景。

---

## 三、工作流差异可视化

### 3.1 需求理解阶段

```
Superpowers:
需求 → brainstorming → 设计文档 → (审查循环) → 批准设计

gstack:
需求 → /plan-ceo-review → (四模式探索) → 重塑产品 → 设计文档

GSD-2:
需求 → Research → 理解代码库 → 研究外部文档 → 知识整合

VIC-SDD:
需求 → 定图纸 (vibe-think) → SPEC-REQUIREMENTS.md → Gate 0 检查
```

### 3.2 规划阶段

```
Superpowers:
设计 → writing-plans → 原子任务 → (审查循环) → 执行计划

gstack:
产品 → /plan-eng-review → 架构/数据流/图表 → 技术计划
     → /plan-design-review → 80项设计审计 → 设计计划

GSD-2:
研究 → Plan阶段 → Slice分解 → Task列表 → 每个Task有must-haves

VIC-SDD:
SPEC → 打地基 (vibe-architect) → SPEC-ARCHITECTURE.md → Gate 1 检查
```

### 3.3 执行阶段

```
Superpowers:
Task → subagent驱动 → 两阶段审查 → 完成 → 下一Task

gstack:
(用户使用AI在会话中执行代码)

GSD-2:
Task → 新鲜上下文 → 执行 → verification_commands → 摘要 → 下一Task

VIC-SDD:
SPEC → 代码生成 (spec-to-codebase) → 代码 → spec-contract-diff 检查
```

### 3.4 验证阶段

```
Superpowers:
→ verification-before-completion → 证据驱动 → 声称完成

gstack:
→ /review (Staff Engineer) → 找生产级bug
→ /qa (QA Lead) → 浏览器测试 → Bug修复 → 回归测试

GSD-2:
→ 验证层级 (静态→命令→行为→人工)
→ verification_commands 自动运行
→ 失败自动修复重试

VIC-SDD:
→ vic check → 代码对齐检查
→ vic validate → 完整验证
→ Gate 2 (代码对齐) + Gate 3 (测试覆盖)
```

### 3.5 审查阶段

```
Superpowers:
→ requesting-code-review → 计划合规 → 报告问题

gstack:
→ /review → 追踪枚举值 → 自动修复 → 升级模糊问题
→ /design-review → 80项审计 → 修复循环 → 前后截图

GSD-2:
→ 每Task后 → 代码质量
→ 所有Slice后 → validate-milestone → 比较成功标准vs实际结果

VIC-SDD:
→ vic spec gate 0 → 需求完整性
→ vic spec gate 1 → 架构完整性
→ vic spec gate 2 → 代码对齐
→ vic spec gate 3 → 测试覆盖
```

### 3.6 发布阶段

```
Superpowers:
→ finishing-a-development-branch → 合并/PR选择 → 清理

gstack:
→ /ship → 同步main → 测试 → 覆盖审计 → PR → (测试引导)

GSD-2:
→ Slice N完成 → 摘要 → 提交
→ 所有Slice完成 → validate-milestone → squash merge → worktree清理

VIC-SDD:
→ vic phase advance → 推进到下一阶段
→ vic spec merge → 合并到 PRD/ARCH/PROJECT
→ sdd-release-guard → 发布守卫检查
```

---

## 四、Vibe Coding 场景对比

### 4.1 简单功能实现

| 阶段 | Superpowers | gstack | GSD-2 | VIC-SDD |
|------|-------------|--------|-------|---------|
| 需求 | brainstorming (强制) | /plan-ceo-review (快速) | Research | 定图纸 (vibe-think) |
| 规划 | writing-plans | /plan-eng-review | Task分解 | 打地基 (vibe-architect) |
| 执行 | 子代理 | 用户会话 | 新鲜上下文 | 代码生成 (spec-to-codebase) |
| 验证 | verification | /qa | auto | vic check |
| 审查 | 代码审查 | /review | 里程碑门控 | Gate 0-3 |
| 发布 | 分支完成 | /ship | worktree merge | vic phase advance |

### 4.2 复杂系统设计

| 阶段 | Superpowers | gstack | GSD-2 | VIC-SDD |
|------|-------------|--------|-------|---------|
| 产品 | brainstorming | /plan-ceo-review + 四模式 | Research + 重估 | 定图纸 |
| 架构 | - | /plan-eng-review + 图表 | Plan → Slice | 打地基 + SPEC |
| 设计 | - | /design-consultation + /design-review | - | - |
| 验证 | verification | /review + /qa | milestone validation | Gate 2-3 |
| 交付 | 分支完成 | /ship | worktree merge | vic spec merge |

### 4.3 长时间自主开发

| 能力 | Superpowers | gstack | GSD-2 | VIC-SDD |
|------|-------------|--------|-------|---------|
| 多会话 | 需要手动 | 需要手动 | 磁盘状态持久化 | 状态文件持久化 |
| 崩溃恢复 | 无 | 无 | ✅ 完整恢复 | ✅ 状态恢复 |
| 成本追踪 | 无 | 无 | ✅ 完整追踪 | 有限 |
| 自主运行 | 部分 | 部分 | ✅ 完全自主 | 部分 |
| 进度可视化 | - | dashboard | overlay | vic status |

### 4.4 团队协作

| 能力 | Superpowers | gstack | GSD-2 | VIC-SDD |
|------|-------------|--------|-------|---------|
| 多用户 | - | - | ✅ unique IDs | ✅ 团队追踪 |
| 角色分工 | - | - | Team mode | AI 快速理解 |
| 决策记录 | - | - | - | ✅ tech-records.yaml |
| 风险记录 | - | - | - | ✅ risk-zones.yaml |
| 依赖追踪 | - | - | - | ✅ dependency-graph.yaml |

---

## 五、核心差异总结

### 5.1 核心理念差异

**Superpowers = 纪律优先**

核心理念：即使在 vibe coding 中，也要遵循软件工程的最佳实践。TDD，系统化调试、验证驱动——这些不是建议，而是强制。

**gstack = 产品思维优先**

核心理念：vibe coding 的目标不是写代码，而是构建产品。AI 首先要问「什么是真正产品」，然后用「10星产品」的标准来重新设计。

**GSD-2 = 自主优先**

核心理念：vibe coding 应该是「设置后离开」。状态机驱动的执行、崩溃恢复、成本追踪——这些让 AI 能够长时间自主工作。

**VIC-SDD = 结构化优先**

核心理念：vibe coding 需要结构化的护栏。Gate 检查、状态转换、决策记录——这些确保 AI 不会迷失在「 vibes」中。SPEC 文档是唯一的真实来源。

### 5.2 用户参与度

```
Superpowers: 用户全程参与 ←→ gstack: 用户引导方向 ←→ GSD-2: 设置后离开 ←→ VIC-SDD: 阶段门控驱动
```

### 5.3 适用场景

| 场景 | 推荐系统 |
|------|---------|
| 小功能，快速迭代 | Superpowers 或 gstack |
| 需要产品重塑 | gstack |
| 需要设计系统 | gstack |
| 需要端到端测试 | gstack |
| 长时间自主开发 | GSD-2 |
| 大型里程碑交付 | GSD-2 |
| 严格流程要求 | Superpowers 或 VIC-SDD |
| 成本敏感项目 | GSD-2 |
| 需要团队协作 | VIC-SDD |
| 需要决策追溯 | VIC-SDD |
| 需要 AI 快速理解项目 | VIC-SDD |

### 5.4 可以互补

这四个系统不是互斥的——它们的独特流程可以互补：

- 使用 **gstack** 的 /plan-ceo-review 进行产品重塑
- 使用 **Superpowers** 的 TDD 和验证流程
- 使用 **VIC-SDD** 的 SPEC 文档化和 Gate 检查
- 使用 **GSD-2** 的自主执行和里程碑管理
- 使用 **gstack** 的 /qa 进行最终浏览器测试

理想情况下，一个完整的 vibe coding 工作流可以结合这四个系统的最佳特性。

---

## 六、详细功能对比矩阵

| 功能 | Superpowers | gstack | GSD-2 | VIC-SDD |
|------|-------------|--------|-------|---------|
| **需求理解** | | | | |
| 强制设计阶段 | ✅ brainstorming | ✅ /plan-ceo-review | ✅ Research | ✅ 定图纸 |
| 产品思维 | 基础 | ✅ 四模式重塑 | 基础 | 基础 |
| 外部研究 | - | - | ✅ Researcher | - |
| **规划** | | | | |
| 任务分解 | ✅ writing-plans | ✅ /plan-eng-review | ✅ Slice → Task | ✅ 打地基 |
| 技术架构图 | - | ✅ 强制图表 | - | ✅ SPEC |
| 设计审查 | - | ✅ 80项审计 | - | - |
| **执行** | | | | |
| 子代理执行 | ✅ subagent | - | ✅ Worker | - |
| 新鲜上下文 | - | - | ✅ 每Task | - |
| TDD 强制 | ✅ 红-绿-重构 | - | - | - |
| 浏览器自动化 | - | ✅ /browse + /qa | - | - |
| **验证** | | | | |
| 验证命令 | ✅ verification | ✅ /review + /qa | ✅ verification | ✅ vic check |
| 证据驱动 | ✅ 铁律 | ✅ 完整 | ✅ 自动 | ✅ Gate |
| 自动化测试 | - | ✅ /qa | ✅ auto | - |
| **审查** | | | | |
| 代码审查 | ✅ 两阶段 | ✅ 生产级bug | 里程碑级 | ✅ Gate 2 |
| 视觉审查 | - | ✅ /design-review | - | - |
| **发布** | | | | |
| 发布命令 | ✅ /ship | ✅ /ship | ✅ /gsd auto | ✅ vic phase |
| Git 策略 | 基础 | 基础 | ✅ Worktree | - |
| **系统特性** | | | | |
| 状态持久化 | 会话 | 会话 | ✅ 磁盘 | ✅ .vic-sdd/ |
| 崩溃恢复 | - | - | ✅ 完整 | ✅ 状态恢复 |
| 成本追踪 | - | - | ✅ 完整 | 有限 |
| 自主运行 | 有限 | 有限 | ✅ 完全 | 有限 |
| **团队协作** | | | | |
| 决策记录 | - | - | ✅ DECISIONS.md | ✅ tech-records.yaml |
| 风险记录 | - | - | - | ✅ risk-zones.yaml |
| 依赖追踪 | - | - | - | ✅ dependency-graph.yaml |
| 团队模式 | - | - | ✅ | ✅ |
| **CLI 工具** | - | - | ✅ gsd CLI | ✅ vic CLI |
| Gate 检查 | - | - | ✅ milestone | ✅ vic spec gate |
| AI 快速理解 | - | - | - | ✅ project.yaml |

# Superpowers 项目核心模块与工作流闭环分析

## 一、项目概述

Superpowers 是一个完整的 AI 驱动软件开发工作流系统，基于一组可组合的「技能」（Skills）和初始指令构建。其核心理念是：**在执行任何任务前，AI 必须检查是否有相关的技能需要调用**，从而确保遵循一致的工作流程，而非凭直觉行事。

该项目的设计哲学强调「系统化优于随机化」——即使面对简单任务，也需要通过设计、计划、验证的完整闭环来确保质量。这种方法论被编码在各个 Skills 文件中，形成了一种可复用的 Agent 开发范式。

### 1.1 核心理念

Superpowers 的核心价值在于将软件工程的最佳实践编码为可强制执行的技能，而非依赖 AI 的「良好行为」。通过设计-计划-执行-验证-审查的闭环流程，以及根因分析、TDD、证据验证等关键原则，该系统显著提高了 AI 辅助开发的质量和可预测性。

### 1.2 支持平台

Superpowers 支持多平台集成，包括 Claude Code、Cursor、Codex、OpenCode 和 Gemini CLI，通过平台适配层来处理不同平台的工具差异。SessionStart 钩子在每次会话开始时注入 using-superpowers 技能，确保整个会话期间都能遵循工作流。

## 二、核心模块分类

### 2.1 元技能层（Meta Skills）

这一层的技能负责整个系统的调度和协调，是整个工作流的入口和基础。

**using-superpowers** 是整个系统的入口技能，它定义了一条核心铁律：**如果存在任何技能可能适用于当前任务，AI 必须调用该技能进行检查**。这条规则没有任何例外情况，AI 不能通过理性化来规避检查。该技能还定义了技能优先级的排序——过程类技能（brainstorming、debugging）优先于实现类技能（frontend-design、mcp-builder），以及用户指令的优先级金字塔：用户显式指令 > Superpowers 技能 > 默认系统提示。

**writing-skills** 则是关于如何创建新技能的元技能，定义了编写高质量技能的规范和测试方法。

### 2.2 需求与设计层

这一层负责在编写代码之前完成需求分析和设计工作。

**brainstorming** 是所有创造性工作的前置技能。当用户提出任何功能请求时，AI 不能直接开始写代码，而是必须通过一系列结构化的对话来提炼需求。该技能包含一个「硬性门槛」：在呈现设计并获得用户批准之前，禁止调用任何实现技能、编写代码或采取任何实现行动。这一层的设计流程非常精细：首先探索项目上下文，然后逐个提出澄清问题（一次只问一个），接着提出 2-3 种方案并说明取舍，最后分节展示设计以获得用户的增量批准。设计文档会被保存到指定路径，并经过专门的 spec-document-reviewer 子代理的审查循环，确保设计质量后才进入实现阶段。

### 2.3 规划层

在设计获得批准后，规划层负责将设计文档拆解为可执行的具体任务。

**writing-plans** 技能要求生成的计划足够详细，以至于一个「缺乏上下文判断力但技术熟练的初级工程师」也能按照计划执行。每个任务被分解为 2-5 分钟的原子步骤，每个步骤都包含精确的文件路径、完整的代码片段、以及验证命令。该技能特别强调 TDD 循环的完整性：写失败测试、运行确认失败、实现最小代码、运行确认通过、提交。同样，计划文档也需经过 plan-document-reviewer 子代理的审查循环才能进入执行阶段。

**executing-plans** 提供了两种执行模式的选择：子代理驱动开发（推荐）或批量执行带检查点。两者都能确保计划被忠实执行，而非凭直觉跳跃式前进。

### 2.4 执行层

执行层负责将计划转化为可工作的代码。

**subagent-driven-development** 是执行层的核心模式。它为每个任务分发一个全新的子代理，采用两阶段审查机制：首先验证实现是否符合规范，其次检查代码质量。子代理完成工作后，主代理进行审查，然后继续下一个任务。这种模式使得 AI 能够自主工作数小时而不偏离原始计划。

**dispatching-parallel-agents** 提供了并行执行多个独立任务的能力，适用于可以真正并行处理的工作单元。

**test-driven-development** 是整个执行层的质量基础。它强制遵循红-绿-重构循环：先写一个失败的测试，运行确认它失败，编写最小代码使其通过，运行确认通过，最后提交。该技能明确禁止在任何测试通过之前编写实现代码，这一铁律确保了测试覆盖率和对代码行为的信心。

### 2.5 质量保证层

这一层的技能确保交付物的质量达到标准。

**verification-before-completion** 制定了完成声明的铁律：**没有新鲜验证证据就不能声称完成**。这条规则涵盖所有变体——任何成功、满意或正面陈述工作状态之前，AI 必须运行完整的验证命令并展示输出。该技能列举了常见的失败模式：使用「应该」「可能」「看起来」这类词汇，在验证之前表达满意，或信任子代理的成功报告而不独立验证。

**requesting-code-review** 在任务之间触发，进行计划合规性检查并按严重程度报告问题。关键问题会阻止继续前进。

**receiving-code-review** 指导如何响应审查反馈，强调在实施建议之前进行技术验证，而非盲目服从。

### 2.6 调试层

**systematic-debugging** 是处理任何 bug、测试失败或意外行为的前置技能。它定义了一个四阶段方法论：根因调查（必须完成才能进入下一阶段）、模式分析（找到工作示例并比较差异）、假设与测试（形成单一假设并最小化测试）、实现修复（修复根因而非症状）。

该技能包含一个关键约束：如果已尝试三个以上的修复但都失败了，AI 必须停下来质疑架构本身而非继续打补丁。这防止了在根本架构问题上的无效循环。

### 2.7 分支与工作流管理层

**using-git-worktrees** 在设计批准后激活，创建隔离的工作空间在新分支上运行，验证干净的测试基线。

**finishing-a-development-branch** 在任务完成时激活，验证测试通过，呈现合并/PR/保留/丢弃的选择，并清理工作树。

## 三、工作流闭环

Superpowers 的工作流形成了一个清晰的闭环，从用户需求出发，经过设计、规划、执行、验证、审查，最终到达交付：

```
用户需求 → brainstorming（设计探索）→ 设计文档（已审查） 
    ↓
writing-plans（任务分解）→ 实现计划（已审查）
    ↓
subagent-driven-development / executing-plans（TDD 循环执行）
    ↓
verification-before-completion（验证）
    ↓
requesting-code-review / receiving-code-review（代码审查）
    ↓
finishing-a-development-branch（合并决策）
```

### 3.1 闭环特点

这个闭环的每个阶段都有明确的入口条件和出口条件。brainstorming 的终端状态是调用 writing-plans；writing-plans 的终端状态是调用 subagent-driven-development 或 executing-plans；每个实现任务都强制遵循 TDD 循环；任何完成声明必须先经过 verification-before-completion。这种结构确保了工作不会在某个阶段被跳过或绕过。

### 3.2 关键阶段说明

**设计探索阶段（brainstorming）**是所有创造性工作的起点。该阶段的核心目标是理解用户的真实需求，通过结构化的对话逐步提炼出完整的设计方案。AI 在此阶段扮演的是需求分析师的角色，而非实现者的角色。

**任务分解阶段（writing-plans）**将设计文档转化为可执行的任务清单。每个任务都被分解为原子级别的步骤，包含精确的文件路径、完整的代码和验证命令。这种粒度确保了任何 Agent 都能准确执行。

**执行阶段（subagent-driven-development）**是闭环中耗时最长的阶段。通过子代理分发和两阶段审查，确保每个任务都被正确实现且符合规范。

**验证阶段（verification-before-completion）**是质量防线的最后一道关口。任何完成声明都必须伴随新鲜的验证证据，这一条铁律贯穿整个工作流。

**审查阶段（requesting-code-review / receiving-code-review）**提供了额外的质量保障。通过人工或代理审查，确保代码不仅能工作，而且质量达标。

## 四、关键设计理念

### 4.1 证据优于声明

任何关于成功、正确或完成的断言都必须伴随新鲜的验证证据。在 verification-before-completion 和 systematic-debugging 中，这一原则被表述为不可违反的铁律。AI 不能使用「应该」「可能」「看起来」这类模糊词汇，也不能在运行验证命令之前表达满意。

### 4.2 根因优于症状

systematic-debugging 强制在提出任何修复之前完成根因调查。这防止了常见的「打补丁」模式，即临时修复表面问题而忽视根本原因，导致问题反复出现。该技能要求在进入修复阶段之前，必须完成根因调查、模式分析和假设测试四个阶段。

### 4.3 设计先行

brainstorming 设置了硬性门槛，要求在编写任何代码之前完成设计并获得批准。这并非官僚主义，而是因为「未examined的假设在最简单的项目中造成最大的浪费」。即使是看似简单的任务，也必须经过设计阶段的审视。

### 4.4 原子任务粒度

writing-plans 要求每个步骤都是 2-5 分钟的原子动作，包含精确的文件路径、完整代码和验证命令。这种粒度使得子代理能够可靠地执行，也使得审查和恢复变得简单可控。每个 TDD 循环都被拆解为独立的步骤：写测试、运行确认失败、实现、运行确认通过、提交。

### 4.5 强制流程而非建议

using-superpowers 的核心机制是技能自动触发，而非可选建议。如果有任何技能可能适用，AI 必须调用它——这不是选择，而是义务。该技能列出了常见的理性化思维，并明确标识为违反规则。

## 五、可复用模式提炼

基于对 Superpowers 的分析，可以提炼出几个可复用的模式用于构建类似的工作流系统。

### 5.1 技能触发模式

核心原则是「1% 可能性就调用」——如果存在技能可能适用的哪怕很小的概率，AI 也应该调用该技能进行检查。这通过 using-superpowers 中的红名单来强化，那些「我在理性化」的思维被明确标识为违反规则。

该模式的工作流程如下：用户消息接收 → 检查是否有技能可能适用 → 如果是，调用 Skill 工具 → 宣布使用该技能的目的 → 如有检查清单则为每个项目创建待办项 → 严格遵循技能执行。

### 5.2 审查循环模式

出现在 brainstorming 和 writing-plans 中。设计文档或实现计划完成后，会分发一个专门的审查代理进行质量检查，如果发现问题则修复后重新分发，直到通过或达到最大迭代次数（通常为 3 次）后升级给人工。这种循环确保了质量门槛在进入下一阶段之前被满足。

该模式的关键要素包括：专门的审查代理（而非主代理自己）、迭代次数限制、问题修复后重新分发、以及人工升级机制。

### 5.3 两阶段审查模式

是 subagent-driven-development 的核心。每个子代理完成后都经过两阶段审查：首先验证实现是否符合规范（spec compliance），其次检查代码质量（code quality）。这防止了仅仅「能工作」但质量不达标的代码进入代码库。

两阶段审查确保了实现既满足用户需求，又符合代码质量标准。规范合规性检查关注功能是否正确实现，代码质量检查关注代码的可读性、可维护性和最佳实践。

### 5.4 最小验证单元模式

在多个技能中出现。systematic-debugging 要求每次只改变一个变量来测试假设；test-driven-development 要求每个任务都从写失败的测试开始；verification-before-completion 要求每次都运行完整的验证命令。这些模式共同确保了可预测性和可追溯性。

该模式的核心思想是将复杂问题分解为可独立验证的最小单元，每个单元都可以被单独测试和验证。

### 5.5 硬性门槛模式

定义了不可绕过的工作流边界。brainstorming 的硬性门槛是「不批准设计就不能写代码」；test-driven-development 的硬性门槛是「测试不通过就不能写实现」；verification-before-completion 的硬性门槛是「没有验证证据就不能声称完成」。这些门槛构成了质量防线的最后堡垒。

硬性门槛通过强制执行特定顺序的步骤来确保流程不被跳过。每个门槛都有明确的触发条件和违反后果。

## 六、技术架构特点

### 6.1 技能系统架构

从技术实现角度看，Superpowers 的技能系统通过 Skill 工具进行调用，技能内容以 Markdown 格式存储在 skills 目录中。每个技能包含元数据（name、description）和详细的执行指南。技能之间通过特定的调用顺序形成工作流，后一个技能的触发是前一个技能的终端状态。

### 6.2 平台集成

该系统支持多平台集成，通过平台适配层来处理不同平台的工具差异。主要支持的平台包括 Claude Code（通过插件市场）、Cursor（通过插件市场）、Codex（通过安装脚本）、OpenCode（通过安装脚本）和 Gemini CLI（通过扩展）。

### 6.3 会话启动机制

SessionStart 钩子在每次会话开始时注入 using-superpowers 技能，确保整个会话期间都能遵循工作流。这种机制保证了工作流的连续性，即使在长会话中也不会偏离既定流程。

### 6.4 子代理调度

subagent-driven-development 采用了精心设计的子代理调度机制。每个任务都分发到一个全新的子代理，避免了上下文污染。两阶段审查确保了每个子代理的输出都经过严格把关。

## 七、Skills 目录结构参考

Superpowers 项目中的 skills 目录结构如下：

```
skills/
├── brainstorming/                    # 设计探索技能
│   ├── SKILL.md
│   ├── scripts/
│   ├── spec-document-reviewer-prompt.md
│   └── visual-companion.md
├── dispatching-parallel-agents/     # 并行代理调度
│   └── SKILL.md
├── executing-plans/                  # 执行计划
│   └── SKILL.md
├── finishing-a-development-branch/  # 完成开发分支
│   └── SKILL.md
├── receiving-code-review/            # 接收代码审查
│   └── SKILL.md
├── requesting-code-review/           # 请求代码审查
│   ├── SKILL.md
│   └── code-reviewer.md
├── subagent-driven-development/      # 子代理驱动开发
│   ├── SKILL.md
│   ├── code-quality-reviewer-prompt.md
│   ├── implementer-prompt.md
│   └── spec-reviewer-prompt.md
├── systematic-debugging/             # 系统化调试
│   ├── SKILL.md
│   ├── CREATION-LOG.md
│   ├── condition-based-waiting-example.ts
│   ├── condition-based-waiting.md
│   ├── defense-in-depth.md
│   ├── find-polluter.sh
│   ├── root-cause-tracing.md
│   ├── test-academic.md
│   ├── test-pressure-1.md
│   ├── test-pressure-2.md
│   └── test-pressure-3.md
├── test-driven-development/          # 测试驱动开发
│   ├── SKILL.md
│   └── testing-anti-patterns.md
├── using-git-worktrees/              # 使用 Git Worktrees
│   └── SKILL.md
├── using-superpowers/                # 使用 Superpowers
│   ├── SKILL.md
│   └── references/
├── verification-before-completion/   # 完成前验证
│   └── SKILL.md
├── writing-plans/                    # 编写计划
│   ├── SKILL.md
│   └── plan-document-reviewer-prompt.md
└── writing-skills/                  # 编写技能
    ├── SKILL.md
    ├── anthropic-best-practices.md
    ├── examples/
    ├── graphviz-conventions.dot
    ├── render-graphs.js
    ├── persuasion-principles.md
    └── testing-skills-with-subagents.md
```

## 八、总结与启示

Superpowers 提供了一个完整且经过实战检验的 AI 驱动开发工作流范式。其核心理念可以归纳为以下几点：

**第一，流程强制化。** 通过技能自动触发机制，确保关键工作流步骤不会被跳过或绕过。AI 无法通过「这太简单了」或「我直接开始吧」等理由逃避必要的设计和验证环节。

**第二，证据驱动。** 所有关于系统状态的声明都必须基于可验证的证据。这一原则贯穿整个工作流，从调试阶段的根因调查到完成阶段的验证声明。

**第三，粒度可控。** 通过将任务分解为原子级别的步骤，每个步骤都可独立验证和恢复。这种粒度使得大规模并行工作和自动化审查成为可能。

**第四，循环迭代。** 关键阶段都设置了审查循环，通过迭代改进确保质量。设计需要经过审查循环，计划需要经过审查循环，代码实现也需要经过审查循环。

**第五，平台无关。** 技能系统的设计考虑了多平台兼容性，通过抽象的工具层来适配不同的 AI 编码环境。

这种工作流范式对于构建其他领域的 AI 工作流系统具有重要的参考价值。无论是构建 DevOps 自动化、数据分析流程还是其他类型的 AI 辅助工作流，Superpowers 的核心原则——强制流程、证据驱动、粒度可控、循环迭代——都可以提供有益的指导。

# SkillFlow SDD Toolkit

[English README](./README.md)

SkillFlow SDD Toolkit 是一套可开源复用的 **严格 Spec-Driven Development（SDD）技能工具集**。  
它通过状态机编排与关卡校验，把特性交付过程从“经验驱动”升级为“可追踪、可验证、可发布”。

## 为什么使用这套工具

- 统一状态流转：`Ideation -> SpecDraft -> SpecValidated -> CodeGenerated -> Implemented -> ContractVerified -> Released`
- 统一产物约束：规格、契约、测试、追踪矩阵、发布守门报告
- 统一机器校验：`validate-sdd.py` 自动检查技能一致性与关卡完整性
- 兼容多工具目录：支持单层与多层 `skills` 结构

## 技能清单

- `sdd-orchestrator`：状态机入口与路由控制
- `spec-architect`：规格与契约设计
- `spec-to-codebase`：从规格生成实现
- `spec-contract-diff`：契约漂移检测
- `spec-driven-test`：基于规格的测试关卡
- `spec-traceability`：需求-契约-代码-测试追踪
- `sdd-release-guard`：发布前最终守门

## 目录结构

```text
skills/
  sdd-orchestrator/
    sdd-machine-schema.json
    sdd-gate-checklist.json
    validate-sdd.py
    validate-sdd.config.single-layer.json
    validate-sdd.config.multi-layer.json
  spec-architect/
  spec-to-codebase/
  spec-contract-diff/
  spec-driven-test/
  spec-traceability/
  sdd-release-guard/
```

## 快速开始

1) 默认校验（扫描 `<root>/skills`）：

```bash
python skills/sdd-orchestrator/validate-sdd.py
```

2) 使用单层目录模板：

```bash
python skills/sdd-orchestrator/validate-sdd.py --config skills/sdd-orchestrator/validate-sdd.config.single-layer.json
```

3) 使用多层目录模板：

```bash
python skills/sdd-orchestrator/validate-sdd.py --config skills/sdd-orchestrator/validate-sdd.config.multi-layer.json
```

## 示例输出

```text
SDD validation passed
Root: D:\Code\aaa
Skills paths:
- D:\Code\aaa\skills
Schema: D:\Code\aaa\skills\sdd-orchestrator\sdd-machine-schema.json
Checklist: D:\Code\aaa\skills\sdd-orchestrator\sdd-gate-checklist.json
```

出现 `SDD validation passed` 时，表示技能覆盖、状态枚举与关卡清单结构均已通过一致性检查。

## 配置方式

`validate-sdd.py` 支持三类配置来源：命令参数、环境变量、JSON 配置文件。

优先级：

- `root_path`：命令参数 > 环境变量 > 配置文件 > 脚本默认
- `skills_paths`：命令参数 + 环境变量 + 配置文件合并去重

常用参数：

- `--root-path`
- `--skills-path`（可重复传入）
- `--orchestrator-path`
- `--schema-path`
- `--checklist-path`
- `--recursive-search true|false`
- `--config <json>`

环境变量：

- `SDD_VALIDATE_CONFIG`
- `SDD_ROOT_PATH`
- `SDD_SKILLS_PATHS`
- `SDD_ORCHESTRATOR_PATH`
- `SDD_SCHEMA_PATH`
- `SDD_CHECKLIST_PATH`
- `SDD_RECURSIVE_SEARCH`

## 常见失败与排查

- `Unable to resolve sdd-orchestrator path from configured skills paths`
  - 检查 `skills_paths` 是否指向真实技能根目录
  - 检查 `sdd-orchestrator` 是否包含 `sdd-machine-schema.json` 与 `sdd-gate-checklist.json`
- `SKILL.md not found for <skill>`
  - 检查目标技能目录是否存在
  - 多层目录结构请启用 `--recursive-search true`
- `missing schema reference` 或 `missing checklist reference`
  - 检查技能 `SKILL.md` 是否包含 schema 与 checklist 引用
- `State enum mismatch between schema and checklist`
  - 对齐 `sdd-machine-schema.json` 与 `sdd-gate-checklist.json` 的状态枚举
- `Checklist section incomplete for <skill>`
  - 检查 checklist 是否包含 `entry_state`、`required_outputs`、`gate_checks`

## 开源发布建议

- 技能目录统一放在项目根 `skills/`
- 避免使用工具私有路径（例如 `.trae/skills/`）
- 每次发布前执行校验脚本
- `LICENSE` 与 `.gitignore` 与功能变更一起提交

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](./LICENSE)。

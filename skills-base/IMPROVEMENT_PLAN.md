# Skills 完整改进计划

## 目标

将 `skills-base` 和 `skills-sdd` 从文档描述转化为**可执行的技能系统**，实现：
1. Skill 可发现、可注册、可调用
2. 完整的工作流协调
3. 统一的配置和路径规范
4. 可靠的运行时机制

---

## 阶段一：基础设施（Foundation）

### 1.1 Skill 元信息标准

**目标**：统一 skill 定义格式，实现自动发现和注册

```
# 新增: skills-base/skill-registry.json
{
  "version": "1.0.0",
  "skills": [
    {
      "id": "vibe-guard",
      "name": "vibe-guard",
      "category": "completion-guard",
      "description": "AI completion integrity checker",
      "implementation": "skills-base/vibe-guard/validate-vibe-guard.py",
      "entry_points": ["--check", "--mode"],
      "dependencies": [],
      "outputs": [".sdd-spec/vibe-guard-report.json"]
    },
    {
      "id": "vibe-design",
      "name": "vibe-design", 
      "category": "architecture-memory",
      "description": "Requirement clarification and design helper",
      "implementation": "skills-base/vibe-design/vibe-design.py",
      "entry_points": ["--clarify", "--interactive"],
      "dependencies": ["vibe-integrity-writer"]
    }
  ]
}
```

**文件位置**：`skills-base/skill-registry.json`

### 1.2 统一路径规范

**问题**：
- `skills-base/` - 基础能力（完成守卫、架构记忆）
- `skills-sdd/` - SDD 工作流
- 文档中混用 `skills/`、`skills-base/`、`skills-sdd/`

**解决方案**：

```
skills-base/           # 基础能力目录
├── skill-registry.json    # 新增：统一注册表
├── vibe-guard/        # 完成守卫
│   ├── SKILL.md
│   ├── validate-vibe-guard.py
│   └── vibe-guard.config.json    # 新增
├── vibe-design/       # 需求澄清（新增代码）
│   ├── SKILL.md
│   └── vibe-design.py
├── vibe-integrity-debug/  # 调试辅助（新增代码）
│   ├── SKILL.md
│   └── vibe-integrity_debug.py
├── vibe-integrity-writer/  # YAML 写入器
│   ├── SKILL.md
│   └── vibe-integrity-writer.py
├── vibe-integrity/    # 验证框架
│   ├── SKILL.md
│   └── validate-vibe-integrity.py
└── templates/         # 新增：YAML 模板
    ├── project.schema.json
    ├── tech-records.schema.json
    └── ...

skills-sdd/           # SDD 工作流目录（保持不变）
├── sdd-orchestrator/
├── spec-architect/
├── spec-to-codebase/
└── ...
```

### 1.3 创建缺失配置文件

**vibe-guard.config.json**：
```json
{
  "mode": "standard",
  "auto_trigger": true,
  "trigger_phrases": ["done", "ready", "complete", "finished", "完成"],
  "grace_period_minutes": 10,
  "skip_if_no_changes": true,
  "checks": {
    "completeness": {
      "scan_todo": true,
      "scan_stub": true,
      "severity_by_mode": {
        "vibe": "warning",
        "standard": "warning", 
        "strict": "error"
      }
    }
  },
  "file_patterns": {
    "scan": ["**/*.ts", "**/*.js", "**/*.py"],
    "exclude": ["node_modules/**", "dist/**"]
  },
  "output": {
    "report_file": ".sdd-spec/vibe-guard-report.json"
  }
}
```

---

## 阶段二：Skill 实现（Implementation）

### 2.1 vibe-design 实现

**功能**：
1. 交互式需求澄清对话
2. 决策自动记录到 .vibe-integrity/
3. 生成设计摘要文档

**核心文件**：`skills-base/vibe-design/vibe-design.py`

```python
# 伪代码结构
class VibeDesign:
    def __init__(self):
        self.writer = VibeIntegrityWriter()
        self.questions = [...]  # 苏格拉底式提问模板
        
    def start_clarification(self, user_input):
        """启动需求澄清"""
        # 1. 检查现有 .vibe-integrity/ 上下文
        # 2. 生成第一个澄清问题
        # 3. 循环直到需求清晰
        
    def record_decision(self, decision_type, data):
        """记录决策到对应 YAML"""
        self.writer.write(decision_type, data)
        
    def generate_summary(self):
        """生成设计摘要"""
        # 输出到 docs/plans/YYYY-MM-DD-<topic>-design.md
```

### 2.2 vibe-integrity-debug 实现

**功能**：
1. 四阶段系统调试流程
2. 根因分析验证
3. 风险自动记录

**核心文件**：`skills-base/vibe-integrity-debug/vibe_integrity_debug.py`

### 2.3 skill 调用协议

**目标**：定义跨 skill 通信标准

**协议格式**：
```json
{
  "protocol_version": "1.0.0",
  "caller": "vibe-design",
  "callee": "vibe-integrity-writer",
  "operation": "add_record",
  "payload": {
    "target_file": "tech-records.yaml",
    "data": {...}
  },
  "callback": {
    "on_success": "continue",
    "on_failure": "abort"
  }
}
```

**调用接口**：`skills-base/skill-bus.py`（新增）
```python
class SkillBus:
    """Skill 间通信总线"""
    
    async def call_skill(self, callee: str, payload: dict) -> dict:
        """调用另一个 skill"""
        
    def register_handler(self, skill_id: str, handler: callable):
        """注册 skill 处理函数"""
```

---

## 阶段三：集成机制（Integration）

### 3.1 自动触发系统

**架构**：
```
skill-trigger/
├── trigger-manager.py    # 触发器管理器
├── phrase-detector.py    # 完成词检测
├── state-monitor.py      # SDD 状态监控
└── webhook-server.py     # 可选：Webhook 接收器
```

**触发条件**：
1. 短语检测（done, ready, complete...）
2. SDD 状态转换
3. 手动触发
4. 定时检查（可选）

### 3.2 状态持久化

**SDD 状态** → `.sdd-spec/specs/<feature>.state.json`
```json
{
  "feature": "user-auth",
  "current_state": "Build",
  "history": [
    {"state": "Ideation", "timestamp": "...", "skill": "spec-architect"},
    {"state": "Explore", "timestamp": "...", "skill": "spec-architect"}
  ],
  "artifacts": ["spec.json", "contracts.yaml"]
}
```

### 3.3 统一 CLI 入口

**文件**：`skills-base/cli.py`

```bash
# 统一入口
python -m skills-base.cli <command> [options]

# 示例
python -m skills-base.cli vibe-guard --check
python -m skills-base.cli vibe-design --clarify "实现用户登录"
python -m skills-base.cli vibe-debug --analyze "登录失败"
python -m skills-base.cli sdd-orchestrator --start feature-name
python -m skills-base.cli validate --all
```

---

## 阶段四：协作增强（Collaboration）

### 4.1 改进文件锁

**问题**：Windows 兼容性差

**方案**：使用跨平台锁库
```python
# 使用 filelock 库（跨平台）
from filelock import FileLock

lock = FileLock("task.lock", timeout=10)
with lock:
    # 安全的文件操作
```

### 4.2 冲突自动解决

**策略**：
1. **ID 冲突**：自动追加后缀（DB-001 → DB-001-v2）
2. **内容冲突**：保留两者，标记需人工审查
3. **语义冲突**：记录到 conflict-journal.yaml

### 4.3 Agent 追踪 schema

**新增**：`skills-base/schemas/agent-metadata.schema.json`
```json
{
  "agent_metadata": {
    "agent_id": "uuid",
    "session_id": "uuid", 
    "timestamp": "iso8601",
    "branch": "string",
    "action": "add|update|delete"
  }
}
```

---

## 实施顺序

| 阶段 | 任务 | 优先级 | 预估工作 |
|------|------|--------|----------|
| **1** | 创建 skill-registry.json | P0 | 1h |
| **1** | 统一路径规范 | P0 | 2h |
| **1** | 创建 vibe-guard.config.json | P1 | 1h |
| **2** | 实现 vibe-design.py | P0 | 8h |
| **2** | 实现 vibe_integrity_debug.py | P0 | 8h |
| **2** | 实现 skill-bus.py | P0 | 4h |
| **3** | 实现自动触发系统 | P1 | 6h |
| **3** | 创建统一 CLI | P1 | 3h |
| **4** | 改进文件锁兼容性 | P2 | 2h |
| **4** | 冲突自动解决 | P2 | 4h |

**总预估**：约 39 小时

---

## 验收标准

### 阶段一完成
- [ ] `python skills-base/skill-registry.json` 可被解析
- [ ] 所有路径引用统一到 `skills-base/` 和 `skills-sdd/`
- [ ] vibe-guard 可读取配置文件

### 阶段二完成
- [ ] `python skills-base/vibe-design/vibe-design.py --clarify` 可运行
- [ ] vibe-design 决策可写入 .vibe-integrity/
- [ ] skill-bus 可协调跨 skill 调用

### 阶段三完成
- [ ] vibe-guard 可检测完成词自动触发
- [ ] SDD 状态正确持久化
- [ ] 统一 CLI 可用

### 阶段四完成
- [ ] 文件锁在 Windows/Linux 正常工作
- [ ] 冲突检测和解决自动化

---

## 风险与依赖

| 风险 | 影响 | 缓解 |
|------|------|------|
| OpenCode 不支持自定义 skill 调用 | 无法真正执行 | 先实现 CLI 工具，可独立运行 |
| 多 skill 状态一致性 | 数据不一致 | 使用事务和锁 |
| 跨平台文件锁 | Windows 兼容 | 使用 filelock 库 |


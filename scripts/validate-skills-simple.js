#!/usr/bin/env node

/**
 * Skills 简单验证脚本
 * 用于验证 SKILL.md 格式和 references 文件
 */

const fs = require('fs');
const path = require('path');

// Skills 目录
const SKILLS_DIR = path.join(__dirname, '../skills');

// 验证规则
const VALIDATION_RULES = {
  // 必须的章节
  requiredSections: [
    'Overview',
    'L1: When to Use',
    'L1: Auto-Activate Triggers',
    'L2: How to Use',
    'Vic Commands',
    'L3: References'
  ],

  // references 必须包含的文件
  requiredReferences: {
    'context-tracker': ['confidence-formula.md', 'blocker-types.md', 'examples.md', 'troubleshooting.md'],
    'spec-workflow': ['spec-workflow-guide.md', 'examples.md', 'templates.md'],
    'implementation': ['implementation-guide.md', 'examples.md', 'troubleshooting.md'],
    'unified-workflow': ['unified-workflow-guide.md', 'sdd-state-machine.md', 'constitution-rules.md', 'traceability-patterns.md', 'examples.md'],
    'quick': ['quick-guide.md', 'examples.md', 'escalation.md']
  }
};

// 检查文件是否存在
function fileExists(filePath) {
  return fs.existsSync(filePath);
}

// 提取章节标题
function extractSections(content) {
  const sections = [];
  const regex = /^## (.+)$/gm;
  let match;

  while ((match = regex.exec(content)) !== null) {
    sections.push(match[1]);
  }

  return sections;
}

// 验证单个 skill
function validateSkill(skillName, skillDir) {
  const skillFile = path.join(skillDir, 'SKILL.md');
  const referencesDir = path.join(skillDir, 'references');

  const issues = [];

  // 1. 检查 SKILL.md 文件是否存在
  if (!fileExists(skillFile)) {
    issues.push(`❌ SKILL.md 文件不存在`);
    return issues;
  }

  // 2. 读取文件内容
  const content = fs.readFileSync(skillFile, 'utf8');

  // 3. 检查是否有 YAML frontmatter
  const hasYaml = content.startsWith('---\n');
  if (!hasYaml) {
    issues.push(`❌ 缺少 YAML frontmatter`);
  }

  // 4. 验证章节
  const sections = extractSections(content);
  for (const section of VALIDATION_RULES.requiredSections) {
    if (!sections.includes(section)) {
      issues.push(`❌ 缺少章节: ${section}`);
    }
  }

  // 5. 检查 When to Use 表格格式
  const hasWhenToUseSection = sections.includes('L1: When to Use');
  if (!hasWhenToUseSection) {
    issues.push(`❌ 缺少章节: L1: When to Use`);
  } else {
    const sectionStart = content.indexOf('## L1: When to Use');
    const sectionEnd = content.indexOf('##', sectionStart + 1);
    const sectionContent = content.substring(sectionStart, sectionEnd);
    const hasSituationColumn = sectionContent.includes('| Situation |');
    const hasUseSkillColumn = sectionContent.includes('| Use Skill? |');

    if (!hasSituationColumn || !hasUseSkillColumn) {
      issues.push(`❌ 'L1: When to Use' 表格格式不正确`);
    }
  }

  // 6. 验证 references
  if (fileExists(referencesDir)) {
    const refFiles = fs.readdirSync(referencesDir);
    const requiredRefs = VALIDATION_RULES.requiredReferences[skillName] || [];

    for (const requiredRef of requiredRefs) {
      if (!refFiles.includes(requiredRef)) {
        issues.push(`❌ 缺少 reference 文件: ${requiredRef}`);
      }
    }
  } else {
    issues.push(`❌ references 目录不存在`);
  }

  return issues;
}

// 主函数
function main() {
  console.log('🔍 开始验证 Skills (简化版)...\n');

  const skills = ['context-tracker', 'spec-workflow', 'implementation', 'unified-workflow', 'quick'];
  let totalIssues = 0;

  for (const skill of skills) {
    console.log(`\n📁 验证 Skill: ${skill}`);
    console.log('='.repeat(50));

    const skillDir = path.join(SKILLS_DIR, skill);
    const issues = validateSkill(skill, skillDir);

    if (issues.length === 0) {
      console.log('✅ 验证通过！');
    } else {
      console.log(`❌ 发现 ${issues.length} 个问题:`);
      issues.forEach(issue => console.log(`  ${issue}`));
      totalIssues += issues.length;
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log(`📊 验证总结:`);
  console.log(`- 总检查: ${skills.length} 个 skills`);
  console.log(`- 发现问题: ${totalIssues} 个`);

  if (totalIssues === 0) {
    console.log('🎉 所有 Skills 验证通过！');
    process.exit(0);
  } else {
    console.log('⚠️  需要修复上述问题');
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main();
}

module.exports = { validateSkill, VALIDATION_RULES };
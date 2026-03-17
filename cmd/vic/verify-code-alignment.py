#!/usr/bin/env python3
"""
Verify Code Alignment - Lightweight code-to-decision verification
=================================================================

Validates that actual code implementation matches recorded decisions.
This is a LIGHTWEIGHT check - not exhaustive analysis.

Usage:
    python verify-code-alignment.py                    # Check all
    python verify-code-alignment.py --category database # Check specific category
    python verify-code-alignment.py --json             # JSON output
"""

import os
import re
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    UNKNOWN = "unknown"


@dataclass
class CheckResult:
    """Result of a single alignment check"""
    record_id: str
    category: str
    decision: str
    status: CheckStatus
    message: str
    details: Optional[Dict[str, Any]] = None


class CodeAlignmentChecker:
    """Lightweight checker for code-to-decision alignment"""
    
    # Comprehensive patterns to detect technology usage in code
    # Format: category -> technology -> list of regex patterns
    TECH_PATTERNS: Dict[str, Dict[str, List[str]]] = {
        # ============================================
        # DATABASE
        # ============================================
        'database': {
            'postgresql': [
                r'postgres',
                r'psycopg',
                r'psycopg2',
                r'pg\.',
                r'postgresql://',
                r'Prisma.*postgresql',
                r'database.*postgres',
                r'dialect.*postgres',
            ],
            'mysql': [
                r'mysql',
                r'mysql2',
                r'mariadb',
                r'pymysql',
                r'mysql://',
                r'dialect.*mysql',
            ],
            'sqlite': [
                r'sqlite',
                r'\.db["\']',
                r'sqlite3',
                r'sqlite://',
                r'better-sqlite',
            ],
            'mongodb': [
                r'mongodb',
                r'mongoose',
                r'MongoClient',
                r'mongodb://',
                r'@nestjs/mongoose',
            ],
            'redis': [
                r'redis',
                r'ioredis',
                r'redis://',
                r'connect-redis',
                r'@upstash/redis',
            ],
            'prisma': [
                r'prisma',
                r'@prisma/client',
                r'PrismaClient',
                r'schema\.prisma',
            ],
            'typeorm': [
                r'typeorm',
                r'@typeorm',
                r'DataSource',
                r'Entity\(',
            ],
            'sequelize': [
                r'sequelize',
                r'Sequelize\(',
                r'DataTypes\.',
            ],
            'drizzle': [
                r'drizzle',
                r'drizzle-orm',
                r'drizzle-kit',
            ],
        },
        
        # ============================================
        # AUTHENTICATION
        # ============================================
        'auth': {
            'jwt': [
                r'jwt',
                r'jsonwebtoken',
                r'Bearer\s+',
                r'jwt\.sign',
                r'jwt\.verify',
                r'@fastify/jwt',
                r'express-jwt',
            ],
            'oauth': [
                r'oauth',
                r'passport',
                r'NextAuth',
                r'Auth0',
                r'@auth0',
                r'oauth2',
                r'Clerk',
                r'@clerk',
            ],
            'session': [
                r'express-session',
                r'cookie-session',
                r'express-cookie',
                r'session\s*=',
            ],
            'bcrypt': [
                r'bcrypt',
                r'bcryptjs',
                r'hash\(',
                r'compare\(',
            ],
            'cryptography': [
                r'crypto',
                r'node-forge',
                r'tweetnacl',
                r'argon2',
            ],
            'clerk': [
                r'clerk',
                r'@clerk/nextjs',
                r'@clerk/clerk-react',
            ],
            'nextauth': [
                r'next-auth',
                r'NextAuth',
                r'getServerSession',
            ],
        },
        
        # ============================================
        # FRONTEND FRAMEWORKS
        # ============================================
        'frontend': {
            'vue': [
                r'vue',
                r'Vue\.',
                r'createApp',
                r'<template>',
                r'@vue/',
                r'vue@',
                r'pinia',
            ],
            'react': [
                r'\breact\b',
                r'React\.',
                r'jsx',
                r'useState',
                r'useEffect',
                r'@react',
                r'react-dom',
            ],
            'angular': [
                r'@angular',
                r'NgModule',
                r'Component\(',
                r'angular/core',
            ],
            'svelte': [
                r'svelte',
                r'@svelte',
                r'\.svelte',
            ],
            'solid': [
                r'solid-js',
                r'@solid',
                r'createSignal',
            ],
            'qwik': [
                r'@builder\.io/qwik',
                r'\$\(\'',
                r'useSignal',
            ],
            'astro': [
                r'astro',
                r'@astro',
                r'\.astro',
            ],
            'next.js': [
                r'next',
                r'next/link',
                r'next/navigation',
                r'next/head',
                r'getServerSideProps',
                r'getStaticProps',
            ],
            'nuxt': [
                r'nuxt',
                r'@nuxt',
                r'defineNuxtConfig',
                r'useNuxtApp',
            ],
            'remix': [
                r'@remix-run',
                r'remix',
                r'loader\(',
                r'action\(',
            ],
            'sveltekit': [
                r'@sveltejs/kit',
                r'\+page\.svelte',
                r'\+layout\.svelte',
            ],
        },
        
        # ============================================
        # STYLING
        # ============================================
        'styling': {
            'tailwind': [
                r'tailwind',
                r'tailwindcss',
                r'@tailwind',
                r'class="\S+"',
                r'className="\S+"',
            ],
            'css-modules': [
                r'\.module\.css',
                r'styles\.',
                r'css-modules',
            ],
            'styled-components': [
                r'styled-components',
                r'styled\.',
                r'css`',
            ],
            'emotion': [
                r'@emotion',
                r'css\s*\(',
                r'styled\s*\(',
            ],
            'sass': [
                r'sass',
                r'scss',
                r'\.scss',
                r'\.sass',
            ],
            'chakra': [
                r'@chakra-ui',
                r'chakra',
                r'ChakraProvider',
            ],
            'mui': [
                r'@mui',
                r'@material-ui',
                r'Mui',
            ],
            'shadcn': [
                r'shadcn',
                r'@radix-ui',
                r'components/ui',
            ],
        },
        
        # ============================================
        # TESTING
        # ============================================
        'testing': {
            'jest': [
                r'jest',
                r'describe\s*\(',
                r'it\s*\(',
                r'test\s*\(',
                r'expect\s*\(',
                r'@testing-library',
            ],
            'vitest': [
                r'vitest',
                r'vi\.',
                r'vitest\.config',
            ],
            'pytest': [
                r'pytest',
                r'def test_',
                r'assert\s+',
                r'unittest',
                r'conftest',
            ],
            'cypress': [
                r'cypress',
                r'cy\.',
                r'cy\.visit',
                r'cy\.get',
            ],
            'playwright': [
                r'playwright',
                r'@playwright',
                r'page\.',
                r'expect\s*\(\s*page',
            ],
            'mocha': [
                r'mocha',
                r'describe\s*\(',
                r'before\s*\(',
                r'after\s*\(',
            ],
            'karma': [
                r'karma',
                r'karma\.conf',
            ],
            'storybook': [
                r'storybook',
                r'@storybook',
                r'\.stories\.',
                r'\.story\.',
            ],
        },
        
        # ============================================
        # STATE MANAGEMENT
        # ============================================
        'state': {
            'redux': [
                r'redux',
                r'@reduxjs',
                r'createStore',
                r'useDispatch',
                r'useSelector',
            ],
            'zustand': [
                r'zustand',
                r'create\s*<',
                r'useStore',
            ],
            'mobx': [
                r'mobx',
                r'makeObservable',
                r'@observable',
                r'observer',
            ],
            'pinia': [
                r'pinia',
                r'defineStore',
                r'usePinia',
            ],
            'recoil': [
                r'recoil',
                r'atom\(',
                r'useRecoilState',
            ],
            'jotai': [
                r'jotai',
                r'atom\(',
                r'useAtom',
            ],
            'xstate': [
                r'xstate',
                r'createMachine',
                r'useMachine',
            ],
        },
        
        # ============================================
        # API / BACKEND
        # ============================================
        'api': {
            'express': [
                r'express',
                r'express\(\)',
                r'router\.',
                r'app\.get\(',
                r'app\.post\(',
            ],
            'fastify': [
                r'fastify',
                r'fastify\(\)',
                r'fastify\.get\(',
                r'fastify\.post\(',
            ],
            'nestjs': [
                r'@nestjs',
                r'@Controller',
                r'@Module',
                r'@Injectable',
            ],
            'hono': [
                r'hono',
                r'new Hono',
                r'Hono\(\)',
            ],
            'trpc': [
                r'trpc',
                r'@trpc',
                r'initTRPC',
                r'router\.',
            ],
            'graphql': [
                r'graphql',
                r'gql`',
                r'GraphQL',
                r'apollo',
                r'@apollo',
            ],
            'fastapi': [
                r'fastapi',
                r'FastAPI\(',
                r'@app\.get',
                r'@app\.post',
            ],
            'flask': [
                r'flask',
                r'Flask\(',
                r'@app\.route',
            ],
            'django': [
                r'django',
                r'DJANGO',
                r'from django',
                r'urls\.py',
                r'views\.py',
            ],
        },
        
        # ============================================
        # ORM / DATABASE TOOLS
        # ============================================
        'orm': {
            'prisma': [
                r'prisma',
                r'PrismaClient',
                r'@prisma/client',
                r'schema\.prisma',
            ],
            'drizzle': [
                r'drizzle',
                r'drizzle-orm',
                r'drizzle-kit',
            ],
            'typeorm': [
                r'typeorm',
                r'@typeorm',
                r'Entity\(',
                r'Column\(',
            ],
            'sequelize': [
                r'sequelize',
                r'Sequelize\(',
            ],
            'mongoose': [
                r'mongoose',
                r'Schema\(',
                r'model\(',
            ],
            'sqlalchemy': [
                r'sqlalchemy',
                r'Session',
                r'declarative_base',
                r'Column\(',
            ],
            'sqlmodel': [
                r'sqlmodel',
                r'SQLModel',
            ],
            'alembic': [
                r'alembic',
                r'migrations',
            ],
        },
        
        # ============================================
        # VALIDATION
        # ============================================
        'validation': {
            'zod': [
                r'zod',
                r'z\.',
                r'z\.string\(',
                r'z\.object\(',
            ],
            'yup': [
                r'yup',
                r'yup\.',
                r'yup\.string\(',
                r'yup\.object\(',
            ],
            'joi': [
                r'joi',
                r'Joi\.',
                r'Joi\.string\(',
            ],
            'pydantic': [
                r'pydantic',
                r'BaseModel',
                r'Field\(',
                r'validator',
            ],
            'class-validator': [
                r'class-validator',
                r'@IsString',
                r'@IsNumber',
                r'@IsEmail',
            ],
        },
        
        # ============================================
        # BUILD TOOLS
        # ============================================
        'build': {
            'vite': [
                r'vite',
                r'vite\.config',
                r'vitest\.config',
            ],
            'webpack': [
                r'webpack',
                r'webpack\.config',
            ],
            'esbuild': [
                r'esbuild',
                r'esbuild\.config',
            ],
            'rollup': [
                r'rollup',
                r'rollup\.config',
            ],
            'turbo': [
                r'turbo',
                r'turbo\.json',
            ],
            'nx': [
                r'nx',
                r'nx\.json',
                r'project\.json',
            ],
        },
        
        # ============================================
        # MONOREPO
        # ============================================
        'monorepo': {
            'pnpm-workspace': [
                r'pnpm-workspace',
                r'workspace:',
            ],
            'lerna': [
                r'lerna',
                r'lerna\.json',
            ],
            'turborepo': [
                r'turbo',
                r'turbo\.json',
            ],
            'nx': [
                r'nx',
                r'nx\.json',
            ],
        },
        
        # ============================================
        # CLOUD / INFRASTRUCTURE
        # ============================================
        'cloud': {
            'vercel': [
                r'vercel',
                r'vercel\.json',
                r'@vercel',
            ],
            'netlify': [
                r'netlify',
                r'netlify\.toml',
            ],
            'aws': [
                r'aws',
                r'@aws-sdk',
                r'aws-sdk',
                r'amazonaws',
            ],
            'gcp': [
                r'google-cloud',
                r'@google-cloud',
                r'firebase',
            ],
            'azure': [
                r'azure',
                r'@azure',
            ],
            'cloudflare': [
                r'cloudflare',
                r'wrangler',
                r'@cloudflare',
            ],
            'supabase': [
                r'supabase',
                r'@supabase',
            ],
            'planetscale': [
                r'planetscale',
                r'@planetscale',
            ],
            'railway': [
                r'railway',
                r'railway\.toml',
            ],
            'render': [
                r'render',
                r'render\.yaml',
            ],
        },
        
        # ============================================
        # AI / ML
        # ============================================
        'ai': {
            'openai': [
                r'openai',
                r'@openai',
                r'gpt-',
                r'davinci',
            ],
            'anthropic': [
                r'anthropic',
                r'@anthropic',
                r'claude',
            ],
            'langchain': [
                r'langchain',
                r'@langchain',
            ],
            'llamaindex': [
                r'llamaindex',
                r'llama_index',
            ],
            'huggingface': [
                r'huggingface',
                r'@huggingface',
                r'transformers',
            ],
            'replicate': [
                r'replicate',
                r'@replicate',
            ],
        },
        
        # ============================================
        # ARCHITECTURE PATTERNS
        # ============================================
        'architecture': {
            'microservices': [
                r'microservice',
                r'docker-compose',
                r'kubernetes',
                r'k8s',
            ],
            'serverless': [
                r'serverless',
                r'lambda',
                r'@serverless',
                r'vercel/functions',
            ],
            'turborepo': [
                r'turbo',
                r'turborepo',
            ],
            'monorepo': [
                r'monorepo',
                r'pnpm-workspace',
                r'lerna',
            ],
        },
        
        # ============================================
        # MONITORING / LOGGING
        # ============================================
        'monitoring': {
            'sentry': [
                r'sentry',
                r'@sentry',
            ],
            'datadog': [
                r'datadog',
                r'dd-trace',
            ],
            'logrocket': [
                r'logrocket',
                r'LogRocket',
            ],
            'prometheus': [
                r'prometheus',
                r'prom-client',
            ],
            'grafana': [
                r'grafana',
            ],
        },
    }
    
    # Category mapping (user-facing category -> internal check category)
    CATEGORY_MAP = {
        'database': 'database',
        'db': 'database',
        'auth': 'auth',
        'authentication': 'auth',
        'frontend': 'frontend',
        'ui': 'frontend',
        'framework': 'frontend',
        'testing': 'testing',
        'test': 'testing',
        'styling': 'styling',
        'css': 'styling',
        'state': 'state',
        'api': 'api',
        'backend': 'api',
        'orm': 'orm',
        'validation': 'validation',
        'build': 'build',
        'monorepo': 'monorepo',
        'cloud': 'cloud',
        'infrastructure': 'cloud',
        'ai': 'ai',
        'ml': 'ai',
        'architecture': 'architecture',
        'monitoring': 'monitoring',
        'logging': 'monitoring',
    }
    
    def __init__(self, root_path: Optional[str] = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.vibe_dir = self.root_path / '.vibe-integrity'
        self.results: List[CheckResult] = []
        self._content_cache: Dict[str, str] = {}
    
    def load_tech_records(self) -> List[Dict]:
        """Load tech records from vibe integrity"""
        filepath = self.vibe_dir / 'tech-records.yaml'
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            return data.get('records', [])
        except Exception as e:
            print(f"Warning: Could not load tech records: {e}")
            return []
    
    def find_config_files(self) -> List[Path]:
        """Find relevant configuration files"""
        config_patterns = [
            'package.json',
            'package-lock.json',
            'yarn.lock',
            'pnpm-lock.yaml',
            'requirements.txt',
            'pyproject.toml',
            'poetry.lock',
            'Gemfile',
            'Gemfile.lock',
            'go.mod',
            'go.sum',
            'Cargo.toml',
            'Cargo.lock',
            'pom.xml',
            'build.gradle',
            'build.gradle.kts',
            '**/schema.prisma',
            '**/*.config.js',
            '**/*.config.ts',
            '**/*.config.mjs',
            '**/settings.py',
            '**/config.py',
            '.env.example',
            'docker-compose.yml',
            'Dockerfile',
            'vercel.json',
            'netlify.toml',
        ]
        
        files = []
        for pattern in config_patterns:
            files.extend(self.root_path.glob(pattern))
        
        return files[:100]  # Limit to avoid performance issues
    
    def find_source_files(self, extensions: Optional[List[str]] = None) -> List[Path]:
        """Find source code files"""
        if extensions is None:
            extensions = ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.py', '.go', '.java', '.rb', '.rs', '.vue', '.svelte']
        
        exclude_dirs = {'node_modules', 'dist', 'build', '.git', '__pycache__', 'venv', '.venv', 'target', 'vendor', '.next', 'out'}
        files = []
        
        for ext in extensions:
            for f in self.root_path.rglob(f'*{ext}'):
                if any(part in exclude_dirs for part in f.parts):
                    continue
                files.append(f)
        
        return files[:200]  # Limit for performance
    
    def get_cached_content(self, key: str, loader_func) -> str:
        """Get cached content or load it"""
        if key not in self._content_cache:
            self._content_cache[key] = loader_func()
        return self._content_cache[key]
    
    def read_files_content(self, files: List[Path]) -> str:
        """Read content from multiple files"""
        content_parts = []
        for f in files:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                content_parts.append(f"--- {f.name} ---\n{content}")
            except:
                pass
        return '\n'.join(content_parts)
    
    def check_tech_usage(self, category: str, tech_name: str) -> Tuple[bool, str]:
        """Check if a technology is actually used in code"""
        if category not in self.TECH_PATTERNS:
            return True, "No patterns defined for this category"
        
        patterns = self.TECH_PATTERNS[category].get(tech_name.lower(), [])
        if not patterns:
            return True, "No patterns defined for this technology"
        
        # Check config files first (faster)
        config_content = self.get_cached_content('config', lambda: self.read_files_content(self.find_config_files()))
        
        for pattern in patterns:
            if re.search(pattern, config_content, re.IGNORECASE):
                return True, f"Found in config files: {pattern}"
        
        # Check source files
        source_content = self.get_cached_content('source', lambda: self.read_files_content(self.find_source_files()))
        
        for pattern in patterns:
            if re.search(pattern, source_content, re.IGNORECASE):
                return True, f"Found in source: {pattern}"
        
        return False, f"Technology '{tech_name}' not detected in codebase"
    
    def extract_tech_from_text(self, text: str, category: str) -> Optional[str]:
        """Extract technology name from decision text"""
        text_lower = text.lower()
        
        if category not in self.TECH_PATTERNS:
            return None
        
        # Try to find matching technology
        for tech_name in self.TECH_PATTERNS[category].keys():
            if tech_name in text_lower:
                return tech_name
        
        # Try common aliases
        aliases = {
            'postgres': 'postgresql',
            'mysql': 'mysql',
            'mongo': 'mongodb',
            'react.js': 'react',
            'vue.js': 'vue',
            'tailwindcss': 'tailwind',
            'scss': 'sass',
            'nextjs': 'next.js',
        }
        
        for alias, tech in aliases.items():
            if alias in text_lower and tech in self.TECH_PATTERNS.get(category, {}):
                return tech
        
        return None
    
    def check_record(self, record: Dict) -> CheckResult:
        """Check a single tech record against actual code"""
        record_id = record.get('id', 'unknown')
        category = record.get('category', '')
        decision = record.get('decision', '')
        title = record.get('title', '')
        
        # Extract technology name from decision/title
        text_to_check = f"{decision} {title}"
        
        # Map category to check type
        check_category = self.CATEGORY_MAP.get(category.lower())
        if not check_category:
            return CheckResult(
                record_id=record_id,
                category=category,
                decision=decision[:100],
                status=CheckStatus.SKIP,
                message=f"Category '{category}' not supported for automatic verification"
            )
        
        # Try to find matching technology
        found_tech = self.extract_tech_from_text(text_to_check, check_category)
        
        if not found_tech:
            return CheckResult(
                record_id=record_id,
                category=category,
                decision=decision[:100],
                status=CheckStatus.UNKNOWN,
                message="Could not determine specific technology from decision text"
            )
        
        # Check if technology is used
        is_used, message = self.check_tech_usage(check_category, found_tech)
        
        return CheckResult(
            record_id=record_id,
            category=category,
            decision=decision[:100],
            status=CheckStatus.PASS if is_used else CheckStatus.FAIL,
            message=message,
            details={'technology': found_tech, 'check_category': check_category}
        )
    
    def run_checks(self, category_filter: Optional[str] = None) -> List[CheckResult]:
        """Run all alignment checks"""
        records = self.load_tech_records()
        
        if not records:
            print("No tech records found")
            return []
        
        self.results = []
        self._content_cache = {}  # Clear cache
        
        for record in records:
            if category_filter:
                if record.get('category', '').lower() != category_filter.lower():
                    continue
            
            result = self.check_record(record)
            self.results.append(result)
        
        return self.results
    
    def print_report(self) -> bool:
        """Print alignment check report"""
        if not self.results:
            print("No results to report")
            return True
        
        print("\n" + "=" * 60)
        print("Code Alignment Verification Report")
        print("=" * 60 + "\n")
        
        status_counts = {s: 0 for s in CheckStatus}
        
        for result in self.results:
            status_counts[result.status] += 1
            
            status_icon = {
                CheckStatus.PASS: "✅",
                CheckStatus.FAIL: "❌",
                CheckStatus.SKIP: "⏭️",
                CheckStatus.UNKNOWN: "❓",
            }.get(result.status, "❓")
            
            print(f"{status_icon} [{result.record_id}] {result.category}")
            print(f"   Decision: {result.decision[:60]}{'...' if len(result.decision) > 60 else ''}")
            print(f"   Status: {result.status.value.upper()}")
            print(f"   Message: {result.message}")
            if result.details:
                print(f"   Details: {result.details}")
            print()
        
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"✅ Pass: {status_counts[CheckStatus.PASS]}")
        print(f"❌ Fail: {status_counts[CheckStatus.FAIL]}")
        print(f"⏭️ Skip: {status_counts[CheckStatus.SKIP]}")
        print(f"❓ Unknown: {status_counts[CheckStatus.UNKNOWN]}")
        print()
        
        if status_counts[CheckStatus.FAIL] > 0:
            print("⚠️  Some decisions are not reflected in code!")
            print("   Review failed checks and either update code or records.")
            return False
        else:
            print("✅ All checked decisions align with code!")
            return True
    
    def get_failed_checks(self) -> List[CheckResult]:
        """Get list of failed checks"""
        return [r for r in self.results if r.status == CheckStatus.FAIL]
    
    def get_results_dict(self) -> Dict[str, Any]:
        """Get results as dictionary for JSON output"""
        return {
            'results': [
                {
                    'record_id': r.record_id,
                    'category': r.category,
                    'decision': r.decision,
                    'status': r.status.value,
                    'message': r.message,
                    'details': r.details
                }
                for r in self.results
            ],
            'summary': {
                'total': len(self.results),
                'pass': sum(1 for r in self.results if r.status == CheckStatus.PASS),
                'fail': sum(1 for r in self.results if r.status == CheckStatus.FAIL),
                'skip': sum(1 for r in self.results if r.status == CheckStatus.SKIP),
                'unknown': sum(1 for r in self.results if r.status == CheckStatus.UNKNOWN),
            },
            'failed_count': len(self.get_failed_checks())
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify code alignment with tech decisions')
    parser.add_argument('--root', help='Root path of project')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--quiet', action='store_true', help='Only show failures')
    parser.add_argument('--list-categories', action='store_true', help='List all supported categories')
    
    args = parser.parse_args()
    
    if args.list_categories:
        print("Supported categories:")
        for cat in sorted(CodeAlignmentChecker.CATEGORY_MAP.keys()):
            print(f"  - {cat}")
        return
    
    checker = CodeAlignmentChecker(args.root)
    results = checker.run_checks(args.category)
    
    if args.json:
        print(json.dumps(checker.get_results_dict(), indent=2, ensure_ascii=False))
    else:
        success = checker.print_report()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

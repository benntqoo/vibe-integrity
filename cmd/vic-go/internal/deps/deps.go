package deps

import (
	"fmt"
	"go/parser"
	"go/token"
	"gopkg.in/yaml.v3"
	"os"
	"path/filepath"
	"regexp"
	"slices"
	"strings"
	"time"
)

// Language represents a programming language with its import parsing
type Language interface {
	Name() string
	Extensions() []string
	ParseImports(content string) []string
	IsExternal(path string) bool
}

// GoLanguage parses Go imports using AST
type GoLanguage struct{}

func (GoLanguage) Name() string         { return "Go" }
func (GoLanguage) Extensions() []string { return []string{".go"} }
func (GoLanguage) IsExternal(path string) bool {
	return !strings.Contains(path, ".") || strings.HasPrefix(path, ".")
}

func (GoLanguage) ParseImports(content string) []string {
	// Use go/parser for accurate parsing
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, "", content, parser.ImportsOnly)
	if err != nil {
		return nil
	}

	var imports []string
	for _, imp := range f.Imports {
		if imp.Path != nil {
			imports = append(imports, strings.Trim(imp.Path.Value, "\""))
		}
	}
	return imports
}

// PythonLanguage parses Python imports using regex
type PythonLanguage struct{}

func (PythonLanguage) Name() string         { return "Python" }
func (PythonLanguage) Extensions() []string { return []string{".py", ".pyi"} }

func (PythonLanguage) IsExternal(path string) bool {
	// External: doesn't start with . and has dots (package imports)
	return !strings.HasPrefix(path, ".") && strings.Contains(path, ".")
}

func (PythonLanguage) ParseImports(content string) []string {
	var imports []string

	// Match: import x, import x as y, import x.y.z
	importRE := regexp.MustCompile(`(?m)^\s*import\s+([^\s;#]+)`)
	// Match: from x import y, from x.y import z
	fromImportRE := regexp.MustCompile(`(?m)^\s*from\s+([^\s;#]+)\s+import`)

	for _, match := range importRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, cleanPythonImport(match[1]))
		}
	}

	for _, match := range fromImportRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, cleanPythonImport(match[1]))
		}
	}

	return imports
}

func cleanPythonImport(path string) string {
	// Remove 'as' alias part if present
	if idx := strings.Index(path, " as "); idx != -1 {
		path = path[:idx]
	}
	// Remove everything after first dot that might be function/variable
	parts := strings.Split(path, ".")
	if len(parts) > 2 && !strings.HasPrefix(parts[0], ".") {
		// Keep top-level package
		return strings.Join(parts[:2], ".")
	}
	return parts[0]
}

// JavaScriptLanguage parses JS imports using regex
type JavaScriptLanguage struct{}

func (JavaScriptLanguage) Name() string         { return "JavaScript" }
func (JavaScriptLanguage) Extensions() []string { return []string{".js", ".mjs", ".cjs"} }

func (JavaScriptLanguage) IsExternal(path string) bool {
	// External: doesn't start with . or ..
	return !strings.HasPrefix(path, ".")
}

func (JavaScriptLanguage) ParseImports(content string) []string {
	var imports []string

	// Match: import x from 'path', import * as x from 'path', import { x } from 'path'
	importRE := regexp.MustCompile(`(?m)^\s*import\s+(?:[^'"]*from\s+)?['"]([^'"]+)['"]`)
	// Match: require('path') or require("path")
	requireRE := regexp.MustCompile(`(?m)^\s*(?:const|let|var)?\s*\w*\s*=\s*require\s*\(\s*['"]([^'"]+)['"]\s*\)`)

	for _, match := range importRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, match[1])
		}
	}

	for _, match := range requireRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, match[1])
		}
	}

	return imports
}

// TypeScriptLanguage parses TS imports using regex
type TypeScriptLanguage struct{}

func (TypeScriptLanguage) Name() string         { return "TypeScript" }
func (TypeScriptLanguage) Extensions() []string { return []string{".ts", ".tsx", ".mts", ".cts"} }

func (TypeScriptLanguage) IsExternal(path string) bool {
	return !strings.HasPrefix(path, ".") && !strings.HasPrefix(path, "/")
}

func (TypeScriptLanguage) ParseImports(content string) []string {
	var imports []string

	// Match ES6 imports
	importRE := regexp.MustCompile(`(?m)^\s*import\s+(?:[^'"]*from\s+)?['"]([^'"]+)['"]`)
	// Match require()
	requireRE := regexp.MustCompile(`(?m)^\s*(?:const|let|var)?\s*\w*\s*=\s*require\s*\(\s*['"]([^'"]+)['"]\s*\)`)
	// Match type imports
	typeImportRE := regexp.MustCompile(`(?m)^\s*import\s+type\s+(?:[^'"]*from\s+)?['"]([^'"]+)['"]`)

	for _, match := range importRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, match[1])
		}
	}
	for _, match := range requireRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, match[1])
		}
	}
	for _, match := range typeImportRE.FindAllStringSubmatch(content, -1) {
		if len(match) > 1 {
			imports = append(imports, match[1])
		}
	}

	return imports
}

// Analyzer scans code and builds dependency graph
type Analyzer struct {
	projectDir   string
	modulePrefix string // e.g., "github.com/user/project"
	languages    []Language
	modules      map[string]*Module
}

// Module represents a code module (directory with source files)
type Module struct {
	Name      string   `yaml:"name"`
	Type      string   `yaml:"type"`
	Language  string   `yaml:"language,omitempty"`
	Files     []string `yaml:"files,omitempty"`
	DependsOn []string `yaml:"depends_on,omitempty"`
	CalledBy  []string `yaml:"called_by,omitempty"`
	Exports   []string `yaml:"exports,omitempty"`
}

// AnalyzeResult contains the complete analysis result
type AnalyzeResult struct {
	Version           string    `yaml:"version"`
	GeneratedAt       string    `yaml:"generated_at"`
	AnalysisMode      string    `yaml:"analysis_mode"`
	ProjectDir        string    `yaml:"project_dir"`
	LanguagesDetected []string  `yaml:"languages_detected"`
	Modules           []*Module `yaml:"modules"`
	InternalDepsCount int       `yaml:"internal_deps_count"`
	Confidence        int       `yaml:"confidence"`
	ConfidenceFactors []string  `yaml:"confidence_factors,omitempty"`
	Warnings          []string  `yaml:"warnings,omitempty"`
}

// NewAnalyzer creates a new dependency analyzer
func NewAnalyzer(projectDir string) *Analyzer {
	analyzer := &Analyzer{
		projectDir: projectDir,
		languages: []Language{
			GoLanguage{},
			PythonLanguage{},
			JavaScriptLanguage{},
			TypeScriptLanguage{},
		},
		modules: make(map[string]*Module),
	}

	// Try to read module name from go.mod
	goModPath := filepath.Join(projectDir, "go.mod")
	if data, err := os.ReadFile(goModPath); err == nil {
		lines := strings.Split(string(data), "\n")
		for _, line := range lines {
			if strings.HasPrefix(strings.TrimSpace(line), "module ") {
				analyzer.modulePrefix = strings.TrimSpace(strings.TrimPrefix(line, "module "))
				break
			}
		}
	}

	return analyzer
}

// Analyze performs the dependency analysis
func (a *Analyzer) Analyze() (*AnalyzeResult, error) {
	// Step 1: Find all source files grouped by module
	modules, err := a.findModules()
	if err != nil {
		return nil, err
	}

	// Store modules in analyzer for use by isInternal/resolveInternal
	a.modules = modules

	// Step 2: Parse imports for each module
	for _, module := range modules {
		imports := a.parseModuleImports(module)
		for _, imp := range imports {
			if a.isInternal(module.Name, imp) {
				dep := a.resolveInternal(module.Name, imp)
				if dep != "" && dep != module.Name {
					if !contains(module.DependsOn, dep) {
						module.DependsOn = append(module.DependsOn, dep)
					}
				}
			}
		}
	}

	// Step 3: Calculate called_by (reverse dependencies)
	for _, module := range modules {
		for _, dep := range module.DependsOn {
			if depModule, ok := modules[dep]; ok {
				if !contains(depModule.CalledBy, module.Name) {
					depModule.CalledBy = append(depModule.CalledBy, module.Name)
				}
			}
		}
	}

	// Step 4: Collect detected languages
	langSet := make(map[string]bool)
	for _, m := range modules {
		langSet[m.Language] = true
	}
	var languages []string
	for l := range langSet {
		languages = append(languages, l)
	}

	// Step 5: Calculate statistics
	depsCount := 0
	for _, m := range modules {
		depsCount += len(m.DependsOn)
	}

	// Step 6: Calculate confidence
	confidence := 70
	if len(modules) > 5 {
		confidence += 10
	}
	if len(modules) > 10 {
		confidence += 10
	}
	if depsCount > 5 {
		confidence += 10
	}
	if confidence > 95 {
		confidence = 95
	}

	// Build result
	moduleList := make([]*Module, 0, len(modules))
	for _, m := range modules {
		moduleList = append(moduleList, m)
	}

	return &AnalyzeResult{
		Version:           "2.0",
		GeneratedAt:       time.Now().Format(time.RFC3339),
		AnalysisMode:      "multi_language_import_analysis",
		ProjectDir:        a.projectDir,
		LanguagesDetected: languages,
		Modules:           moduleList,
		InternalDepsCount: depsCount,
		Confidence:        confidence,
		ConfidenceFactors: []string{fmt.Sprintf("analyzed_%d_modules", len(modules))},
	}, nil
}

// findModules finds all modules (directories with source files)
func (a *Analyzer) findModules() (map[string]*Module, error) {
	modules := make(map[string]*Module)

	// Build extension to language map
	extToLang := make(map[string]Language)
	for _, lang := range a.languages {
		for _, ext := range lang.Extensions() {
			extToLang[ext] = lang
		}
	}

	err := filepath.Walk(a.projectDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}

		// Skip certain directories
		skipDirs := []string{
			".git", "vendor", "node_modules", ".venv", "venv",
			"testdata", "_test", ".idea", ".vscode", "dist", "build",
			"target", "__pycache__", ".next", ".nuxt",
		}
		rel, _ := filepath.Rel(a.projectDir, path)
		rel = filepath.ToSlash(rel)
		for _, skip := range skipDirs {
			if strings.Contains(rel, skip+"/") || rel == skip {
				if info.IsDir() {
					return filepath.SkipDir
				}
				return nil
			}
		}

		if info.IsDir() {
			// Check if directory has source files
			var sourceFiles []string
			var mainLang Language

			entries, err := os.ReadDir(path)
			if err != nil {
				return nil
			}

			for _, entry := range entries {
				if entry.IsDir() {
					continue
				}
				ext := filepath.Ext(entry.Name())
				if lang, ok := extToLang[ext]; ok {
					if !strings.HasSuffix(entry.Name(), "_test") && !strings.HasSuffix(entry.Name(), ".test."+ext) {
						sourceFiles = append(sourceFiles, filepath.Join(path, entry.Name()))
						if mainLang == nil {
							mainLang = lang
						}
					}
				}
			}

			if len(sourceFiles) > 0 {
				modulePath, _ := filepath.Rel(a.projectDir, path)
				modulePath = filepath.ToSlash(modulePath)

				if modulePath != "." {
					modules[modulePath] = &Module{
						Name:     modulePath,
						Type:     guessModuleType(modulePath),
						Language: mainLang.Name(),
						Files:    sourceFiles,
					}
				}
			}
		}

		return nil
	})

	return modules, err
}

// parseModuleImports parses all imports in a module
func (a *Analyzer) parseModuleImports(module *Module) []string {
	var allImports []string

	for _, file := range module.Files {
		content, err := os.ReadFile(file)
		if err != nil {
			continue
		}

		ext := filepath.Ext(file)
		var lang Language
		for _, l := range a.languages {
			for _, e := range l.Extensions() {
				if e == ext {
					lang = l
					break
				}
			}
			if lang != nil {
				break
			}
		}

		if lang != nil {
			imports := lang.ParseImports(string(content))

			// For Go, convert full import paths to relative paths
			if a.modulePrefix != "" && lang.Name() == "Go" {
				for i, imp := range imports {
					if strings.HasPrefix(imp, a.modulePrefix+"/") {
						imports[i] = strings.TrimPrefix(imp, a.modulePrefix+"/")
					}
				}
			}

			allImports = append(allImports, imports...)
		}
	}

	return allImports
}

// isInternal checks if an import path is internal to the project
func (a *Analyzer) isInternal(moduleName, importPath string) bool {
	// Normalize import path
	importPath = a.normalizeImportPath(importPath)

	// Check if it's a known module
	for name := range a.modules {
		if importPath == name || importPath == "./"+name || importPath == "../"+name {
			return true
		}
		// Check if import path starts with module name (for Go-style)
		if strings.HasPrefix(importPath, moduleName+"/") {
			return true
		}
	}

	return false
}

// normalizeImportPath normalizes import path format
func (a *Analyzer) normalizeImportPath(path string) string {
	// Remove leading ./ or ./
	path = strings.TrimPrefix(path, "./")
	path = strings.TrimPrefix(path, "../")

	// Remove file extensions
	path = strings.TrimSuffix(path, ".go")
	path = strings.TrimSuffix(path, ".py")
	path = strings.TrimSuffix(path, ".js")
	path = strings.TrimSuffix(path, ".ts")

	// Remove trailing slashes
	path = strings.TrimSuffix(path, "/")

	return path
}

// resolveInternal resolves an import to a module name
func (a *Analyzer) resolveInternal(moduleName, importPath string) string {
	importPath = a.normalizeImportPath(importPath)

	// Direct match
	if _, ok := a.modules[importPath]; ok {
		return importPath
	}

	// Relative path match
	if strings.HasPrefix(importPath, "./") || strings.HasPrefix(importPath, "../") {
		// Try to resolve relative to module
		resolved := filepath.Join(moduleName, importPath)
		resolved = filepath.ToSlash(resolved)

		// Try exact match
		if _, ok := a.modules[resolved]; ok {
			return resolved
		}

		// Try parent directories
		for {
			resolved = filepath.Dir(resolved)
			if resolved == "." || resolved == "/" {
				break
			}
			resolved = filepath.ToSlash(resolved)
			if _, ok := a.modules[resolved]; ok {
				return resolved
			}
		}
	}

	// Check if import starts with module name
	if strings.HasPrefix(importPath, moduleName+"/") {
		internalPath := strings.TrimPrefix(importPath, moduleName+"/")
		return internalPath
	}

	return ""
}

// guessModuleType guesses the module type based on its path
func guessModuleType(path string) string {
	switch {
	case strings.HasPrefix(path, "cmd/"):
		return "binary"
	case strings.HasPrefix(path, "src/cmd/"):
		return "binary"
	case strings.HasPrefix(path, "internal/"):
		return "library"
	case strings.HasPrefix(path, "pkg/"):
		return "library"
	case strings.HasPrefix(path, "lib/"):
		return "library"
	case strings.HasPrefix(path, "src/"):
		return "library"
	case strings.HasPrefix(path, "packages/"):
		return "library"
	default:
		return "library"
	}
}

// contains checks if a slice contains a string
func contains(slice []string, s string) bool {
	for _, v := range slice {
		if v == s {
			return true
		}
	}
	return false
}

// Save saves the analysis result to a YAML file
func (r *AnalyzeResult) Save(path string) error {
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return err
	}

	data, err := r.MarshalYAML()
	if err != nil {
		return err
	}

	return os.WriteFile(path, data, 0644)
}

// MarshalYAML converts result to YAML bytes
func (r *AnalyzeResult) MarshalYAML() ([]byte, error) {
	var sb strings.Builder

	sb.WriteString("# Dependency Graph - VIBE-SDD\n")
	sb.WriteString("# =================================\n")
	sb.WriteString("# Auto-generated by vic-go deps scan\n")
	sb.WriteString("# DO NOT EDIT MANUALLY - re-run vic deps scan to regenerate\n\n")

	fmt.Fprintf(&sb, "version: %q\n", r.Version)
	fmt.Fprintf(&sb, "generated_at: %q\n", r.GeneratedAt)
	fmt.Fprintf(&sb, "analysis_mode: %q\n", r.AnalysisMode)
	fmt.Fprintf(&sb, "project_dir: %q\n", r.ProjectDir)

	if len(r.LanguagesDetected) > 0 {
		sb.WriteString("languages_detected:\n")
		for _, l := range r.LanguagesDetected {
			fmt.Fprintf(&sb, "  - %s\n", l)
		}
	}

	sb.WriteString("\nmodules:\n")
	for _, m := range r.Modules {
		fmt.Fprintf(&sb, "  %s:\n", m.Name)
		fmt.Fprintf(&sb, "    type: %s\n", m.Type)
		if m.Language != "" {
			fmt.Fprintf(&sb, "    language: %s\n", m.Language)
		}
		if len(m.DependsOn) > 0 {
			sb.WriteString("    depends_on:\n")
			for _, dep := range m.DependsOn {
				fmt.Fprintf(&sb, "      - %s\n", dep)
			}
		}
		if len(m.CalledBy) > 0 {
			sb.WriteString("    called_by:\n")
			for _, caller := range m.CalledBy {
				fmt.Fprintf(&sb, "      - %s\n", caller)
			}
		}
	}

	sb.WriteString("\nstatistics:\n")
	fmt.Fprintf(&sb, "  module_count: %d\n", len(r.Modules))
	fmt.Fprintf(&sb, "  internal_deps_count: %d\n", r.InternalDepsCount)
	fmt.Fprintf(&sb, "  confidence: %d\n", r.Confidence)
	if len(r.ConfidenceFactors) > 0 {
		sb.WriteString("  confidence_factors:\n")
		for _, f := range r.ConfidenceFactors {
			fmt.Fprintf(&sb, "    - %s\n", f)
		}
	}

	return []byte(sb.String()), nil
}

// ============================================================================
// Query Methods (for on-demand context)
// ============================================================================

// LoadGraph loads a dependency graph from a YAML file
func LoadGraph(path string) (*AnalyzeResult, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	// Parse YAML format
	var parsed struct {
		Version           string   `yaml:"version"`
		GeneratedAt       string   `yaml:"generated_at"`
		AnalysisMode      string   `yaml:"analysis_mode"`
		ProjectDir        string   `yaml:"project_dir"`
		LanguagesDetected []string `yaml:"languages_detected"`
		Modules           map[string]struct {
			Type      string   `yaml:"type"`
			Language  string   `yaml:"language"`
			DependsOn []string `yaml:"depends_on"`
			CalledBy  []string `yaml:"called_by"`
		} `yaml:"modules"`
		Statistics struct {
			ModuleCount       int      `yaml:"module_count"`
			InternalDepsCount int      `yaml:"internal_deps_count"`
			Confidence        int      `yaml:"confidence"`
			ConfidenceFactors []string `yaml:"confidence_factors"`
		} `yaml:"statistics"`
	}

	if err := yaml.Unmarshal(data, &parsed); err != nil {
		return nil, fmt.Errorf("failed to parse YAML: %w", err)
	}

	// Convert to AnalyzeResult
	modules := make([]*Module, 0, len(parsed.Modules))
	for name, m := range parsed.Modules {
		modules = append(modules, &Module{
			Name:      name,
			Type:      m.Type,
			Language:  m.Language,
			DependsOn: m.DependsOn,
			CalledBy:  m.CalledBy,
		})
	}

	return &AnalyzeResult{
		Version:           parsed.Version,
		GeneratedAt:       parsed.GeneratedAt,
		AnalysisMode:      parsed.AnalysisMode,
		ProjectDir:        parsed.ProjectDir,
		LanguagesDetected: parsed.LanguagesDetected,
		Modules:           modules,
		InternalDepsCount: parsed.Statistics.InternalDepsCount,
		Confidence:        parsed.Statistics.Confidence,
		ConfidenceFactors: parsed.Statistics.ConfidenceFactors,
	}, nil
}

// Impact represents the impact analysis result
type Impact struct {
	Type            string
	DirectCallers   []string
	IndirectCallers []string
	APIsUsed        []string
}

// Search finds modules matching a pattern
func (r *AnalyzeResult) Search(pattern string) []*Module {
	var matches []*Module
	pattern = strings.ToLower(pattern)

	for _, m := range r.Modules {
		if strings.Contains(strings.ToLower(m.Name), pattern) {
			matches = append(matches, m)
		}
	}

	return matches
}

// GetModule returns a module by name
func (r *AnalyzeResult) GetModule(name string) *Module {
	for _, m := range r.Modules {
		if m.Name == name {
			return m
		}
	}
	return nil
}

// GetImpact calculates the impact of changing a module
func (r *AnalyzeResult) GetImpact(moduleName string) *Impact {
	module := r.GetModule(moduleName)
	if module == nil {
		return nil
	}

	// Build module map for quick lookup
	moduleMap := make(map[string]*Module)
	for _, m := range r.Modules {
		moduleMap[m.Name] = m
	}

	// Direct callers
	directCallers := make([]string, 0)
	for _, c := range module.CalledBy {
		if !slices.Contains(directCallers, c) {
			directCallers = append(directCallers, c)
		}
	}

	// Indirect callers (callers of callers)
	indirectCallers := make([]string, 0)
	visited := make(map[string]bool)
	queue := make([]string, len(directCallers))
	copy(queue, directCallers)

	for len(queue) > 0 {
		caller := queue[0]
		queue = queue[1:]

		if visited[caller] {
			continue
		}
		visited[caller] = true

		if m, ok := moduleMap[caller]; ok {
			for _, c := range m.CalledBy {
				if c != moduleName && !slices.Contains(directCallers, c) && !slices.Contains(indirectCallers, c) {
					indirectCallers = append(indirectCallers, c)
					queue = append(queue, c)
				}
			}
		}
	}

	// APIs used (dependencies)
	apisUsed := make([]string, 0)
	for _, dep := range module.DependsOn {
		if !slices.Contains(apisUsed, dep) {
			apisUsed = append(apisUsed, dep)
		}
	}

	return &Impact{
		Type:            module.Type,
		DirectCallers:   directCallers,
		IndirectCallers: indirectCallers,
		APIsUsed:        apisUsed,
	}
}

package commands

import (
	"fmt"

	"github.com/spf13/cobra"
	"github.com/vic-sdd/vic/internal/config"
	"github.com/vic-sdd/vic/internal/deps"
)

// NewDepsCmd creates the deps command
func NewDepsCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "deps",
		Short: "Analyze code dependencies and module relationships",
		Long: `Analyze internal module dependencies and generate dependency graph.

This helps understand:
- What modules exist and their structure
- Which modules depend on which
- Impact analysis: what changes affect what

Examples:
  vic deps scan          # Scan and generate dependency graph
  vic deps search auth   # Search for modules matching "auth"
  vic deps impact auth   # Show impact of changing auth module
  vic deps callers auth   # Show who calls auth module`,
	}

	cmd.AddCommand(NewDepsScanCmd(cfg))
	cmd.AddCommand(NewDepsSearchCmd(cfg))
	cmd.AddCommand(NewDepsImpactCmd(cfg))
	cmd.AddCommand(NewDepsCallersCmd(cfg))
	cmd.AddCommand(NewDepsListCmd(cfg))

	return cmd
}

// ============================================================================
// SCAN Command
// ============================================================================

// NewDepsScanCmd creates the deps scan subcommand
func NewDepsScanCmd(cfg *config.Config) *cobra.Command {
	var outputFile string

	cmd := &cobra.Command{
		Use:     "scan",
		Short:   "Scan project and generate dependency graph",
		Long:    `Scan the project using static analysis to build a dependency graph.`,
		Example: `  vic deps scan`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDepsScan(cfg, outputFile)
		},
	}

	cmd.Flags().StringVarP(&outputFile, "output", "o", "", "Output file (default: .vic-sdd/dependency-graph.yaml)")

	return cmd
}

func runDepsScan(cfg *config.Config, outputFile string) error {
	fmt.Println("🔍 Scanning project for dependencies...")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	// Determine output file
	if outputFile == "" {
		outputFile = cfg.DependencyGraphFile
	}

	// Create analyzer
	analyzer := deps.NewAnalyzer(cfg.ProjectDir)

	// Run analysis
	result, err := analyzer.Analyze()
	if err != nil {
		return fmt.Errorf("analysis failed: %w", err)
	}

	// Print summary
	printSummary(result)

	// Write output
	if err := result.Save(outputFile); err != nil {
		return fmt.Errorf("failed to save: %w", err)
	}

	fmt.Printf("\n✅ Output: %s\n", outputFile)

	return nil
}

// ============================================================================
// SEARCH Command
// ============================================================================

// NewDepsSearchCmd creates the deps search subcommand
func NewDepsSearchCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "search [pattern]",
		Short: "Search for modules matching a pattern",
		Long:  `Search for modules whose name contains the pattern.`,
		Example: `  vic deps search auth    # Search for modules containing "auth"
  vic deps search handler  # Search for modules containing "handler"`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDepsSearch(cfg, args[0])
		},
	}

	return cmd
}

func runDepsSearch(cfg *config.Config, pattern string) error {
	// Load existing dependency graph
	result, err := deps.LoadGraph(cfg.DependencyGraphFile)
	if err != nil {
		// If no graph exists, run scan first
		fmt.Println("⚠️  No dependency graph found. Running scan first...")
		analyzer := deps.NewAnalyzer(cfg.ProjectDir)
		result, err = analyzer.Analyze()
		if err != nil {
			return fmt.Errorf("scan failed: %w", err)
		}
		if err := result.Save(cfg.DependencyGraphFile); err != nil {
			return fmt.Errorf("failed to save: %w", err)
		}
	}

	// Search for matching modules
	matches := result.Search(pattern)

	if len(matches) == 0 {
		fmt.Printf("❌ No modules found matching: %s\n", pattern)
		return nil
	}

	fmt.Printf("🔍 Search results for: %s\n", pattern)
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	for _, m := range matches {
		printModuleDetail(m)
	}

	fmt.Printf("\n✅ Found %d matching module(s)\n", len(matches))

	return nil
}

// ============================================================================
// IMPACT Command
// ============================================================================

// NewDepsImpactCmd creates the deps impact subcommand
func NewDepsImpactCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "impact [module]",
		Short: "Show impact of changing a module",
		Long:  `Show what modules and APIs would be affected if you change the specified module.`,
		Example: `  vic deps impact internal/auth    # Show impact of changing auth
  vic deps impact handlers/auth    # Show impact of changing auth handler`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDepsImpact(cfg, args[0])
		},
	}

	return cmd
}

func runDepsImpact(cfg *config.Config, moduleName string) error {
	// Load existing dependency graph
	result, err := deps.LoadGraph(cfg.DependencyGraphFile)
	if err != nil {
		return fmt.Errorf("no dependency graph found. Run 'vic deps scan' first")
	}

	// Get impact
	impact := result.GetImpact(moduleName)

	if impact == nil {
		fmt.Printf("❌ Module not found: %s\n", moduleName)
		fmt.Println("💡 Run 'vic deps list' to see all modules")
		return nil
	}

	fmt.Printf("🔍 Impact Analysis: %s\n", moduleName)
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("📁 Type: %s\n\n", impact.Type)

	// Direct callers (affected if you change this module)
	if len(impact.DirectCallers) > 0 {
		fmt.Println("🟢 Direct Callers (directly affected):")
		for _, caller := range impact.DirectCallers {
			fmt.Printf("   └─ %s\n", caller)
		}
		fmt.Println()
	}

	// Indirect callers (transitively affected)
	if len(impact.IndirectCallers) > 0 {
		fmt.Println("🟡 Indirect Callers (transitively affected):")
		for _, caller := range impact.IndirectCallers {
			fmt.Printf("   └─ %s\n", caller)
		}
		fmt.Println()
	}

	// APIs used by this module
	if len(impact.APIsUsed) > 0 {
		fmt.Println("📡 APIs Used by This Module:")
		for _, api := range impact.APIsUsed {
			fmt.Printf("   └─ %s\n", api)
		}
		fmt.Println()
	}

	// Risk summary
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("📊 Impact Summary:")
	fmt.Printf("   🟢 Direct impact: %d modules\n", len(impact.DirectCallers))
	fmt.Printf("   🟡 Indirect impact: %d modules\n", len(impact.IndirectCallers))
	fmt.Printf("   📡 Total affected: %d modules\n", len(impact.DirectCallers)+len(impact.IndirectCallers))

	// Risk level
	riskLevel := "Low"
	if len(impact.DirectCallers)+len(impact.IndirectCallers) > 5 {
		riskLevel = "Medium"
	}
	if len(impact.DirectCallers)+len(impact.IndirectCallers) > 10 {
		riskLevel = "High"
	}
	fmt.Printf("   ⚠️  Risk Level: %s\n", riskLevel)

	return nil
}

// ============================================================================
// CALLERS Command
// ============================================================================

// NewDepsCallersCmd creates the deps callers subcommand
func NewDepsCallersCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "callers [module]",
		Short: "Show who calls a module",
		Long:  `Show which modules call the specified module.`,
		Example: `  vic deps callers internal/auth  # Show who calls auth
  vic deps callers handlers      # Show who calls handlers`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDepsCallers(cfg, args[0])
		},
	}

	return cmd
}

func runDepsCallers(cfg *config.Config, moduleName string) error {
	// Load existing dependency graph
	result, err := deps.LoadGraph(cfg.DependencyGraphFile)
	if err != nil {
		return fmt.Errorf("no dependency graph found. Run 'vic deps scan' first")
	}

	// Get callers
	module := result.GetModule(moduleName)

	if module == nil {
		fmt.Printf("❌ Module not found: %s\n", moduleName)
		fmt.Println("💡 Run 'vic deps list' to see all modules")
		return nil
	}

	fmt.Printf("🔍 Callers of: %s\n", moduleName)
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	if len(module.CalledBy) == 0 {
		fmt.Println("📭 No modules call this module directly.")
		fmt.Println("   (This might be a top-level module or entry point)")
	} else {
		fmt.Println("📞 Direct Callers:")
		for _, caller := range module.CalledBy {
			fmt.Printf("   └─ %s\n", caller)
		}
	}

	return nil
}

// ============================================================================
// LIST Command
// ============================================================================

// NewDepsListCmd creates the deps list subcommand
func NewDepsListCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:     "list",
		Short:   "List all modules",
		Long:    `List all modules in the dependency graph.`,
		Example: `  vic deps list    # List all modules`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDepsList(cfg)
		},
	}

	return cmd
}

func runDepsList(cfg *config.Config) error {
	// Load existing dependency graph
	result, err := deps.LoadGraph(cfg.DependencyGraphFile)
	if err != nil {
		// If no graph exists, run scan first
		fmt.Println("⚠️  No dependency graph found. Running scan first...")
		analyzer := deps.NewAnalyzer(cfg.ProjectDir)
		result, err = analyzer.Analyze()
		if err != nil {
			return fmt.Errorf("scan failed: %w", err)
		}
		if err := result.Save(cfg.DependencyGraphFile); err != nil {
			return fmt.Errorf("failed to save: %w", err)
		}
	}

	fmt.Println("📦 All Modules")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	for _, m := range result.Modules {
		stats := ""
		if len(m.DependsOn) > 0 {
			stats += fmt.Sprintf(" →%d", len(m.DependsOn))
		}
		if len(m.CalledBy) > 0 {
			stats += fmt.Sprintf(" ←%d", len(m.CalledBy))
		}
		if stats == "" {
			stats = " (no dependencies)"
		}
		fmt.Printf("  📁 %s%s\n", m.Name, stats)
	}

	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("✅ Total: %d modules\n", len(result.Modules))

	return nil
}

// ============================================================================
// Helper Functions
// ============================================================================

func printSummary(result *deps.AnalyzeResult) {
	fmt.Println("\n📦 Module Analysis")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	// Print modules
	for _, module := range result.Modules {
		printModuleDetail(module)
	}

	fmt.Println("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("✅ Found %d modules\n", len(result.Modules))
	if len(result.LanguagesDetected) > 0 {
		fmt.Printf("✅ Languages: %v\n", result.LanguagesDetected)
	}
	fmt.Printf("✅ %d internal dependencies\n", result.InternalDepsCount)
	fmt.Printf("✅ Confidence: %d%%\n", result.Confidence)
}

func printModuleDetail(m *deps.Module) {
	fmt.Printf("\n📁 %s (%s)", m.Name, m.Type)
	if m.Language != "" {
		fmt.Printf(" [%s]", m.Language)
	}
	fmt.Println()

	if len(m.DependsOn) > 0 {
		fmt.Println("   depends on:")
		for _, dep := range m.DependsOn {
			fmt.Printf("      └─ %s\n", dep)
		}
	}
	if len(m.CalledBy) > 0 {
		fmt.Println("   called by:")
		for _, caller := range m.CalledBy {
			fmt.Printf("      └─ %s\n", caller)
		}
	}
}

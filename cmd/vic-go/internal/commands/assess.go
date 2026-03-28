package commands

import (
	"fmt"
	"os/exec"
	"strconv"
	"strings"

	"github.com/spf13/cobra"
	"github.com/vic-sdd/vic/internal/config"
)

// ChangeType represents the type of change detected
type ChangeType string

const (
	ChangeTypeTypoFix            ChangeType = "typo_fix"
	ChangeTypeRenameRefactor     ChangeType = "rename_refactor"
	ChangeTypeBugFix             ChangeType = "bug_fix"
	ChangeTypeFeatureAddition    ChangeType = "feature_addition"
	ChangeTypeArchitectureChange ChangeType = "architecture_change"
)

// RiskLevel represents the risk level of a change
type RiskLevel string

const (
	RiskLevelMinimal  RiskLevel = "minimal"
	RiskLevelLow      RiskLevel = "low"
	RiskLevelMedium   RiskLevel = "medium"
	RiskLevelHigh     RiskLevel = "high"
	RiskLevelCritical RiskLevel = "critical"
)

// AssessmentResult contains the result of change assessment
type AssessmentResult struct {
	ChangeType      ChangeType `json:"change_type"`
	RiskScore       float64    `json:"risk_score"`
	RiskLevel       RiskLevel  `json:"risk_level"`
	GatesRequired   []int      `json:"gates_required"`
	RecommendedSkill string    `json:"recommended_skill"`
	AutoSwitch      bool       `json:"auto_switch"`
	Details         AssessmentDetails `json:"details"`
}

// AssessmentDetails contains detailed assessment information
type AssessmentDetails struct {
	FilesChanged   int    `json:"files_changed"`
	LinesChanged   int    `json:"lines_changed"`
	Scope          int    `json:"scope"`
	Complexity     int    `json:"complexity"`
	SPECImpact     int    `json:"spec_impact"`
	TestCoverage   int    `json:"test_coverage"`
	HasLogicChange bool   `json:"has_logic_change"`
	SPECAffected   bool   `json:"spec_affected"`
}

// NewAssessCmd creates the assess command
func NewAssessCmd(cfg *config.Config) *cobra.Command {
	var showDetails bool
	var outputFormat string

	cmd := &cobra.Command{
		Use:   "assess",
		Short: "Intelligent change assessment",
		Long: `Analyze current changes and determine:
- Change type (typo_fix, bug_fix, feature_addition, etc.)
- Risk level (minimal, low, medium, high, critical)
- Required gates
- Recommended skill
- Auto-switch recommendation`,
		Example: `  vic assess              # Basic assessment
  vic assess --details   # Show detailed breakdown
  vic assess --output json  # JSON output`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAssess(cfg, showDetails, outputFormat)
		},
	}

	cmd.Flags().BoolVarP(&showDetails, "details", "d", false, "Show detailed assessment breakdown")
	cmd.Flags().StringVarP(&outputFormat, "output", "o", "plain", "Output format (plain, json)")

	return cmd
}

func runAssess(cfg *config.Config, showDetails bool, outputFormat string) error {
	// Get git diff information
	details, err := getGitDiffDetails()
	if err != nil {
		return fmt.Errorf("failed to get git diff: %w", err)
	}

	// Detect change type
	changeType := detectChangeTypeFromDetails(details)

	// Assess risk
	riskScore, riskLevel := assessRisk(details)

	// Determine required gates
	gatesRequired := getRequiredGates(riskLevel)

	// Recommend skill
	recommendedSkill := getRecommendedSkill(changeType, riskLevel)

	// Build result
	result := AssessmentResult{
		ChangeType:       changeType,
		RiskScore:        riskScore,
		RiskLevel:        riskLevel,
		GatesRequired:    gatesRequired,
		RecommendedSkill: recommendedSkill,
		AutoSwitch:       riskLevel != RiskLevelCritical,
		Details:          details,
	}

	// Output result
	if outputFormat == "json" {
		return outputJSON(result)
	}

	return outputPlain(result, showDetails)
}

func getGitDiffDetails() (AssessmentDetails, error) {
	details := AssessmentDetails{}

	// Get files changed
	filesCmd := exec.Command("git", "diff", "--name-only")
	filesOutput, err := filesCmd.Output()
	if err != nil {
		return details, fmt.Errorf("git diff --name-only failed: %w", err)
	}
	files := strings.Split(strings.TrimSpace(string(filesOutput)), "\n")
	if len(files) == 1 && files[0] == "" {
		files = []string{}
	}
	details.FilesChanged = len(files)

	// Check SPEC affected
	for _, file := range files {
		if strings.Contains(file, "SPEC-") && strings.HasSuffix(file, ".md") {
			details.SPECAffected = true
			break
		}
		if strings.HasPrefix(file, ".vic-sdd/") {
			details.SPECAffected = true
			break
		}
	}

	// Get lines changed
	statCmd := exec.Command("git", "diff", "--stat")
	statOutput, err := statCmd.Output()
	if err != nil {
		return details, fmt.Errorf("git diff --stat failed: %w", err)
	}
	details.LinesChanged = parseLinesFromStat(string(statOutput))

	// Check for logic changes
	diffCmd := exec.Command("git", "diff", "--unified=0")
	diffOutput, err := diffCmd.Output()
	if err != nil {
		return details, fmt.Errorf("git diff failed: %w", err)
	}
	details.HasLogicChange = hasLogicChange(string(diffOutput))

	// Calculate scope
	details.Scope = calculateScope(details.FilesChanged, files)

	// Calculate complexity
	details.Complexity = calculateComplexity(string(diffOutput), details.HasLogicChange)

	// Calculate SPEC impact
	details.SPECImpact = calculateSPECImpact(details.SPECAffected, details.Scope)

	// Calculate test coverage need
	details.TestCoverage = calculateTestCoverage(details.HasLogicChange, details.FilesChanged)

	return details, nil
}

func parseLinesFromStat(stat string) int {
	// Parse output like: "file.go | 10 +++++-----"
	lines := 0
	for _, line := range strings.Split(stat, "\n") {
		if strings.Contains(line, "|") {
			parts := strings.Split(line, "|")
			if len(parts) >= 2 {
				changePart := strings.TrimSpace(parts[1])
				// Extract number before +/-
				numStr := ""
				for _, c := range changePart {
					if c >= '0' && c <= '9' {
						numStr += string(c)
					} else {
						break
					}
				}
				if num, err := strconv.Atoi(numStr); err == nil {
					lines += num
				}
			}
		}
	}
	return lines
}

func hasLogicChange(diff string) bool {
	// Check for logic-related patterns
	logicPatterns := []string{
		"if ", "for ", "while ", "switch ",
		"function ", "func ", "def ", "class ",
		"async ", "await ", "Promise ",
		"return ", "throw ", "try ", "catch ",
	}

	for _, pattern := range logicPatterns {
		if strings.Contains(diff, "+"+pattern) || strings.Contains(diff, "-"+pattern) {
			return true
		}
	}
	return false
}

func calculateScope(filesChanged int, files []string) int {
	// Count unique directories/modules
	modules := make(map[string]bool)
	for _, file := range files {
		parts := strings.Split(file, "/")
		if len(parts) >= 2 {
			modules[parts[0]+"/"+parts[1]] = true
		} else if len(parts) == 1 {
			modules[parts[0]] = true
		}
	}

	if filesChanged == 1 {
		return 1 // Single file
	}
	if len(modules) == 1 {
		return 2 // Single module
	}
	if len(modules) <= 3 {
		return 3 // Multiple modules
	}
	return 4 // Cross-cutting
}

func calculateComplexity(diff string, hasLogicChange bool) int {
	if !hasLogicChange {
		return 1 // Trivial
	}

	// Count complex patterns
	complexPatterns := 0
	patterns := []string{"async", "await", "Promise", "thread", "lock", "transaction"}
	for _, p := range patterns {
		complexPatterns += strings.Count(diff, p)
	}

	// Count new abstractions
	abstractions := strings.Count(diff, "interface") + strings.Count(diff, "abstract")

	if abstractions > 0 {
		return 4 // Complex
	}
	if complexPatterns > 3 {
		return 3 // Moderate
	}
	return 2 // Simple
}

func calculateSPECImpact(specAffected bool, scope int) int {
	if specAffected {
		return 3 // Major
	}
	if scope >= 3 {
		return 2 // Moderate
	}
	if scope == 2 {
		return 1 // Minor
	}
	return 0 // None
}

func calculateTestCoverage(hasLogicChange bool, filesChanged int) int {
	if !hasLogicChange {
		return 0 // Existing sufficient
	}
	if filesChanged > 3 {
		return 3 // Needs integration
	}
	return 2 // Needs new tests
}

func detectChangeTypeFromDetails(details AssessmentDetails) ChangeType {
	// Priority-based detection

	// 1. Architecture change
	if details.SPECAffected || details.FilesChanged > 10 {
		return ChangeTypeArchitectureChange
	}

	// 2. Check for feature keywords (would need task description in real implementation)
	// For now, use heuristics based on change patterns

	// 3. Feature addition (new files, new logic)
	if details.HasLogicChange && details.FilesChanged > 1 {
		return ChangeTypeFeatureAddition
	}

	// 4. Bug fix (logic change but localized)
	if details.HasLogicChange && details.FilesChanged <= 2 {
		return ChangeTypeBugFix
	}

	// 5. Rename refactor (no logic change, multiple files)
	if !details.HasLogicChange && details.FilesChanged > 1 && details.FilesChanged <= 5 {
		return ChangeTypeRenameRefactor
	}

	// 6. Typo fix (no logic change, single file, small)
	if !details.HasLogicChange && details.FilesChanged == 1 && details.LinesChanged < 10 {
		return ChangeTypeTypoFix
	}

	// Default to feature addition
	return ChangeTypeFeatureAddition
}

func assessRisk(details AssessmentDetails) (float64, RiskLevel) {
	score := float64(details.Scope+details.Complexity+details.SPECImpact+details.TestCoverage) / 4.0

	var level RiskLevel
	switch {
	case score < 1.0:
		level = RiskLevelMinimal
	case score < 1.5:
		level = RiskLevelLow
	case score < 2.5:
		level = RiskLevelMedium
	case score < 3.5:
		level = RiskLevelHigh
	default:
		level = RiskLevelCritical
	}

	return score, level
}

func getRequiredGates(riskLevel RiskLevel) []int {
	switch riskLevel {
	case RiskLevelMinimal:
		return []int{}
	case RiskLevelLow:
		return []int{2}
	case RiskLevelMedium:
		return []int{2, 3}
	case RiskLevelHigh:
		return []int{0, 2, 3}
	case RiskLevelCritical:
		return []int{0, 1, 2, 3}
	default:
		return []int{0, 1, 2, 3}
	}
}

func getRecommendedSkill(changeType ChangeType, riskLevel RiskLevel) string {
	switch {
	case changeType == ChangeTypeTypoFix || changeType == ChangeTypeRenameRefactor:
		return "quick"
	case riskLevel == RiskLevelCritical:
		return "spec-workflow"
	default:
		return "implementation"
	}
}

func outputJSON(result AssessmentResult) error {
	// Simple JSON output
	fmt.Printf(`{
  "change_type": "%s",
  "risk_score": %.2f,
  "risk_level": "%s",
  "gates_required": %v,
  "recommended_skill": "%s",
  "auto_switch": %v
}`, result.ChangeType, result.RiskScore, result.RiskLevel, result.GatesRequired, result.RecommendedSkill, result.AutoSwitch)
	fmt.Println()
	return nil
}

func outputPlain(result AssessmentResult, showDetails bool) error {
	fmt.Println()
	fmt.Println("🔍 VIBE-SDD Change Assessment")
	fmt.Println("========================================")
	fmt.Println()

	// Change type with icon
	typeIcon := getChangeTypeIcon(result.ChangeType)
	fmt.Printf("📋 Change Type: %s %s\n", typeIcon, result.ChangeType)

	// Risk level with color indicator
	riskIcon := getRiskIcon(result.RiskLevel)
	fmt.Printf("⚠️  Risk Level: %s %s (%.2f)\n", riskIcon, result.RiskLevel, result.RiskScore)

	// Gates required
	gatesStr := "None"
	if len(result.GatesRequired) > 0 {
		gatesStr = fmt.Sprintf("%v", result.GatesRequired)
	}
	fmt.Printf("🚪 Gates Required: %s\n", gatesStr)

	// Recommended skill
	skillIcon := getSkillIcon(result.RecommendedSkill)
	fmt.Printf("🎯 Recommended Skill: %s %s\n", skillIcon, result.RecommendedSkill)

	// Auto-switch
	autoStr := "yes"
	if !result.AutoSwitch {
		autoStr = "no (requires human checkpoint)"
	}
	fmt.Printf("🔄 Auto-switch: %s\n", autoStr)

	// Details
	if showDetails {
		fmt.Println()
		fmt.Println("📊 Assessment Details")
		fmt.Println("----------------------------------------")
		fmt.Printf("   Files Changed: %d\n", result.Details.FilesChanged)
		fmt.Printf("   Lines Changed: %d\n", result.Details.LinesChanged)
		fmt.Printf("   Scope: %d/4\n", result.Details.Scope)
		fmt.Printf("   Complexity: %d/4\n", result.Details.Complexity)
		fmt.Printf("   SPEC Impact: %d/3\n", result.Details.SPECImpact)
		fmt.Printf("   Test Coverage Need: %d/3\n", result.Details.TestCoverage)
		fmt.Printf("   Logic Change: %v\n", result.Details.HasLogicChange)
		fmt.Printf("   SPEC Affected: %v\n", result.Details.SPECAffected)
	}

	fmt.Println()
	fmt.Println("========================================")

	// Next step suggestion
	if result.RecommendedSkill == "quick" {
		fmt.Println("✅ This is a simple change - quick workflow recommended")
	} else if result.RecommendedSkill == "spec-workflow" {
		fmt.Println("⚠️  This requires SPEC review before implementation")
		fmt.Println("   Run: vic spec status")
	} else {
		fmt.Println("📝 Ready for implementation workflow")
		if len(result.GatesRequired) > 0 {
			fmt.Printf("   Required gates: %v\n", result.GatesRequired)
		}
	}

	return nil
}

func getChangeTypeIcon(ct ChangeType) string {
	switch ct {
	case ChangeTypeTypoFix:
		return "✏️"
	case ChangeTypeRenameRefactor:
		return "📝"
	case ChangeTypeBugFix:
		return "🐛"
	case ChangeTypeFeatureAddition:
		return "✨"
	case ChangeTypeArchitectureChange:
		return "🏗️"
	default:
		return "📋"
	}
}

func getRiskIcon(rl RiskLevel) string {
	switch rl {
	case RiskLevelMinimal:
		return "🟢"
	case RiskLevelLow:
		return "🔵"
	case RiskLevelMedium:
		return "🟡"
	case RiskLevelHigh:
		return "🟠"
	case RiskLevelCritical:
		return "🔴"
	default:
		return "⚪"
	}
}

func getSkillIcon(skill string) string {
	switch skill {
	case "quick":
		return "⚡"
	case "spec-workflow":
		return "📐"
	case "implementation":
		return "🔨"
	case "unified-workflow":
		return "🎯"
	default:
		return "📋"
	}
}

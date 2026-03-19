package commands

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/vic-sdd/vic/internal/config"
	"github.com/vic-sdd/vic/internal/types"
	"github.com/vic-sdd/vic/internal/utils"
	"gopkg.in/yaml.v3"
)

// NewCostCmd creates the cost command
func NewCostCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "cost",
		Short: "Cost tracking management",
		Long:  `Manage token and cost tracking for AI usage.`,
		Example: `  vic cost init              # Initialize cost tracking
  vic cost status           # Show current costs
  vic cost set-budget 50    # Set budget ceiling to $50`,
	}

	cmd.AddCommand(NewCostInitCmd(cfg))
	cmd.AddCommand(NewCostStatusCmd(cfg))
	cmd.AddCommand(NewCostSetBudgetCmd(cfg))
	cmd.AddCommand(NewCostAddCmd(cfg))

	return cmd
}

// ============================================
// Init Command
// ============================================

// NewCostInitCmd creates the cost init subcommand
func NewCostInitCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:   "init",
		Short: "Initialize cost tracking",
		Long:  `Initialize cost tracking with default budget settings.`,
		Example: `  vic cost init
  vic cost init --budget 100 --alert 0.8`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCostInit(cfg)
		},
	}
}

func runCostInit(cfg *config.Config) error {
	// Check if already initialized
	if utils.FileExists(cfg.CostTrackingFile) {
		fmt.Println("⚠️  Cost tracking already initialized")
		fmt.Printf("   File: %s\n", cfg.CostTrackingFile)
		fmt.Println("   Use 'vic cost status' to view current tracking")
		return nil
	}

	// Create new cost tracking
	costFile := types.CostTrackingFile{
		Version: "1.0",
		Tracking: types.CostTracking{
			Session: types.CostSession{
				InputTokens:  0,
				OutputTokens: 0,
				Cost:         0,
			},
			ProjectTotal: types.ProjectCost{
				InputTokens:  0,
				OutputTokens: 0,
				Cost:         0,
			},
			Budget: types.BudgetConfig{
				Ceiling:        50.0, // Default $50
				AlertThreshold: 0.8,  // 80%
				AutoPause:      true,
			},
			WarningIssued: false,
		},
	}

	// Save
	if err := saveCostTracking(cfg, &costFile); err != nil {
		return fmt.Errorf("failed to save cost tracking: %w", err)
	}

	fmt.Println("✅ Cost tracking initialized")
	fmt.Println("")
	fmt.Println("   Default settings:")
	fmt.Printf("   • Budget ceiling: $%.2f\n", costFile.Tracking.Budget.Ceiling)
	fmt.Printf("   • Alert threshold: %.0f%%\n", costFile.Tracking.Budget.AlertThreshold*100)
	fmt.Printf("   • Auto-pause: %v\n", costFile.Tracking.Budget.AutoPause)
	fmt.Println("")
	fmt.Println("   Use 'vic cost set-budget' to adjust")
	fmt.Println("   Use 'vic cost add' to record token usage")

	return nil
}

// ============================================
// Status Command
// ============================================

// NewCostStatusCmd creates the cost status subcommand
func NewCostStatusCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:     "status",
		Short:   "Show cost status",
		Long:    `Show current cost tracking status and projections.`,
		Example: `  vic cost status`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCostStatus(cfg)
		},
	}
}

func runCostStatus(cfg *config.Config) error {
	costFile, err := loadCostTracking(cfg)
	if err != nil {
		fmt.Println("⚠️  Cost tracking not initialized")
		fmt.Printf("   Run 'vic cost init' to start tracking\n")
		return nil
	}

	fmt.Println("═══════════════════════════════════════════════════════════")
	fmt.Println("  💰 Cost Tracking Status")
	fmt.Println("═══════════════════════════════════════════════════════════")

	// Session costs
	fmt.Println("")
	fmt.Println("  📊 本次会话 (Session)")
	fmt.Println("  ──────────────────────────────────────────────")
	fmt.Printf("  Token (输入):  %d\n", costFile.Tracking.Session.InputTokens)
	fmt.Printf("  Token (输出):  %d\n", costFile.Tracking.Session.OutputTokens)
	fmt.Printf("  成本:          $%.2f\n", costFile.Tracking.Session.Cost)

	// Project total
	fmt.Println("")
	fmt.Println("  📈 项目总计 (Project Total)")
	fmt.Println("  ──────────────────────────────────────────────")
	fmt.Printf("  Token (输入):  %d\n", costFile.Tracking.ProjectTotal.InputTokens)
	fmt.Printf("  Token (输出):  %d\n", costFile.Tracking.ProjectTotal.OutputTokens)
	fmt.Printf("  成本:          $%.2f\n", costFile.Tracking.ProjectTotal.Cost)

	// Budget
	if costFile.Tracking.Budget.Ceiling > 0 {
		fmt.Println("")
		fmt.Println("  💵 预算 (Budget)")
		fmt.Println("  ──────────────────────────────────────────────")
		fmt.Printf("  预算上限:     $%.2f\n", costFile.Tracking.Budget.Ceiling)
		fmt.Printf("  已使用:       $%.2f (%.1f%%)\n", costFile.Tracking.ProjectTotal.Cost, (costFile.Tracking.ProjectTotal.Cost/costFile.Tracking.Budget.Ceiling)*100)
		fmt.Printf("  剩余:         $%.2f\n", costFile.Tracking.Budget.Ceiling-costFile.Tracking.ProjectTotal.Cost)
		fmt.Printf("  警告阈值:     %.0f%%\n", costFile.Tracking.Budget.AlertThreshold*100)
		fmt.Printf("  自动暂停:     %v\n", costFile.Tracking.Budget.AutoPause)

		// Warning
		if costFile.Tracking.ProjectTotal.Cost >= costFile.Tracking.Budget.Ceiling*costFile.Tracking.Budget.AlertThreshold {
			fmt.Println("")
			if costFile.Tracking.ProjectTotal.Cost >= costFile.Tracking.Budget.Ceiling {
				fmt.Println("  ⚠️  预算已耗尽! Auto mode 将暂停")
			} else {
				fmt.Println("  ⚠️  接近预算上限!")
			}
		}
	}

	fmt.Println("")
	fmt.Println("═══════════════════════════════════════════════════════════")

	return nil
}

// ============================================
// Set Budget Command
// ============================================

// NewCostSetBudgetCmd creates the cost set-budget subcommand
func NewCostSetBudgetCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:   "set-budget [amount]",
		Short: "Set budget ceiling",
		Long:  `Set the budget ceiling in USD. Auto mode will pause when threshold is reached.`,
		Example: `  vic cost set-budget 100      # Set $100 ceiling
  vic cost set-budget 0       # Disable budget`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runCostSetBudget(cfg, args[0])
		},
	}
}

func runCostSetBudget(cfg *config.Config, amountStr string) error {
	var amount float64
	if _, err := fmt.Sscanf(amountStr, "%f", &amount); err != nil {
		return fmt.Errorf("invalid amount: %s", amountStr)
	}

	costFile, err := loadCostTracking(cfg)
	if err != nil {
		// Create new if not exists
		costFile = &types.CostTrackingFile{
			Version: "1.0",
			Tracking: types.CostTracking{
				Budget: types.BudgetConfig{
					Ceiling:        amount,
					AlertThreshold: 0.8,
					AutoPause:      true,
				},
			},
		}
	}

	costFile.Tracking.Budget.Ceiling = amount

	if err := saveCostTracking(cfg, costFile); err != nil {
		return fmt.Errorf("failed to save: %w", err)
	}

	if amount == 0 {
		fmt.Println("✅ Budget disabled")
	} else {
		fmt.Printf("✅ Budget set to $%.2f\n", amount)
	}

	return nil
}

// ============================================
// Add Cost Command
// ============================================

// NewCostAddCmd creates the cost add subcommand
func NewCostAddCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:   "add",
		Short: "Add cost record",
		Long:  `Record token usage and cost.`,
		Example: `  vic cost add --input 1000 --output 500 --cost 0.50
  vic cost add --input 5000 --output 2000 --cost 2.00 --phase 1`,
		RunE: func(cmd *cobra.Command, args []string) error {
			inputTokens, _ := cmd.Flags().GetInt64("input")
			outputTokens, _ := cmd.Flags().GetInt64("output")
			cost, _ := cmd.Flags().GetFloat64("cost")
			phase, _ := cmd.Flags().GetInt("phase")
			return runCostAdd(cfg, inputTokens, outputTokens, cost, phase)
		},
	}
}

func runCostAdd(cfg *config.Config, inputTokens, outputTokens int64, cost float64, phase int) error {
	costFile, err := loadCostTracking(cfg)
	if err != nil {
		// Create new
		costFile = &types.CostTrackingFile{
			Version: "1.0",
			Tracking: types.CostTracking{
				Budget: types.BudgetConfig{
					Ceiling:        50.0,
					AlertThreshold: 0.8,
					AutoPause:      true,
				},
			},
		}
	}

	// Add to session
	costFile.Tracking.Session.InputTokens += inputTokens
	costFile.Tracking.Session.OutputTokens += outputTokens
	costFile.Tracking.Session.Cost += cost

	// Add to project total
	costFile.Tracking.ProjectTotal.InputTokens += inputTokens
	costFile.Tracking.ProjectTotal.OutputTokens += outputTokens
	costFile.Tracking.ProjectTotal.Cost += cost

	// Check budget
	if costFile.Tracking.Budget.Ceiling > 0 && costFile.Tracking.ProjectTotal.Cost >= costFile.Tracking.Budget.Ceiling*costFile.Tracking.Budget.AlertThreshold {
		if !costFile.Tracking.WarningIssued {
			costFile.Tracking.WarningIssued = true
			fmt.Println("⚠️  Warning: Approaching budget ceiling!")
			fmt.Printf("   Used: $%.2f / $%.2f (%.1f%%)\n", costFile.Tracking.ProjectTotal.Cost, costFile.Tracking.Budget.Ceiling, (costFile.Tracking.ProjectTotal.Cost/costFile.Tracking.Budget.Ceiling)*100)
		}
	}

	if costFile.Tracking.Budget.Ceiling > 0 && costFile.Tracking.ProjectTotal.Cost >= costFile.Tracking.Budget.Ceiling {
		if costFile.Tracking.Budget.AutoPause {
			fmt.Println("🛑 Budget exceeded! Auto mode will pause.")
		}
	}

	if err := saveCostTracking(cfg, costFile); err != nil {
		return fmt.Errorf("failed to save: %w", err)
	}

	fmt.Println("✅ Cost recorded")
	fmt.Printf("   Added: Input %d, Output %d, Cost $%.2f\n", inputTokens, outputTokens, cost)
	fmt.Printf("   Session total: $%.2f\n", costFile.Tracking.Session.Cost)
	fmt.Printf("   Project total: $%.2f\n", costFile.Tracking.ProjectTotal.Cost)

	return nil
}

// ============================================
// Helper Functions
// ============================================

func saveCostTracking(cfg *config.Config, costFile *types.CostTrackingFile) error {
	// Ensure status directory exists
	statusDir := cfg.ProjectDir + "/status"
	if !utils.FileExists(statusDir) {
		if err := os.MkdirAll(statusDir, 0755); err != nil {
			return fmt.Errorf("failed to create status directory: %w", err)
		}
	}

	data, err := yaml.Marshal(costFile)
	if err != nil {
		return fmt.Errorf("failed to marshal cost tracking: %w", err)
	}

	header := []byte(`# Cost Tracking - VIBE-SDD
# Auto-generated by vic-go
# Do not edit manually - use vic cost commands

`)
	if err := os.WriteFile(cfg.CostTrackingFile, append(header, data...), 0644); err != nil {
		return fmt.Errorf("failed to write cost tracking file: %w", err)
	}

	return nil
}

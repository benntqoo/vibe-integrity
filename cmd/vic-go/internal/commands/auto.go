package commands

import (
	"fmt"
	"os"
	"time"

	"github.com/spf13/cobra"
	"github.com/vic-sdd/vic/internal/config"
	"github.com/vic-sdd/vic/internal/types"
	"github.com/vic-sdd/vic/internal/utils"
	"gopkg.in/yaml.v3"
)

// NewAutoCmd creates the auto command
func NewAutoCmd(cfg *config.Config) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "auto",
		Short: "Autonomous execution mode",
		Long:  `Manage autonomous execution mode with state persistence and crash recovery.`,
		Example: `  vic auto start           # Start autonomous mode
  vic auto status          # Show auto mode status
  vic auto pause          # Pause autonomous mode
  vic auto resume         # Resume autonomous mode
  vic auto stop           # Stop autonomous mode`,
	}

	cmd.AddCommand(NewAutoStartCmd(cfg))
	cmd.AddCommand(NewAutoStatusCmd(cfg))
	cmd.AddCommand(NewAutoPauseCmd(cfg))
	cmd.AddCommand(NewAutoResumeCmd(cfg))
	cmd.AddCommand(NewAutoStopCmd(cfg))

	return cmd
}

// ============================================
// Start Command
// ============================================

// NewAutoStartCmd creates the auto start subcommand
func NewAutoStartCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:   "start",
		Short: "Start autonomous mode",
		Long:  `Start autonomous execution mode. Saves state to disk for crash recovery.`,
		Example: `  vic auto start
  vic auto start --max-cost 10.00`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAutoStart(cfg)
		},
	}
}

func runAutoStart(cfg *config.Config) error {
	// Load existing state or create new
	autoFile, err := loadAutoState(cfg)
	if err != nil {
		return fmt.Errorf("failed to load auto state: %w", err)
	}

	// Check if already running
	if autoFile.State.Status == "running" {
		fmt.Println("⚠️  Auto mode is already running")
		fmt.Printf("   Current: Phase %d, Task: %s\n", autoFile.State.CurrentPhase, autoFile.State.CurrentTask)
		fmt.Println("   Use 'vic auto resume' to continue")
		return nil
	}

	// Update state
	autoFile.State.Enabled = true
	autoFile.State.Status = "running"
	autoFile.State.LastDispatch = time.Now()

	// Save
	if err := saveAutoState(cfg, autoFile); err != nil {
		return fmt.Errorf("failed to save auto state: %w", err)
	}

	fmt.Println("🚀 Auto mode started")
	fmt.Println("")
	fmt.Println("   Current state:")
	fmt.Printf("   • Phase: %d\n", autoFile.State.CurrentPhase)
	fmt.Printf("   • Slice: %d\n", autoFile.State.CurrentSlice)
	fmt.Printf("   • Task: %s\n", autoFile.State.CurrentTask)
	fmt.Printf("   • Dispatch count: %d\n", autoFile.State.DispatchCount)
	fmt.Printf("   • Total cost: $%.2f\n", autoFile.State.TotalCost)
	fmt.Println("")
	fmt.Println("   Use 'vic auto status' to monitor progress")
	fmt.Println("   Use 'vic auto pause' to pause")
	fmt.Println("   Use 'vic auto stop' to stop")

	return nil
}

// ============================================
// Status Command
// ============================================

// NewAutoStatusCmd creates the auto status subcommand
func NewAutoStatusCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:     "status",
		Short:   "Show auto mode status",
		Long:    `Show current status of autonomous execution mode.`,
		Example: `  vic auto status`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAutoStatus(cfg)
		},
	}
}

func runAutoStatus(cfg *config.Config) error {
	autoFile, err := loadAutoState(cfg)
	if err != nil {
		return fmt.Errorf("failed to load auto state: %w", err)
	}

	// Load cost tracking
	costFile, _ := loadCostTracking(cfg)

	statusIcon := "⏹️"
	switch autoFile.State.Status {
	case "running":
		statusIcon = "🔄"
	case "paused":
		statusIcon = "⏸️"
	case "completed":
		statusIcon = "✅"
	case "failed":
		statusIcon = "❌"
	}

	fmt.Println("═══════════════════════════════════════════════════════════")
	fmt.Println("  VIC-SDD Auto Mode Status")
	fmt.Println("═══════════════════════════════════════════════════════════")
	fmt.Printf("\n📊 Status: %s %s\n", statusIcon, autoFile.State.Status)
	fmt.Printf("📍 Current Phase: %d\n", autoFile.State.CurrentPhase)
	fmt.Printf("📦 Current Slice: %d\n", autoFile.State.CurrentSlice)
	fmt.Printf("📝 Current Task: %s\n", autoFile.State.CurrentTask)

	if !autoFile.State.LastDispatch.IsZero() {
		fmt.Printf("⏱️  Last Dispatch: %s\n", autoFile.State.LastDispatch.Format("2006-01-02 15:04:05"))
	}

	fmt.Println("")
	fmt.Println("───────────────────────────────────────────────────────────")
	fmt.Println("  💰 Cost Tracking")
	fmt.Println("───────────────────────────────────────────────────────────")

	if costFile != nil {
		fmt.Printf("\n  本次会话 (Session):\n")
		fmt.Printf("    Token (输入):  %d\n", costFile.Tracking.Session.InputTokens)
		fmt.Printf("    Token (输出):  %d\n", costFile.Tracking.Session.OutputTokens)
		fmt.Printf("    成本:          $%.2f\n", costFile.Tracking.Session.Cost)

		fmt.Printf("\n  项目总计 (Project Total):\n")
		fmt.Printf("    Token (输入):  %d\n", costFile.Tracking.ProjectTotal.InputTokens)
		fmt.Printf("    Token (输出):  %d\n", costFile.Tracking.ProjectTotal.OutputTokens)
		fmt.Printf("    成本:          $%.2f\n", costFile.Tracking.ProjectTotal.Cost)

		if costFile.Tracking.Budget.Ceiling > 0 {
			usedPercent := (costFile.Tracking.ProjectTotal.Cost / costFile.Tracking.Budget.Ceiling) * 100
			fmt.Printf("\n  💵 预算状态:\n")
			fmt.Printf("    预算上限:     $%.2f\n", costFile.Tracking.Budget.Ceiling)
			fmt.Printf("    已使用:       %.0f%%\n", usedPercent)
			if usedPercent >= costFile.Tracking.Budget.AlertThreshold*100 {
				fmt.Println("    ⚠️  接近预算上限!")
			}
		}
	} else {
		fmt.Println("  成本追踪未初始化 (Run 'vic cost init' to start tracking)")
	}

	fmt.Println("")
	fmt.Println("───────────────────────────────────────────────────────────")
	fmt.Println("  🔧 Dispatch Statistics")
	fmt.Println("───────────────────────────────────────────────────────────")
	fmt.Printf("\n  Dispatch Count: %d\n", autoFile.State.DispatchCount)
	fmt.Printf("  Total Cost: $%.2f\n", autoFile.State.TotalCost)

	// Show recovery info
	if len(autoFile.Recovery.DispatchHistory) > 0 {
		fmt.Println("")
		fmt.Println("  📜 Recent Dispatches:")
		recentCount := 3
		if len(autoFile.Recovery.DispatchHistory) < recentCount {
			recentCount = len(autoFile.Recovery.DispatchHistory)
		}
		for i := len(autoFile.Recovery.DispatchHistory) - recentCount; i < len(autoFile.Recovery.DispatchHistory); i++ {
			entry := autoFile.Recovery.DispatchHistory[i]
			statusIcon := "⏳"
			if entry.Status == "completed" {
				statusIcon = "✅"
			} else if entry.Status == "failed" {
				statusIcon = "❌"
			}
			fmt.Printf("    %s %s - %s (%s)\n", statusIcon, entry.ID, entry.Skill, entry.Status)
		}
	}

	// Show crash sessions if any
	if len(autoFile.Recovery.CrashSessions) > 0 {
		fmt.Println("")
		fmt.Println("  ⚠️  Crash Sessions:")
		for _, crash := range autoFile.Recovery.CrashSessions {
			fmt.Printf("    • %s - Phase %d, Task: %s\n", crash.CrashedAt.Format("2006-01-02 15:04"), crash.LastPhase, crash.LastTask)
		}
	}

	fmt.Println("")
	fmt.Println("═══════════════════════════════════════════════════════════")

	// Show next steps
	if autoFile.State.Status == "running" {
		fmt.Println("\n   Next: 'vic auto pause' to pause, 'vic auto stop' to stop")
	} else if autoFile.State.Status == "paused" {
		fmt.Println("\n   Next: 'vic auto resume' to continue")
	}

	return nil
}

// ============================================
// Pause Command
// ============================================

// NewAutoPauseCmd creates the auto pause subcommand
func NewAutoPauseCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:     "pause",
		Short:   "Pause autonomous mode",
		Long:    `Pause autonomous execution. State is preserved for later resume.`,
		Example: `  vic auto pause`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAutoPause(cfg)
		},
	}
}

func runAutoPause(cfg *config.Config) error {
	autoFile, err := loadAutoState(cfg)
	if err != nil {
		return fmt.Errorf("failed to load auto state: %w", err)
	}

	if autoFile.State.Status != "running" {
		fmt.Println("⚠️  Auto mode is not running")
		if autoFile.State.Status == "paused" {
			fmt.Println("   Already paused")
		}
		return nil
	}

	autoFile.State.Status = "paused"

	if err := saveAutoState(cfg, autoFile); err != nil {
		return fmt.Errorf("failed to save auto state: %w", err)
	}

	fmt.Println("⏸️  Auto mode paused")
	fmt.Println("")
	fmt.Println("   State preserved:")
	fmt.Printf("   • Phase: %d, Slice: %d, Task: %s\n", autoFile.State.CurrentPhase, autoFile.State.CurrentSlice, autoFile.State.CurrentTask)
	fmt.Printf("   • Dispatch count: %d\n", autoFile.State.DispatchCount)
	fmt.Println("")
	fmt.Println("   Use 'vic auto resume' to continue")
	fmt.Println("   Use 'vic auto stop' to end")

	return nil
}

// ============================================
// Resume Command
// ============================================

// NewAutoResumeCmd creates the auto resume subcommand
func NewAutoResumeCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:     "resume",
		Short:   "Resume autonomous mode",
		Long:    `Resume autonomous execution from paused state.`,
		Example: `  vic auto resume`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAutoResume(cfg)
		},
	}
}

func runAutoResume(cfg *config.Config) error {
	autoFile, err := loadAutoState(cfg)
	if err != nil {
		return fmt.Errorf("failed to load auto state: %w", err)
	}

	if autoFile.State.Status != "paused" {
		if autoFile.State.Status == "running" {
			fmt.Println("⚠️  Auto mode is already running")
			return nil
		}
		fmt.Println("⚠️  No paused session to resume")
		fmt.Println("   Use 'vic auto start' to start a new session")
		return nil
	}

	// Check for crash recovery
	if len(autoFile.Recovery.CrashSessions) > 0 {
		lastCrash := autoFile.Recovery.CrashSessions[len(autoFile.Recovery.CrashSessions)-1]
		fmt.Println("🔄 Recovery mode detected")
		fmt.Printf("   Last crash: %s\n", lastCrash.CrashedAt.Format("2006-01-02 15:04:05"))
		fmt.Printf("   Last task: %s\n", lastCrash.LastTask)
		fmt.Println("")
		fmt.Println("   Resuming from last checkpoint...")

		// Record recovery
		crashSession := types.CrashSession{
			ID:          fmt.Sprintf("CRASH-%d", len(autoFile.Recovery.CrashSessions)),
			StartedAt:   lastCrash.CrashedAt,
			CrashedAt:   time.Now(),
			LastPhase:   autoFile.State.CurrentPhase,
			LastTask:    autoFile.State.CurrentTask,
			Recoverable: true,
		}
		autoFile.Recovery.CrashSessions = append(autoFile.Recovery.CrashSessions, crashSession)
	}

	autoFile.State.Status = "running"
	autoFile.State.LastDispatch = time.Now()

	if err := saveAutoState(cfg, autoFile); err != nil {
		return fmt.Errorf("failed to save auto state: %w", err)
	}

	fmt.Println("✅ Auto mode resumed")
	fmt.Println("")
	fmt.Printf("   Continuing from: Phase %d, Slice %d, Task: %s\n", autoFile.State.CurrentPhase, autoFile.State.CurrentSlice, autoFile.State.CurrentTask)

	return nil
}

// ============================================
// Stop Command
// ============================================

// NewAutoStopCmd creates the auto stop subcommand
func NewAutoStopCmd(cfg *config.Config) *cobra.Command {
	return &cobra.Command{
		Use:     "stop",
		Short:   "Stop autonomous mode",
		Long:    `Stop autonomous execution and save final state.`,
		Example: `  vic auto stop`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runAutoStop(cfg)
		},
	}
}

func runAutoStop(cfg *config.Config) error {
	autoFile, err := loadAutoState(cfg)
	if err != nil {
		return fmt.Errorf("failed to load auto state: %w", err)
	}

	if autoFile.State.Status == "idle" {
		fmt.Println("⚠️  Auto mode is not running")
		return nil
	}

	fmt.Println("🛑 Stopping auto mode...")
	fmt.Println("")

	// Record final dispatch if any
	if autoFile.State.DispatchCount > 0 {
		fmt.Printf("   Total dispatches: %d\n", autoFile.State.DispatchCount)
		fmt.Printf("   Total cost: $%.2f\n", autoFile.State.TotalCost)
	}

	// Update state
	autoFile.State.Enabled = false
	autoFile.State.Status = "idle"

	if err := saveAutoState(cfg, autoFile); err != nil {
		return fmt.Errorf("failed to save auto state: %w", err)
	}

	fmt.Println("✅ Auto mode stopped")
	fmt.Println("")
	fmt.Println("   State has been saved.")
	fmt.Println("   Use 'vic auto start' to begin a new session")

	return nil
}

// ============================================
// Helper Functions
// ============================================

func loadAutoState(cfg *config.Config) (*types.AutoModeFile, error) {
	if !utils.FileExists(cfg.AutoStateFile) {
		// Return default state
		return &types.AutoModeFile{
			Version: "1.0",
			State: types.AutoModeState{
				Enabled:      false,
				CurrentPhase: 0,
				CurrentSlice: 1,
				CurrentTask:  "",
				Status:       "idle",
			},
			Recovery: types.Recovery{
				Enabled:            true,
				CheckpointInterval: 300, // 5 minutes
				PendingOperations:  []types.PendingOperation{},
				DispatchHistory:    []types.DispatchHistoryEntry{},
				CrashSessions:      []types.CrashSession{},
			},
			Config: types.AutoModeConfig{
				Enabled:            true,
				CheckpointInterval: 300,
				MaxDispatchCount:   100,
				MaxCostPerSession:  50.0,
				AutoPauseOnWarning: true,
				RecoveryEnabled:    true,
			},
		}, nil
	}

	data, err := os.ReadFile(cfg.AutoStateFile)
	if err != nil {
		return nil, fmt.Errorf("failed to read auto state file: %w", err)
	}

	var autoFile types.AutoModeFile
	if err := yaml.Unmarshal(data, &autoFile); err != nil {
		return nil, fmt.Errorf("failed to parse auto state file: %w", err)
	}

	return &autoFile, nil
}

func saveAutoState(cfg *config.Config, autoFile *types.AutoModeFile) error {
	// Ensure status directory exists
	statusDir := cfg.ProjectDir + "/status"
	if !utils.FileExists(statusDir) {
		if err := os.MkdirAll(statusDir, 0755); err != nil {
			return fmt.Errorf("failed to create status directory: %w", err)
		}
	}

	data, err := yaml.Marshal(autoFile)
	if err != nil {
		return fmt.Errorf("failed to marshal auto state: %w", err)
	}

	header := []byte(`# Auto Mode State - VIBE-SDD
# Auto-generated by vic-go
# Do not edit manually - use vic auto commands

`)
	if err := os.WriteFile(cfg.AutoStateFile, append(header, data...), 0644); err != nil {
		return fmt.Errorf("failed to write auto state file: %w", err)
	}

	return nil
}

func loadCostTracking(cfg *config.Config) (*types.CostTrackingFile, error) {
	if !utils.FileExists(cfg.CostTrackingFile) {
		return nil, fmt.Errorf("cost tracking file not found")
	}

	data, err := os.ReadFile(cfg.CostTrackingFile)
	if err != nil {
		return nil, fmt.Errorf("failed to read cost tracking file: %w", err)
	}

	var costFile types.CostTrackingFile
	if err := yaml.Unmarshal(data, &costFile); err != nil {
		return nil, fmt.Errorf("failed to parse cost tracking file: %w", err)
	}

	return &costFile, nil
}

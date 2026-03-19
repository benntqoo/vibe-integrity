package types

// ============================================
// Cost Tracking Types
// ============================================

// CostTracking represents the cost tracking state
type CostTracking struct {
	Session       CostSession  `yaml:"session"`
	ProjectTotal  ProjectCost  `yaml:"project_total"`
	Budget        BudgetConfig `yaml:"budget"`
	WarningIssued bool         `yaml:"warning_issued"`
}

// CostSession represents costs for the current session
type CostSession struct {
	InputTokens  int64   `yaml:"input_tokens"`
	OutputTokens int64   `yaml:"output_tokens"`
	Cost         float64 `yaml:"cost"`
}

// ProjectCost represents cumulative project costs
type ProjectCost struct {
	InputTokens  int64   `yaml:"input_tokens"`
	OutputTokens int64   `yaml:"output_tokens"`
	Cost         float64 `yaml:"cost"`
}

// BudgetConfig represents budget settings
type BudgetConfig struct {
	Ceiling        float64 `yaml:"ceiling"`
	AlertThreshold float64 `yaml:"alert_threshold"` // percentage (0.0-1.0)
	AutoPause      bool    `yaml:"auto_pause"`
}

// CostTrackingFile represents the cost tracking persistence file
type CostTrackingFile struct {
	Version  string       `yaml:"version,omitempty"`
	Tracking CostTracking `yaml:"tracking"`
}

// TokenUsage represents token usage for a single operation
type TokenUsage struct {
	Model        string  `yaml:"model"`
	InputTokens  int64   `yaml:"input_tokens"`
	OutputTokens int64   `yaml:"output_tokens"`
	Cost         float64 `yaml:"cost"`
}

// CostBreakdown represents a detailed cost breakdown
type CostBreakdown struct {
	TotalInputTokens  int64              `yaml:"total_input_tokens"`
	TotalOutputTokens int64              `yaml:"total_output_tokens"`
	TotalCost         float64            `yaml:"total_cost"`
	ByPhase           map[int]float64    `yaml:"by_phase"`
	BySkill           map[string]float64 `yaml:"by_skill"`
}

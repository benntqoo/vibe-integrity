package types

import "time"

// ============================================
// Replan Types
// ============================================

// ReplanTrigger represents what triggered a replan
type ReplanTrigger string

const (
	ReplanTriggerResearch      ReplanTrigger = "research_complete"
	ReplanTriggerSliceComplete ReplanTrigger = "slice_complete"
	ReplanTriggerUserRequest   ReplanTrigger = "user_request"
	ReplanTriggerTechSurprise  ReplanTrigger = "technical_surprise"
	ReplanTriggerEnvChange     ReplanTrigger = "environment_change"
)

// ReplanDecision represents a single replan decision
type ReplanDecision struct {
	ID           string        `yaml:"id"`
	Trigger      ReplanTrigger `yaml:"trigger"`
	Timestamp    time.Time     `yaml:"timestamp"`
	Finding      string        `yaml:"finding"`
	OriginalPlan string        `yaml:"original_plan"`
	NewPlan      string        `yaml:"new_plan"`
	Reason       string        `yaml:"reason"`
	UserApproved bool          `yaml:"user_approved"`
	Impact       ReplanImpact  `yaml:"impact"`
}

// ReplanImpact represents the impact of a replan
type ReplanImpact struct {
	ScopeChanges  []string `yaml:"scope_changes"`
	TimelineDelta string   `yaml:"timeline_delta"` // e.g., "+2 hours", "-1 day"
	EffortChange  string   `yaml:"effort_change"`  // increased/decreased/same
	EffortLevel   string   `yaml:"effort_level"`   // low/medium/high
}

// ReplanLogFile represents the replan log
type ReplanLogFile struct {
	Version       string           `yaml:"version"`
	ReplanHistory []ReplanDecision `yaml:"replan_history"`
	LastReplan    time.Time        `yaml:"last_replan"`
}

// ProductRedesign represents a product redesign decision
type ProductRedesign struct {
	ID           string            `yaml:"id"`
	Type         string            `yaml:"type"` // "product-redesign"
	Timestamp    time.Time         `yaml:"timestamp"`
	OriginalReq  string            `yaml:"original_request"`
	RealProduct  string            `yaml:"real_product"`
	Mode         string            `yaml:"mode"` // expansion/selective/hold/reduction
	Decisions    []ProductDecision `yaml:"decisions"`
	UserApproved bool              `yaml:"user_approved"`
}

// ProductDecision represents a single product decision
type ProductDecision struct {
	ID          string `yaml:"id"`
	Description string `yaml:"description"`
	Effort      string `yaml:"effort"` // low/medium/high
	Impact      string `yaml:"impact"` // low/medium/high
	Selected    bool   `yaml:"selected"`
	Reason      string `yaml:"reason,omitempty"`
}

// ProductRecordsFile represents the product redesign records
type ProductRecordsFile struct {
	Version string            `yaml:"version"`
	Records []ProductRedesign `yaml:"records"`
}

package types

import "time"

// ============================================
// Auto Mode Types
// ============================================

// AutoModeState represents the current state of auto mode
type AutoModeState struct {
	Enabled       bool      `yaml:"enabled"`
	CurrentPhase  int       `yaml:"current_phase"`
	CurrentSlice  int       `yaml:"current_slice"`
	CurrentTask   string    `yaml:"current_task"`
	LastDispatch  time.Time `yaml:"last_dispatch"`
	DispatchCount int       `yaml:"dispatch_count"`
	TotalCost     float64   `yaml:"total_cost"`
	Status        string    `yaml:"status"` // idle, running, paused, completed
}

// DispatchHistoryEntry represents a single dispatch record
type DispatchHistoryEntry struct {
	ID               string    `yaml:"id"`
	Timestamp        time.Time `yaml:"timestamp"`
	Skill            string    `yaml:"skill"`
	Task             string    `yaml:"task"`
	Status           string    `yaml:"status"` // pending, in_progress, completed, failed
	ArtifactsWritten []string  `yaml:"artifacts_written"`
	ToolCallsMade    int       `yaml:"tool_calls_made"`
}

// Recovery represents the recovery system state
type Recovery struct {
	Enabled            bool                   `yaml:"enabled"`
	CheckpointInterval int                    `yaml:"checkpoint_interval"` // in seconds
	LastCheckpoint     time.Time              `yaml:"last_checkpoint"`
	PendingOperations  []PendingOperation     `yaml:"pending_operations"`
	DispatchHistory    []DispatchHistoryEntry `yaml:"dispatch_history"`
	CrashSessions      []CrashSession         `yaml:"crash_sessions"`
}

// PendingOperation represents an operation waiting to be completed
type PendingOperation struct {
	ID          string    `yaml:"id"`
	Type        string    `yaml:"type"` // skill_invocation, file_write, command_exec
	Description string    `yaml:"description"`
	CreatedAt   time.Time `yaml:"created_at"`
	Retries     int       `yaml:"retries"`
}

// CrashSession represents a crashed session for recovery
type CrashSession struct {
	ID            string    `yaml:"id"`
	StartedAt     time.Time `yaml:"started_at"`
	CrashedAt     time.Time `yaml:"crashed_at"`
	LastPhase     int       `yaml:"last_phase"`
	LastTask      string    `yaml:"last_task"`
	StateSnapshot string    `yaml:"state_snapshot"` // serialized state
	Recoverable   bool      `yaml:"recoverable"`
}

// AutoModeConfig represents auto mode configuration
type AutoModeConfig struct {
	Enabled            bool    `yaml:"enabled"`
	CheckpointInterval int     `yaml:"checkpoint_interval"` // seconds
	MaxDispatchCount   int     `yaml:"max_dispatch_count"`
	MaxCostPerSession  float64 `yaml:"max_cost_per_session"`
	AutoPauseOnWarning bool    `yaml:"auto_pause_on_warning"`
	RecoveryEnabled    bool    `yaml:"recovery_enabled"`
}

// AutoModeFile represents the auto mode persistence file
type AutoModeFile struct {
	Version  string         `yaml:"version,omitempty"`
	State    AutoModeState  `yaml:"state"`
	Recovery Recovery       `yaml:"recovery"`
	Config   AutoModeConfig `yaml:"config"`
}

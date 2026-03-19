package types

import "time"

// ============================================
// AI Slop Detection Types
// ============================================

// AISlopDetector represents the AI slop detection configuration
type AISlopDetector struct {
	Enabled           bool            `yaml:"enabled"`
	SeverityThreshold string          `yaml:"severity_threshold"` // low, medium, high
	Patterns          []AISlopPattern `yaml:"patterns"`
}

// AISlopPattern represents a single AI slop pattern
type AISlopPattern struct {
	ID          string   `yaml:"id"`
	Type        string   `yaml:"type"`     // design, code, text
	Severity    string   `yaml:"severity"` // low, medium, high
	Pattern     string   `yaml:"pattern"`
	Alternative string   `yaml:"alternative"`
	Files       []string `yaml:"files,omitempty"` // Files where this was found
}

// AISlopReport represents a scan report
type AISlopReport struct {
	Timestamp      time.Time       `yaml:"timestamp"`
	TotalPatterns  int             `yaml:"total_patterns"`
	HighSeverity   int             `yaml:"high_severity"`
	MediumSeverity int             `yaml:"medium_severity"`
	LowSeverity    int             `yaml:"low_severity"`
	Findings       []AISlopFinding `yaml:"findings"`
	Score          string          `yaml:"score"` // A/B/C/D
}

// AISlopFinding represents a single finding
type AISlopFinding struct {
	ID        string `yaml:"id"`
	PatternID string `yaml:"pattern_id"`
	Type      string `yaml:"type"`
	File      string `yaml:"file"`
	Line      int    `yaml:"line"`
	Severity  string `yaml:"severity"`
	Match     string `yaml:"match"`
	Fix       string `yaml:"fix"`
}

// DefaultAISlopPatterns returns the default AI slop patterns
func DefaultAISlopPatterns() []AISlopPattern {
	return []AISlopPattern{
		// Design Patterns
		{
			ID:          "D001",
			Type:        "design",
			Severity:    "high",
			Pattern:     "gradient.*hero|hero.*gradient",
			Alternative: "Use bold typography, real images, or solid colors",
		},
		{
			ID:          "D002",
			Type:        "design",
			Severity:    "high",
			Pattern:     "three.*column|3.*column.*icon|icon.*grid.*3",
			Alternative: "Use asymmetric layouts, two-column, or masonry",
		},
		{
			ID:          "D003",
			Type:        "design",
			Severity:    "medium",
			Pattern:     "border-radius.*8px|uniform.*radius",
			Alternative: "Vary radius by element role (buttons 4px, cards 8px, modals 12px)",
		},
		{
			ID:          "D004",
			Type:        "design",
			Severity:    "high",
			Pattern:     "placeholder.*image|random.*photo|unsplash.*random",
			Alternative: "Use contextually relevant, high-quality images",
		},
		{
			ID:          "D005",
			Type:        "design",
			Severity:    "medium",
			Pattern:     "centered.*everything|all.*center",
			Alternative: "Left-align body text, center headings",
		},
		{
			ID:          "D006",
			Type:        "design",
			Severity:    "medium",
			Pattern:     "clean.*modern|minimalist.*generic",
			Alternative: "Define specific aesthetic direction",
		},
		// Code Patterns
		{
			ID:          "C001",
			Type:        "code",
			Severity:    "high",
			Pattern:     "TODO.*implement|later.*fix|hack.*temporary",
			Alternative: "Complete implementation or create a tracked issue",
		},
		{
			ID:          "C002",
			Type:        "code",
			Severity:    "medium",
			Pattern:     "console\\.log|debugger.*//",
			Alternative: "Use proper logging library or remove debug code",
		},
		{
			ID:          "C003",
			Type:        "code",
			Severity:    "high",
			Pattern:     "as\\s+any|type\\s*assertion|@ts-ignore",
			Alternative: "Use correct type definitions",
		},
		{
			ID:          "C004",
			Type:        "code",
			Severity:    "medium",
			Pattern:     "//.*\\?{2}|magic.*number|hardcoded.*value",
			Alternative: "Define constants, use environment variables",
		},
		{
			ID:          "C005",
			Type:        "code",
			Severity:    "medium",
			Pattern:     "sleep\\(\\d+\\)|setTimeout.*\\d{4}",
			Alternative: "Use proper async/await patterns",
		},
		// Text Patterns
		{
			ID:          "T001",
			Type:        "text",
			Severity:    "high",
			Pattern:     "hello.*world|welcome.*user|Lorem.*ipsum",
			Alternative: "Write specific, contextual copy",
		},
		{
			ID:          "T002",
			Type:        "text",
			Severity:    "medium",
			Pattern:     "get.*started|click.*here|learn.*more",
			Alternative: "Use action-specific CTAs",
		},
		{
			ID:          "T003",
			Type:        "text",
			Severity:    "medium",
			Pattern:     "as.*a.*team|together.*we|join.*our",
			Alternative: "User-centered language",
		},
		{
			ID:          "T004",
			Type:        "text",
			Severity:    "low",
			Pattern:     "©.*2024|powered.*by|made.*with",
			Alternative: "Remove if not needed, or update year",
		},
	}
}

// CalculateScore calculates the AI slop score based on findings
func (r *AISlopReport) CalculateScore() string {
	if r.TotalPatterns == 0 {
		return "A"
	}

	highRatio := float64(r.HighSeverity) / float64(r.TotalPatterns)
	mediumRatio := float64(r.MediumSeverity) / float64(r.TotalPatterns)

	if highRatio >= 0.5 || r.HighSeverity >= 5 {
		return "D"
	}
	if highRatio >= 0.3 || r.HighSeverity >= 3 {
		return "C"
	}
	if mediumRatio >= 0.5 || r.MediumSeverity >= 5 {
		return "B"
	}
	if r.HighSeverity > 0 || r.MediumSeverity > 0 {
		return "B"
	}
	return "A"
}

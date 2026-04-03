package commands

import (
	"regexp"
	"testing"
)

// TestCheckFeaturesHaveCriteria tests the checkFeaturesHaveCriteria function
func TestCheckFeaturesHaveCriteria(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		expected bool
	}{
		{
			name:     "Empty content",
			content:  "",
			expected: true, // No features to check
		},
		{
			name: "Features with acceptance criteria",
			content: `## Key Features
1. Feature One
   - Acceptance: Must work correctly
2. Feature Two
   - Acceptance: Must pass tests`,
			expected: true,
		},
		{
			name: "Features without acceptance criteria",
			content: `## Key Features
- Feature One
- Feature Two
- Feature Three`,
			expected: false, // Less than 50% have criteria
		},
		{
			name: "Numbered features with acceptance criteria",
			content: `## Acceptance Criteria
1.1. Must support tech stacks
   - Acceptance: CLI must accept flags
1.2. Must create SPEC files
   - Acceptance: Files must proper sections`,
			expected: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := checkFeaturesHaveCriteria(tt.content)
			if result.passed != tt.expected {
				t.Errorf("checkFeaturesHaveCriteria() passed = %v, want %v, message: %s",
					result.passed, tt.expected, result.message)
			}
		})
	}
}

// TestGate0ChecksPatterns tests the gate0Checks regex patterns
func TestGate0ChecksPatterns(t *testing.T) {
	tests := []struct {
		id       string
		content  string
		expected bool
	}{
		{"USER_STORIES", "## User Stories\n- As a developer, I can...", true},
		{"USER_STORIES", "No user stories here", false},
		{"KEY_FEATURES", "## Key Features\n1. Feature one", true},
		{"KEY_FEATURES", "## Features\n- Feature list", true},
		{"ACCEPTANCE", "## Acceptance Criteria\n- Given when then", true},
		{"ACCEPTANCE", "## 验收标准\n- 测试", true},
		{"NON_FUNC", "## Non-Functional Requirements\n- Performance", true},
		{"NON_FUNC", "## Security\n- Must be secure", true},
		{"OUT_OF_SCOPE", "## Out of Scope\n- Not included", true},
		{"OUT_OF_SCOPE", "## 不在范围内\n- GUI", true},
	}

	for _, tt := range tests {
		t.Run(tt.id, func(t *testing.T) {
			// Find the matching check
			var found bool
			for _, check := range gate0Checks {
				if check.id == tt.id {
					re := regexp.MustCompile(check.pattern)
					found = re.MatchString(tt.content)
					break
				}
			}
			if found != tt.expected {
				t.Errorf("Pattern match for %s: got %v, want %v", tt.id, found, tt.expected)
			}
		})
	}
}

// TestGate0ResultStructure tests the gate0Result struct
func TestGate0ResultStructure(t *testing.T) {
	result := gate0Result{
		checkID:    "TEST",
		checkName:  "Test Check",
		passed:     true,
		message:    "Test passed",
		lineNumber: 10,
	}

	if result.checkID != "TEST" {
		t.Errorf("Expected checkID 'TEST', got '%s'", result.checkID)
	}
	if result.checkName != "Test Check" {
		t.Errorf("Expected checkName 'Test Check', got '%s'", result.checkName)
	}
	if !result.passed {
		t.Errorf("Expected passed to be true")
	}
	if result.message != "Test passed" {
		t.Errorf("Expected message 'Test passed', got '%s'", result.message)
	}
	if result.lineNumber != 10 {
		t.Errorf("Expected lineNumber 10, got %d", result.lineNumber)
	}
}

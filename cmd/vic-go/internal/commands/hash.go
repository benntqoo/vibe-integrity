package commands

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/spf13/cobra"
	"github.com/vic-sdd/vic/internal/config"
)

var hashCmd = &cobra.Command{
	Use:   "hash",
	Short: "Check SPEC file hashes and detect changes",
	Long: `Calculate hash of SPEC files and compare with last known hash.
            If SPEC has changed since last check, show a diff summary.`,
	Example: `  vic spec hash`,
	RunE: func(cmd *cobra.Command, args []string) error {
		return runHash(cmd, args)
	},
}

type SpecHashRecord struct {
	LastCheck string            `json:"last_check"`
	Hashes    map[string]string `json:"hashes"`
}

func runHash(cmd *cobra.Command, args []string) error {
	cfg := config.Load()

	specDir := filepath.Join(cfg.ProjectDir, ".vic-sdd")
	currentHashes := calculateSpecHashes(specDir)
	record := loadHashRecord(specDir)
	changed, _ := compareHashes(currentHashes, record.Hashes)

	if len(changed) == 0 {
		fmt.Println("✅ SPEC unchanged since last check")
		fmt.Printf("   Last checked: %s\n", record.LastCheck)
		return nil
	}

	fmt.Println("⚠️  SPEC changed since last session")
	fmt.Printf("   Last checked: %s\n", record.LastCheck)
	fmt.Println("\nChanged files:")
	for _, file := range changed {
		fmt.Printf("   • %s\n", file)
	}
	fmt.Println("\n📋 Run 'vic spec diff' for full details")

	record.LastCheck = time.Now().UTC().Format(time.RFC3339)
	record.Hashes = currentHashes
	saveHashRecord(specDir, record)

	return nil
}

func calculateSpecHashes(dir string) map[string]string {
	hashes := make(map[string]string)
	specFiles := []string{"SPEC-REQUIREMENTS.md", "SPEC-ARCHITECTURE.md"}
	for _, file := range specFiles {
		path := filepath.Join(dir, file)
		if data, err := os.ReadFile(path); err == nil {
			hash := sha256.Sum256(data)
			hashes[file] = hex.EncodeToString(hash[:])
		}
	}
	return hashes
}

func loadHashRecord(dir string) *SpecHashRecord {
	path := filepath.Join(dir, "status", "spec-hash.json")
	if data, err := os.ReadFile(path); err == nil {
		var record SpecHashRecord
		if err := json.Unmarshal(data, &record); err == nil {
			return &record
		}
	}
	return &SpecHashRecord{LastCheck: "never", Hashes: make(map[string]string)}
}

func saveHashRecord(dir string, record *SpecHashRecord) {
	path := filepath.Join(dir, "status", "spec-hash.json")
	os.MkdirAll(filepath.Dir(path), 0755)
	data, _ := json.MarshalIndent(record, "", "  ")
	os.WriteFile(path, data, 0644)
}

func compareHashes(current, previous map[string]string) (changed, unchanged []string) {
	for file, hash := range current {
		if prevHash, exists := previous[file]; !exists || prevHash != hash {
			changed = append(changed, file)
		} else {
			unchanged = append(unchanged, file)
		}
	}
	return
}

// NewSpecHashCmd creates the hash command (kept for consistency with other commands)
func NewSpecHashCmd(cfg *config.Config) *cobra.Command {
	return hashCmd
}

# Context Tracker Troubleshooting

## Common Issues

### 1. Context File Missing

**Problem**: `.vic-sdd/context.yaml` doesn't exist

**Solution**:
- Initialize with empty state
- Run `vic context init` if available
- Create manually with basic structure

```yaml
context:
  known: []
  inferred: []
  assumed: []
  unknown: []
signals:
  positive: []
  warnings: []
  blockers: []
confidence: 0.0
```

### 2. Confidence Formula Not Working

**Problem**: Confidence calculation produces unexpected results

**Solutions**:
- Check all signal types are properly recorded
- Ensure positive signals have > 0 weight
- Verify blocker multipliers are correct
- Debug the calculation: `confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals`

### 3. Too Many Blockers

**Problem**: Confidence stays low due to multiple blockers

**Solutions**:
- Address high-priority blockers first
- Use `decision_blocking` for unclear requirements
- Use `unknown_blocking` for external dependencies
- Ask human help when blockers >= 2

### 4. Context Not Updating

**Problem**: Context file doesn't reflect recent changes

**Solutions**:
- Manually edit context.yaml
- Ensure context is updated after major actions
- Check for automation scripts that might overwrite

### 5. Memory Issues

**Problem**: Context file grows too large

**Solutions**:
- Archive old context periodically
- Focus on current session only
- Use `context prune` command if available

## Error Messages

### "Invalid context format"
- **Cause**: YAML syntax error
- **Fix**: Validate YAML structure
- **Solution**: Use YAML validator or formatter

### "Confidence > 1.0"
- **Cause**: Calculation error
- **Fix**: Check signal counts and multipliers
- **Solution**: Recalculate with corrected values

### "Context file corrupted"
- **Cause**: File system error
- **Fix**: Restore from backup or recreate
- **Solution**: Use version control if available

## Best Practices

1. **Update regularly**: After every meaningful action
2. **Be specific**: Clearly document knowledge vs assumptions
3. **Record all signals**: Don't forget negative signals
4. **Review confidence**: If low, investigate blockers
5. **Keep it clean**: Remove obsolete information

## Debug Commands

```bash
# View current context
cat .vic-sdd/context.yaml

# Validate context format
yq validate .vic-sdd/context.yaml

# Check signal counts
grep -c "positive\|warnings\|blockers" .vic-sdd/context.yaml

# Reset context (last resort)
rm .vic-sdd/context.yaml && touch .vic-sdd/context.yaml
```
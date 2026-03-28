# Implementation Troubleshooting

## Common Issues

### 1. TDD Not Working

**Problem**: TDD commands fail or behave unexpectedly

**Solutions**:
- Check if tdd command is available in PATH
- Verify project has proper test setup
- Ensure test directory exists

```bash
# Check if tdd command exists
which vic

# Verify test structure
ls -la tests/
```

**Fix**: Install vic CLI properly

### 2. SPEC Gate Failures

**Problem**: `vic spec gate 2` or `vic spec gate 3` fail

**Solutions**:
- Read gate output carefully
- Fix all blocking issues first
- Update SPEC if code has valid deviations

```bash
# Run gate with blocking check
vic gate check --blocking

# View SPEC diff
vic spec diff
```

### 3. Debug Process Issues

**Problem**: Debug commands don't provide useful information

**Solutions**:
- Ensure problem description is clear
- Provide enough context for pattern matching
- Check if debug logs are enabled

```bash
# Enable debug logging
export DEBUG=debug:*

# Run debug with verbose
vic debug start --problem "clear description" --verbose
```

### 4. AI Slop Detection False Positives

**Problem**: Slop scanner flags acceptable code

**Solutions**:
- Review slop configuration
- Customize rules for your project
- Use `--dry-run` first to preview fixes

```bash
# Preview fixes before applying
vic slop fix --dry-run=true

# Configure slop rules
echo "max_function_length=150" >> .vic-sdd/config.yaml
```

### 5. Test Coverage Issues

**Problem**: Gate 3 fails due to low coverage

**Solutions**:
- Add missing tests
- Improve existing tests
- Adjust coverage thresholds if appropriate

```bash
# Check specific coverage
nyc report --reporter=text

# Generate coverage report
npm run test:coverage
```

## Error Messages

### "TDD command not found"
- **Cause**: vic CLI not installed or not in PATH
- **Fix**: Install vic CLI or add to PATH
- **Solution**: `npm install -g @vic/cli`

### "SPEC file not found"
- **Cause**: Missing SPEC documents
- **Fix**: Create SPEC files
- **Solution**: Use spec-workflow skill

### "Gate check failed"
- **Cause**: Implementation doesn't meet requirements
- **Fix**: Update code or SPEC
- **Solution**: Review gate output and address issues

### "Debug session timeout"
- **Cause**: Debug process took too long
- **Fix**: Break problem into smaller pieces
- **Solution**: Run debug in stages

### "Connection pool exhausted"
- **Cause**: Too many database connections
- **Fix**: Implement connection pooling
- **Solution**: Use connection pool middleware

## Performance Issues

### Slow Test Execution
```bash
# Run tests in parallel
npm test -- --maxWorkers=4

# Cache dependencies
npm install --legacy-peer-deps

# Use test isolation
jest --testTimeout=10000
```

### High Memory Usage
```bash
# Monitor memory
node --inspect index.js

# Optimize memory usage
process.memoryUsage();

# Garbage collection hints
global.gc();
```

## Best Practices

1. **Follow TDD strictly**: Red → Green → Refactor
2. **Keep tests focused**: One assertion per test
3. **Mock external dependencies**: Use test doubles
4. **Update SPEC with changes**: Keep code and SPEC aligned
5. **Review Slop reports**: Don't blindly apply fixes
6. **Document technical decisions**: Use ADRs
7. **Monitor performance**: Profile regularly

## Debugging Commands

```bash
# Start debug session
vic debug start --problem "description"

# View debug logs
vic debug logs

# Exit debug session
vic debug stop

# Check dependencies
vic deps list

# Check dependency impact
vic deps impact <module>
```

## Configuration Tips

Create `.vic-sdd/config.yaml`:
```yaml
tdd:
  timeout: 300
  max_retries: 3

debug:
  max_duration: 600
  verbose: true

slop:
  max_function_length: 150
  max_line_length: 100
  no_magic_numbers: true
```
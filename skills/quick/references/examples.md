# Quick Workflow Examples

## Example 1: Fix a Typo

**Scenario**: Fix typo in README.md

**Before**:
```markdown
# My Project

This is a grate project for managing tasks.
```

**Using Quick Workflow**:
1. Confirm scope: Single file (README.md)
2. Make minimal change
3. Verify no impact on functionality

**After**:
```markdown
# My Project

This is a great project for managing tasks.
```

**Command**:
```bash
# No special vic command needed for typo fix
# Just edit the file and commit
git add README.md
git commit -m "fix: typo in README.md"
```

## Example 2: Rename a Variable

**Scenario**: Rename variable in JavaScript file

**Before**:
```javascript
function getUserData(userId) {
  const userData = database.findUser(userId);
  return userData;
}
```

**Using Quick Workflow**:
1. Confirm scope: Only this file
2. Use IDE refactoring tools
3. Check for LSP errors
4. Run diagnostics

**After**:
```javascript
function getUserData(id) {
  const user = database.findUser(id);
  return user;
}
```

**Command**:
```bash
# Check for impact
vic deps list

# Verify no compilation errors
npm run build
```

## Example 3: Add a Comment

**Scenario**: Add explanatory comment in code

**Before**:
```javascript
function calculateDiscount(price, percentage) {
  return price * (1 - percentage / 100);
}
```

**Using Quick Workflow**:
1. Single file change
2. Add helpful comment
3. No functionality change

**After**:
```javascript
/**
 * Calculate discounted price
 * @param {number} price - Original price
 * @param {number} percentage - Discount percentage (0-100)
 * @returns {number} Discounted price
 */
function calculateDiscount(price, percentage) {
  return price * (1 - percentage / 100);
}
```

## Example 4: Simple Single-File Refactor

**Scenario**: Extract function in a single file

**Before**:
```javascript
function processOrder(order) {
  // Validate order
  if (!order.customer) throw new Error('Customer required');
  if (!order.items) throw new Error('Items required');

  // Calculate total
  let total = 0;
  order.items.forEach(item => {
    total += item.price * item.quantity;
  });

  // Apply discount
  if (order.discount) {
    total = total * (1 - order.discount);
  }

  // Process payment
  const payment = processPayment(total);

  return { order, total, payment };
}
```

**Using Quick Workflow**:
1. Confirm single file scope
2. Extract validation logic
3. No external dependencies changed

**After**:
```javascript
function validateOrder(order) {
  if (!order.customer) throw new Error('Customer required');
  if (!order.items) throw new Error('Items required');
}

function calculateOrderTotal(order) {
  let total = 0;
  order.items.forEach(item => {
    total += item.price * item.quantity;
  });

  if (order.discount) {
    total = total * (1 - order.discount);
  }

  return total;
}

function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  const payment = processPayment(total);

  return { order, total, payment };
}
```

## Example 5: When NOT to Use Quick Workflow

**Scenario**: User wants to add new feature

**Consideration**:
- Multi-file changes needed
- New SPEC required
- Tests needed

**Correct Action**: Use `spec-workflow` skill instead

```bash
# Wrong approach for quick workflow
# This would violate single-file scope
```

```bash
# Right approach
vic spec-workflow  # Proper skill for this task
```

## Quick vs Non-Quick Decision Tree

```
Is change single file?
├── YES
│   ├── Clear scope?
│   │   ├── YES → Use quick
│   │   └── NO → Use implementation
│   └── No SPEC impact?
│       ├── YES → Use quick
│       └── NO → Use spec-workflow
└── NO → Use implementation
```

## Quick Workflow Commands

### Confirm Single File
```bash
vic deps list  # Ensure only one module affected
```

### Check for AI Slop
```bash
vic slop scan --type code
```

### Fix AI Slop
```bash
vic slop fix --dry-run=false
```

### Verify No Impact
```bash
vic check --category <category>  # e.g., tech-stack
vic status  # Overall health check
```

## Common Quick Tasks

### Documentation Fixes
```bash
# Fix broken links
sed -i 's/old-link.com/new-link.com/g' README.md

# Fix formatting
prettier --write docs/*.md
```

### Configuration Updates
```bash
# Update package.json version
npm version patch

# Update environment variables
echo "API_URL=new-url" >> .env
```

### CSS Tweaks
```css
/* Quick style fix */
.button {
  background-color: #007bff; /* Updated color */
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
}
```

### Simple JavaScript Fixes
```javascript
// Fix runtime error
function divide(a, b) {
  if (b === 0) {
    return 0; // Instead of throwing
  }
  return a / b;
}
```

## Escalation Criteria

If any of these conditions are met, escalate to implementation skill:

1. **Multiple Files Changed**
   ```bash
   # Files affected > 1
   git diff --name-only | wc -l > 1
   ```

2. **SPEC Impact Detected**
   ```bash
   # SPEC files modified
   git diff --name-only | grep -E "SPEC-.*\.md"
   ```

3. **Test Files Created**
   ```bash
   # Test files added
   git diff --name-only | grep -E "tests/.*\.test\.js"
   ```

4. **Complex Logic Added**
   ```bash
   # New complex functions
   grep -n "function.*(" src/*.js | wc -l > 5
   ```

## Best Practices for Quick Workflow

1. **Always Confirm Scope**
   - Only one file
   - No SPEC impact
   - No new tests needed

2. **Make Minimal Changes**
   - Don't refactor unnecessarily
   - Don't add features
   - Don't change APIs

3. **Verify After Changes**
   - Run LSP check
   - Build if applicable
   - Test locally

4. **Document Simple Changes**
   - Clear commit messages
   - Reference issue if any
   - Keep it simple

5. **Know When to Escalate**
   - Multi-file changes
   - New requirements
   - Architecture changes
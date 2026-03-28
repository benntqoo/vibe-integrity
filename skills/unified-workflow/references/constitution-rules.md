# Constitution Rules

## Overview

The constitution defines the fundamental rules and principles that govern the software delivery process. These rules are enforced by the unified-workflow skill to ensure quality, maintainability, and consistency.

## Constitution File Location

```
.vic-sdd/constitution.yaml
```

## Core Principles

### 1. Single Responsibility Principle (SRP)

**Rule**: Every module should have only one reason to change

**Enforcement**:
- Module complexity metrics
- Change impact analysis
- Coupling measurements

**Configuration**:
```yaml
principles:
  srp:
    enabled: true
    max_complexity: 10
    max_cohesion: 0.8
```

**Violation Examples**:
```javascript
// Bad: User module handles both auth and notifications
class User {
  login(email, password) { /* ... */ }
  sendNotification(user, message) { /* ... */ }
  updateUserProfile(profile) { /* ... */ }
}

// Good: Separate modules
class UserService {
  login(email, password) { /* ... */ }
  updateProfile(profile) { /* ... */ }
}

class NotificationService {
  send(user, message) { /* ... */ }
}
```

### 2. Don't Repeat Yourself (DRY)

**Rule**: Every piece of knowledge must have a single, unambiguous, authoritative representation

**Enforcement**:
- Code duplication detection
- Template reuse validation
- Configuration centralization

**Configuration**:
```yaml
principles:
  dry:
    enabled: true
    max_duplication: 0.1  # 10% max allowed
    require_templates: true
```

**Violation Examples**:
```javascript
// Bad: Duplicated validation logic
function validateUser(user) {
  if (!user.email) throw new Error('Email required');
  if (!user.name) throw new Error('Name required');
  // ... more validation
}

function validateProduct(product) {
  if (!product.name) throw new Error('Name required');
  if (!product.price) throw new Error('Price required');
  // ... similar validation pattern
}

// Good: Shared validation
function validateRequired(obj, fields) {
  fields.forEach(field => {
    if (!obj[field]) throw new Error(`${field} required`);
  });
}
```

### 3. Open/Closed Principle (OCP)

**Rule**: Software entities should be open for extension, but closed for modification

**Enforcement**:
- Extension points validation
- Modification tracking
- Plugin architecture checks

**Configuration**:
```yaml
principles:
  ocp:
    enabled: true
    require_plugins: true
    max_modifications: 5  # Max direct modifications per module
```

**Violation Examples**:
```javascript
// Bad: Modifying existing class to add new behavior
class PaymentProcessor {
  process(payment) {
    if (payment.type === 'credit') {
      // Credit card logic
    } else if (payment.type === 'paypal') {
      // PayPal logic
    } else if (payment.type === 'crypto') {
      // New crypto logic added here - violation!
    }
  }
}

// Good: Using strategy pattern
class PaymentProcessor {
  constructor() {
    this.strategies = new Map();
  }

  registerStrategy(type, strategy) {
    this.strategies.set(type, strategy);
  }

  process(payment) {
    const strategy = this.strategies.get(payment.type);
    if (!strategy) throw new Error('Unknown payment type');
    return strategy.process(payment);
  }
}
```

### 4. Dependency Inversion Principle (DIP)

**Rule**: Depend on abstractions, not concretions

**Enforcement**:
- Dependency direction checks
- Interface usage validation
- Circular dependency detection

**Configuration**:
```yaml
principles:
  dip:
    enabled: true
    require_interfaces: true
    max_dependencies: 7  // Max dependencies per module
```

**Violation Examples**:
```javascript
// Bad: High-level module depends on low-level
class UserManager {
  constructor() {
    this.db = new MySQLDatabase(); // Direct dependency
  }

  createUser(user) {
    return this.db.save(user);
  }
}

// Good: Dependency injection
class UserManager {
  constructor(database) {
    this.db = database; // Dependency on abstraction
  }

  createUser(user) {
    return this.db.save(user);
  }
}

// With interface
interface Database {
  save(entity): Promise<void>;
}

class MySQLDatabase implements Database {
  save(entity) { /* ... */ }
}
```

## SOLID Principles Check

The system enforces all SOLID principles:

### S - Single Responsibility
**Definition**: A class should have only one reason to change

**Checks**:
- Cyclomatic complexity < 10
- Lines of code < 200
- Number of methods < 10
- Cohesion > 0.8

### O - Open/Closed
**Definition**: Open for extension, closed for modification

**Checks**:
- Extension points > 0
- Direct modifications < 5 per module
- Strategy patterns used
- Plugin architecture

### L - Liskov Substitution
**Definition**: Subtypes must be substitutable for their base types

**Checks**:
- Interface compliance
- Method signatures match
- Pre/post conditions maintained
- No throwing unexpected exceptions

### I - Interface Segregation
**Definition**: Clients should not depend on interfaces they don't use

**Checks**:
- Interface size < 5 methods
- Single responsibility per interface
- No empty methods
- Client-specific interfaces

### D - Dependency Inversion
**Definition**: Depend on abstractions, not concretions

**Checks**:
- No direct instantiations in high-level modules
- Dependency injection used
- Interfaces/abstract classes used
- Dependency direction analysis

## Constitution Check Commands

### Run Constitution Check
```bash
vic constitution check
```

**Output**:
```
Constitution Check Results:
=========================
✓ Single Responsibility Principle: PASSED
✓ Don't Repeat Yourself: PASSED
✓ Open/Closed Principle: PASSED
✓ Liskov Substitution: PASSED
✓ Interface Segregation: PASSED
✓ Dependency Inversion: PASSED
```

### Check Specific Principle
```bash
vic constitution check --principle srp
```

### View Constitution Rules
```bash
vic constitution show
```

### Auto-Fix Violations
```bash
vic constitution fix --auto
```

## Constitution Configuration

### Custom Rules
Add custom rules to `.vic-sdd/constitution.yaml`:

```yaml
rules:
  naming:
    pattern: "^[A-Z][a-zA-Z0-9]*$"
    message: "Class names must be PascalCase"

  method_length:
    max: 50
    message: "Methods should be less than 50 lines"

  complexity:
    max: 10
    message: "Method complexity should be less than 10"
```

### Severity Levels
```yaml
severity:
  critical:  // Must pass
    - srp
    - dip

  high:      // Should pass
    - ocp
    - lsp

  medium:    // Nice to have
    - isp
    - dry

  low:       // Optional
    - naming
    - documentation
```

## Common Issues

### 1. Too Many Dependencies
**Problem**: Module has too many direct dependencies

**Solution**:
- Use dependency injection
- Create facade pattern
- Apply facade pattern

```yaml
// Fix with factory pattern
class ServiceFactory {
  create(serviceName) {
    const dependencies = resolveDependencies(serviceName);
    return new Service(dependencies);
  }
}
```

### 2. Code Duplication
**Problem**: Similar code in multiple places

**Solution**:
- Extract to shared utilities
- Use template methods
- Create base classes

```javascript
// Extract common logic
class ValidationHelper {
  static validateRequired(obj, fields) {
    return fields.every(field => obj[field] !== undefined);
  }
}
```

### 3. Circular Dependencies
**Problem**: Module A depends on B, B depends on A

**Solution**:
- Use event bus
- Apply mediator pattern
- Reorganize modules

```javascript
// Event bus solution
const eventBus = new Event();

class ModuleA {
  doSomething() {
    eventBus.emit('something-happened');
  }
}

class ModuleB {
  constructor() {
    eventBus.on('something-happened', this.handleEvent);
  }
}
```

### 4. Large Classes
**Problem**: Class doing too much

**Solution**:
- Apply Single Responsibility
- Extract new classes
- Use composition over inheritance

```javascript
// Split into focused classes
class OrderProcessor {
  process(order) { /* ... */ }
}

class OrderValidator {
  validate(order) { /* ... */ }
}

class OrderNotifier {
  notify(order) { /* ... */ }
}
```
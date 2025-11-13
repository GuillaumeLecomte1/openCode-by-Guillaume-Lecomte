# Test Suite Runner

Runs the complete test suite with coverage and analysis.

## Usage

Run this command to execute all tests with detailed reporting:
```
/test
```

This will:
- Run all unit and integration tests
- Generate coverage reports
- Identify failing tests
- Suggest fixes for common issues
- Provide performance metrics

## Template

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.\n\n1. First, check what testing framework is being used (jest, vitest, pytest, etc.)\n2. Run the appropriate test command with coverage\n3. Analyze any failures and provide specific suggestions\n4. Check coverage gaps and recommend additional tests",
      "description": "Run tests with coverage",
      "agent": "build"
    }
  }
}
```
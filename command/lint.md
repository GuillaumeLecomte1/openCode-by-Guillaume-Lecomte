# Code Linter and Type Checker

Runs linting and type checking to ensure code quality.

## Usage

Run this command to check code quality:
```
/lint
```

This will:
- Run configured linters (ESLint, Pylint, etc.)
- Execute type checking (TypeScript, mypy, etc.)
- Fix auto-fixable issues
- Report remaining problems with solutions

## Template

```json
{
  "command": {
    "lint": {
      "template": "Run linting and type checking on the codebase. Fix any auto-fixable issues and report the rest.\n\n1. Identify the project's linting setup (ESLint, Prettier, Black, etc.)\n2. Run the linter with auto-fix enabled\n3. Run type checking if applicable\n4. Report any remaining issues with specific solutions\n5. Suggest configuration improvements if needed",
      "description": "Run lint and typecheck",
      "agent": "build"
    }
  }
}
```
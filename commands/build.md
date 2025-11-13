# Project Builder

Builds the project and validates all requirements.

## Usage

Run this command to build and validate:
```
/build
```

This will:
- Execute the build process
- Check for build errors
- Validate dependencies
- Run pre-build checks
- Report build success or failures

## Template

```json
{
  "command": {
    "build": {
      "template": "Build the project and ensure it passes all checks. Report any build errors.\n\n1. Check the project type and build system (webpack, vite, cargo, maven, etc.)\n2. Run dependency checks\n3. Execute the build command\n4. Analyze any build errors\n5. Suggest fixes for common build issues\n6. Verify output files are generated correctly",
      "description": "Build the project",
      "agent": "build"
    }
  }
}
```
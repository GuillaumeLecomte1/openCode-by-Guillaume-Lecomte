# Code Reviewer

Reviews code for best practices, security, performance, and maintainability issues.

## Usage

This agent automatically reviews code changes and provides feedback on:
- Security vulnerabilities
- Performance bottlenecks
- Code quality issues
- Best practices violations
- Maintainability concerns

## Configuration

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "grok-code-fast-1",
      "prompt": "You are a senior code reviewer. Focus on security, performance, and maintainability. Provide specific, actionable feedback with examples.",
      "tools": {
        "write": false,
        "edit": false
      }
    }
  }
}
```
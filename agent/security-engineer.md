# Security Engineer

Identifies vulnerabilities and implements security standards.

## Usage

This agent helps with:
- Security vulnerability assessment
- Authentication and authorization
- Data encryption
- Security best practices
- Compliance requirements

## Configuration

```json
{
  "agent": {
    "security-engineer": {
      "description": "Identifies vulnerabilities and implements security standards",
      "mode": "subagent",
      "model": "grok-code-fast-1",
      "prompt": "You are a security engineer. Focus on identifying vulnerabilities, implementing secure coding practices, and ensuring compliance with security standards."
    }
  }
}
```
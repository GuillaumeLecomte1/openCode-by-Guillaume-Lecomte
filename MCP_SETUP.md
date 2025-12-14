# MCP Configuration Setup Guide

## Overview

This project now automatically generates a proper `.mcp.json` configuration file during installation. This file configures Model Context Protocol (MCP) servers for OpenCode.

## What Changed

### Before
- MCP servers were attempted to be configured in `~/.config/opencode/opencode.json`
- This caused validation errors because OpenCode doesn't support MCP configuration in that file
- Format was invalid (missing `type` field, incorrect structure)

### After
- `.mcp.json` is automatically created in the project root during installation
- Uses the correct OpenCode MCP server format
- Supports filesystem and git MCP servers
- Can be easily extended with additional servers

## Installation

Simply run one of the installer scripts:

```bash
# Full installation with agents and orchestrator
./install-opencode.sh

# Basic installation
./install.sh

# Quick setup from GitHub
curl -fsSL https://raw.githubusercontent.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte/main/quick-setup.sh | bash
```

The installer will automatically:
1. Create `.mcp.json` in the project root
2. Configure filesystem server (project-wide access)
3. Configure git server (git operations)
4. Install required npm packages globally

## MCP Configuration File Format

The generated `.mcp.json` looks like this:

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/full/path/to/project"],
      "env": {}
    },
    "git": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "/full/path/to/project"],
      "env": {}
    }
  }
}
```

## Adding Additional MCP Servers

To add more MCP servers to `.mcp.json`, follow this pattern:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio|http|sse",
      "command": "npx",
      "args": ["-y", "@package/name", "additional-args"],
      "env": {
        "VAR_NAME": "value or ${ENV_VAR}"
      }
    }
  }
}
```

### Example: Adding Context7

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    }
  }
}
```

Then set your environment variable:
```bash
export CONTEXT7_API_KEY="your-api-key"
```

## Scope Options

The `.mcp.json` file is **project-scoped**, meaning:
- It's committed to version control
- It's shared with team members
- It's specific to this project
- Don't store secrets directly in it (use environment variables)

## Troubleshooting

### OpenCode doesn't see the MCP servers

1. Ensure `.mcp.json` is in your project root:
   ```bash
   ls -la .mcp.json
   ```

2. Verify the file format is valid JSON:
   ```bash
   cat .mcp.json | jq .
   ```

3. Check that npm packages are installed:
   ```bash
   npm list -g @modelcontextprotocol/server-filesystem
   npm list -g @modelcontextprotocol/server-git
   ```

4. Restart OpenCode:
   ```bash
   opencode
   ```

### Permission errors with npm packages

If you get permission errors installing global npm packages, try:

```bash
# Create npm global directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# Add to PATH
export PATH=~/.npm-global/bin:$PATH
```

## References

- [OpenCode Documentation](https://opencode.ai/docs)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [Available MCP Servers](https://modelcontextprotocol.io/docs/tools)

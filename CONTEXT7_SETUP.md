# Context7 MCP Integration

This project includes Context7 MCP server integration for up-to-date documentation and code examples.

## Quick Setup

1. **Run the setup script:**

   ```bash
   ./setup-context7.sh
   ```

2. **Or configure manually:**

   ```bash
   # Copy the environment template
   cp .env.example .env

   # Edit .env with your API keys
   nano .env
   ```

## Required API Keys

### Context7 (Required)

- Get your API key from: https://context7.com/dashboard
- Add to `.env`: `CONTEXT7_API_KEY=your_key_here`

### Upstash Redis (Optional - for private caching)

- Get credentials from: https://console.upstash.com/redis
- Add to `.env`:
  ```
  UPSTASH_REDIS_REST_URL=your_redis_url
  UPSTASH_REDIS_REST_TOKEN=your_redis_token
  CONTEXT7_CACHE_TTL=3600
  ```

## Usage Examples

Once configured, use Context7 in your prompts:

```bash
# Create a Next.js middleware with latest docs
"Create a Next.js middleware that checks JWT in cookies. use context7"

# Get React hooks documentation
"Show me React hooks examples. use context7"

# API integration help
"Help me integrate Stripe payment. use context7"
```

## Configuration Files

- `config/global.json`: Main OpenCode configuration (safe to commit)
- `config/global.local.json`: Local overrides with API keys (don't commit)
- `.env`: Environment variables (don't commit)

## Security Notes

⚠️ **Important**: Never commit API keys to version control!

- `.env` is in `.gitignore`
- `config/global.local.json` is in `.gitignore`
- Only use `.env.example` as a template for sharing

## Troubleshooting

If Context7 doesn't work:

1. Check your API key is valid
2. Verify `.env` file is properly formatted
3. Restart OpenCode after configuration changes
4. Check network connectivity

## Documentation

- Context7 Docs: https://context7.com/docs
- MCP Protocol: https://modelcontextprotocol.io
- OpenCode MCP: https://opencode.ai/docs/mcp-servers

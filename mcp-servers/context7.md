# Context7 MCP Server

Documentation caching system using Upstash Redis for fast library documentation access.

## Installation

The Context7 MCP server is included in the installation script. To install manually:

```bash
npm install -g @upstash/context7-mcp
```

## Configuration

Context7 is pre-configured in `config/global.json`:

```json
"context7": {
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_CONTEXT7_API_KEY"]
}
```

## Setup

1. **Get API Key**: Visit [context7.com/dashboard](https://context7.com/dashboard)
2. **Create Account**: Sign up for a free account
3. **Copy API Key**: Get your personal API key for better rate limits
4. **Update Configuration**: Replace `YOUR_CONTEXT7_API_KEY` in the config
5. **Restart OpenCode**: Reload to apply changes

## Usage

Once configured, use Context7 in your prompts:

```bash
# Create a React component with hooks
Create a React component with useState and useEffect hooks. use context7

# Configure Express middleware
Set up Express.js middleware for CORS and JSON parsing. use context7

# Database queries
Write MongoDB aggregation queries for user analytics. use context7
```

## Available Tools

- `resolve-library-id`: Convert library names to Context7-compatible IDs
- `get-library-docs`: Fetch documentation for specific libraries

## Benefits

- 📚 **Up-to-date documentation**: Always get the latest API references
- ⚡ **Fast access**: Cached responses for quick lookups
- 🔍 **Smart search**: Intelligent documentation retrieval
- 🌐 **Wide coverage**: Support for popular libraries and frameworks

## Troubleshooting

If Context7 doesn't work:

1. **Check API Key**: Ensure you replaced `YOUR_CONTEXT7_API_KEY`
2. **Network Issues**: Verify internet connectivity
3. **Rate Limits**: Free tier has usage limits
4. **Restart OpenCode**: Reload the application after config changes

## Libraries Supported

Context7 supports documentation for:
- React, Vue, Angular (frontend frameworks)
- Node.js, Express, Fastify (backend)
- MongoDB, PostgreSQL, MySQL (databases)
- AWS, Google Cloud, Azure (cloud services)
- And many more...

Check [context7.com](https://context7.com) for the complete list.
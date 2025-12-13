#!/bin/bash

# Setup script for OpenCode Context7 integration
# This script helps configure API keys securely

echo "🚀 OpenCode Context7 Setup"
echo "=========================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created!"
else
    echo "ℹ️  .env file already exists"
fi

# Prompt for Context7 API key
echo ""
echo "🔑 Context7 API Key Setup"
echo "Get your API key from: https://context7.com/dashboard"
echo ""
read -p "Enter your Context7 API key (or press Enter to skip): " CONTEXT7_KEY

if [ ! -z "$CONTEXT7_KEY" ]; then
    # Update .env file
    sed -i "s/your_actual_api_key_here/$CONTEXT7_KEY/" .env
    echo "✅ Context7 API key saved to .env"
else
    echo "⚠️  No API key provided - you can add it later to .env"
fi

# Optional: Upstash Redis setup
echo ""
echo "🗄️  Upstash Redis Setup (Optional - for private caching)"
echo "Get credentials from: https://console.upstash.com/redis"
echo ""
read -p "Enter Upstash Redis REST URL (or press Enter to skip): " REDIS_URL
read -p "Enter Upstash Redis REST Token (or press Enter to skip): " REDIS_TOKEN

if [ ! -z "$REDIS_URL" ] && [ ! -z "$REDIS_TOKEN" ]; then
    sed -i "s|your_redis_url_here|$REDIS_URL|" .env
    sed -i "s/your_redis_token_here/$REDIS_TOKEN/" .env
    echo "✅ Upstash Redis credentials saved to .env"
else
    echo "ℹ️  Upstash Redis setup skipped"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart OpenCode to load the new configuration"
echo "2. Test with: 'Create a React component. use context7'"
echo ""
echo "📚 Documentation: https://context7.com/docs"
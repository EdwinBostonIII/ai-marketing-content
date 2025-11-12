#!/bin/bash

# ============================================
# SPLANTS Marketing Engine - Quick Start Script
# ============================================
#
# PURPOSE:
#   This script automates the initial setup and launch of SPLANTS
#   Perfect for first-time users who want a guided experience
#
# WHAT IT DOES:
#   1. Checks if Docker is installed and running
#   2. Creates .env file from template if it doesn't exist
#   3. Prompts you to add your OpenAI API key
#   4. Builds and starts all services (database + application)
#   5. Waits for services to become ready
#   6. Shows you how to access the system
#
# REQUIREMENTS:
#   - Docker Desktop installed and running
#   - OpenAI API key (get from platform.openai.com)
#   - 5-10 minutes for first-time setup
#
# USAGE:
#   ./scripts_quick-start.sh
#
# TROUBLESHOOTING:
#   If this script fails:
#   - Make sure Docker is running (look for whale icon)
#   - Check: docker --version
#   - See TROUBLESHOOTING.md for detailed help
#
# ============================================

# Exit immediately if any command fails
# This prevents cascading errors
set -e

echo "================================================"
echo "SPLANTS Marketing Engine - Quick Start"
echo "================================================"
echo ""
echo "This script will help you set up SPLANTS in 5-10 minutes"
echo ""

# ============================================
# STEP 1: Check for Docker
# ============================================

echo "Step 1/5: Checking Docker installation..."
echo ""

# Check if 'docker' command exists
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "Docker is required to run SPLANTS. It's like a 'virtual container'"
    echo "that has everything the software needs to run."
    echo ""
    echo "How to install Docker:"
    echo "  1. Go to: https://docker.com/get-started"
    echo "  2. Download Docker Desktop for your system"
    echo "  3. Install it (takes about 5 minutes)"
    echo "  4. Look for the whale icon in your system tray"
    echo "  5. Run this script again"
    echo ""
    echo "For detailed instructions, see SETUP_GUIDE.md"
    exit 1
fi

# Check if 'docker-compose' command exists
# Note: Newer Docker versions use 'docker compose' (no dash)
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Warning: docker-compose not found"
    echo "Newer Docker Desktop uses 'docker compose' (without dash)"
    echo "We'll try to use that instead..."
    echo ""
    # Create an alias for the rest of this script
    shopt -s expand_aliases
    alias docker-compose='docker compose'
fi

echo "✅ Docker is installed"
echo ""

# ============================================
# STEP 2: Create .env Configuration File
# ============================================

echo "Step 2/5: Setting up configuration..."
echo ""

# Check if .env file already exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    
    # Copy the example file to create .env
    cp .env.example .env
    
    echo "✅ Created .env file"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  IMPORTANT: You need to add your OpenAI API key"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "What is an OpenAI API key?"
    echo "  - It's like a password that lets SPLANTS use OpenAI's AI"
    echo "  - Required for content generation"
    echo "  - Get one at: https://platform.openai.com/api-keys"
    echo ""
    echo "How to add it:"
    echo "  1. Open the .env file in a text editor"
    echo "  2. Find the line: OPENAI_API_KEY=sk-your-api-key-here"
    echo "  3. Replace 'sk-your-api-key-here' with your actual key"
    echo "  4. Save the file"
    echo ""
    echo "Also recommended:"
    echo "  - Change API_KEY to a secure password (protects your system)"
    echo "  - Set MONTHLY_AI_BUDGET to control spending"
    echo ""
    
    # Prompt user to confirm they've added their key
    read -p "Have you added your OpenAI API key to .env? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "No problem! Here's what to do:"
        echo "  1. Edit the .env file now"
        echo "  2. Add your OpenAI API key"
        echo "  3. Run this script again: ./scripts_quick-start.sh"
        echo ""
        exit 1
    fi
else
    echo "✅ .env file already exists"
    echo ""
fi

# ============================================
# STEP 3: Build Docker Images
# ============================================

echo "Step 3/5: Building Docker images..."
echo ""
echo "This may take 5-10 minutes on first run"
echo "(Downloading required software)"
echo ""

# Build the Docker images
# --quiet: Less output, cleaner display
# On error, this will stop due to 'set -e' above
docker-compose build

echo ""
echo "✅ Docker images built successfully"
echo ""

# ============================================
# STEP 4: Start Services
# ============================================

echo "Step 4/5: Starting services..."
echo ""

# Start all services in detached mode (background)
# -d: detached mode (runs in background)
docker-compose up -d

echo ""
echo "✅ Services started"
echo ""

# ============================================
# STEP 5: Wait for Services to Be Ready
# ============================================

echo "Step 5/5: Waiting for services to be ready..."
echo ""
echo "Services need 30-60 seconds to fully initialize"
echo "(Database is creating tables, app is connecting)"
echo ""

# Show a progress indicator
for i in {1..6}; do
    echo "⏳ Waiting... ($i of 6) - $(($i * 10)) seconds elapsed"
    sleep 10
done

echo ""

# ============================================
# STEP 6: Verify Services Are Running
# ============================================

# Check if services are actually running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 SPLANTS Marketing Engine is ready!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 Access Points:"
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   Main API:       http://localhost:8080"
    echo "   API Docs:       http://localhost:8080/docs  👈 Start here!"
    echo "   Health Check:   http://localhost:8080/health"
    echo "   System Status:  http://localhost:8080/v1/system/status"
    echo ""
    echo "📚 Quick Commands:"
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   View logs:      docker-compose logs -f app"
    echo "   Stop services:  docker-compose down"
    echo "   Restart:        docker-compose restart"
    echo "   Check status:   docker-compose ps"
    echo ""
    echo "🎯 Next Steps:"
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   1. Open http://localhost:8080/docs in your browser"
    echo "   2. Click 'Authorize' and enter your API_KEY from .env"
    echo "   3. Try the 'POST /v1/generate' endpoint"
    echo "   4. Generate your first content!"
    echo ""
    echo "📖 Documentation:"
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   Complete Guide:     README.md"
    echo "   Setup Guide:        SETUP_GUIDE.md"
    echo "   Troubleshooting:    TROUBLESHOOTING.md"
    echo "   FAQ:                FAQ.md"
    echo "   API Reference:      docs_API_GUIDE.md"
    echo ""
    echo "💡 Pro Tips:"
    echo "   - Bookmark http://localhost:8080/docs (your main interface)"
    echo "   - Check costs daily at /v1/costs/usage"
    echo "   - Run weekly backups: ./scripts_backup.sh"
    echo "   - See FAQ.md for common questions"
    echo ""
else
    echo "❌ Services failed to start"
    echo ""
    echo "Troubleshooting steps:"
    echo "  1. Check if Docker is running (whale icon)"
    echo "  2. View logs: docker-compose logs"
    echo "  3. See TROUBLESHOOTING.md for solutions"
    echo "  4. Try restarting: docker-compose down && docker-compose up -d"
    echo ""
    exit 1
fi
#!/bin/bash

# Source the .env file
if [ -f ".env" ]; then
    export $(cat .env | xargs)
fi

# Test checking environment variables
echo "Testing environment variables check..."
echo "DATABASE_URL: ${DATABASE_URL:-Not set}"
echo "SECRET_KEY: ${SECRET_KEY:-Not set}"

# Test showing database info
echo -e "\nTesting database info..."
if [ -f "database/ai_task.db" ]; then
    echo "Database file: database/ai_task.db"
    echo "Database size: $(du -h database/ai_task.db | cut -f1)"
else
    echo "Database file not found."
fi

# Test showing project structure
echo -e "\nTesting project structure..."
find . -not -path "*/\.*" -not -path "./venv/*" -type f | head -10

# Test showing API endpoints
echo -e "\nTesting API endpoints..."
echo "Authentication:"
echo "  POST /register         - Register a new user"
echo "  POST /token            - Get an access token"
echo ""
echo "AI Services (requires authentication):"
echo "  POST /api/v1/ai-task   - Perform an AI task"
echo "    Tasks: qa, get_latest_answer, generate_image, generate_content"
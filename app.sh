#!/bin/bash

# AI Task API Terminal Interface
# A comprehensive shell script for interacting with the AI Task API

# Default server configuration
DEFAULT_HOST="localhost"
DEFAULT_PORT="8000"
SERVER_HOST="${HOST:-$DEFAULT_HOST}"
SERVER_PORT="${PORT:-$DEFAULT_PORT}"
BASE_URL="http://$SERVER_HOST:$SERVER_PORT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if server is running
check_server() {
    if curl -s "$BASE_URL" > /dev/null; then
        echo -e "${GREEN}✓ Server is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Server is not running at $BASE_URL${NC}"
        return 1
    fi
}

# Function to display welcome message
show_welcome() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "    AI Task API Terminal Interface      "
    echo "========================================"
    echo -e "${NC}"
    echo "Welcome to the AI Task API terminal interface!"
    echo "This tool allows you to interact with all API functionalities."
    echo ""
}

# Function to show main menu
show_menu() {
    echo "========================================"
    echo "Available Actions:"
    echo "========================================"
    echo "1. Question & Answer"
    echo "2. Get Latest Answer"
    echo "3. Image Generation"
    echo "4. Content Generation"
    echo "5. View API Documentation"
    echo "6. Check Server Status"
    echo "7. Exit"
    echo "========================================"
    echo ""
}

# Function to perform Q&A
perform_qa() {
    echo -e "${BLUE}=== Question & Answer ===${NC}"
    echo "Enter your question:"
    read -r question
    
    echo "Do you want to provide context? (y/n):"
    read -r has_context
    
    context=""
    if [[ "$has_context" == "y" || "$has_context" == "Y" ]]; then
        echo "Enter the context:"
        read -r context
    fi
    
    echo "Processing your request..."
    
    # Prepare JSON payload
    if [[ -n "$context" ]]; then
        payload="{\"task\": \"qa\", \"question\": \"$question\", \"context\": \"$context\"}"
    else
        payload="{\"task\": \"qa\", \"question\": \"$question\"}"
    fi
    
    # Make API request
    response=$(curl -s -X POST "$BASE_URL/ai-task" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    # Extract result from response
    result=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('result', 'No result found'))
except:
    print('Error processing response')
")
    
    echo ""
    echo -e "${GREEN}Answer:${NC}"
    echo "$result"
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Function to get latest answer
get_latest_answer() {
    echo -e "${BLUE}=== Latest Answer ===${NC}"
    echo "Fetching the latest answer..."
    
    # Make API request
    response=$(curl -s -X POST "$BASE_URL/ai-task" \
        -H "Content-Type: application/json" \
        -d "{\"task\": \"latest_answer\"}")
    
    # Extract result from response
    result=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('result', 'No result found'))
except:
    print('Error processing response or no previous answers found')
")
    
    echo ""
    echo -e "${GREEN}Latest Answer:${NC}"
    echo "$result"
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Function to generate image
generate_image() {
    echo -e "${BLUE}=== Image Generation ===${NC}"
    echo "Enter your image prompt:"
    read -r prompt
    
    echo "Generating image based on: $prompt"
    echo "This may take a moment..."
    
    # Make API request
    response=$(curl -s -X POST "$BASE_URL/ai-task" \
        -H "Content-Type: application/json" \
        -d "{\"task\": \"image_generation\", \"prompt\": \"$prompt\"}")
    
    # Extract result from response
    result=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data.get('result', '')
    if result.startswith('Error') or 'simulated' in result.lower():
        print(result)
    else:
        print('Image generated successfully (base64 encoded)')
        print('Length:', len(result), 'characters')
except:
    print('Error processing response')
")
    
    echo ""
    echo -e "${GREEN}Result:${NC}"
    echo "$result"
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Function to generate content
generate_content() {
    echo -e "${BLUE}=== Content Generation ===${NC}"
    echo "Enter your content prompt:"
    read -r prompt
    
    echo "Select platform:"
    echo "1. Twitter"
    echo "2. Facebook"
    echo "3. LinkedIn"
    echo "4. Instagram"
    echo "5. Other"
    read -r platform_choice
    
    case $platform_choice in
        1) platform="twitter" ;;
        2) platform="facebook" ;;
        3) platform="linkedin" ;;
        4) platform="instagram" ;;
        5) 
            echo "Enter platform name:"
            read -r platform
            ;;
        *) platform="default" ;;
    esac
    
    echo "Generating $platform content based on: $prompt"
    
    # Make API request
    response=$(curl -s -X POST "$BASE_URL/ai-task" \
        -H "Content-Type: application/json" \
        -d "{\"task\": \"content_generation\", \"prompt\": \"$prompt\", \"platform\": \"$platform\"}")
    
    # Extract result from response
    result=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('result', 'No result found'))
except:
    print('Error processing response')
")
    
    echo ""
    echo -e "${GREEN}Generated Content:${NC}"
    echo "$result"
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Function to view API documentation
view_docs() {
    echo -e "${BLUE}=== API Documentation ===${NC}"
    echo "Available documentation:"
    echo "1. Swagger UI (Interactive): $BASE_URL/docs"
    echo "2. ReDoc (Alternative): $BASE_URL/redoc"
    echo ""
    echo "You can open these URLs in your web browser to view detailed API documentation."
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Function to check server status
check_status() {
    echo -e "${BLUE}=== Server Status ===${NC}"
    if check_server; then
        echo "Server Details:"
        echo "  Host: $SERVER_HOST"
        echo "  Port: $SERVER_PORT"
        echo "  Base URL: $BASE_URL"
        
        # Get server info
        server_info=$(curl -s "$BASE_URL")
        if [[ -n "$server_info" ]]; then
            echo ""
            echo "Server Response:"
            echo "$server_info" | python3 -m json.tool 2>/dev/null || echo "$server_info"
        fi
    else
        echo "Please make sure the AI Task API server is running."
        echo "To start the server, run: python main.py"
    fi
    echo ""
    echo "Press Enter to continue..."
    read -r
}

# Main interactive loop
main() {
    show_welcome
    
    # Check if server is running
    if ! check_server; then
        echo ""
        echo "Please start the server by running: python main.py"
        echo "Then run this script again."
        exit 1
    fi
    
    while true; do
        show_menu
        echo "Select an option (1-7):"
        read -r choice
        
        case $choice in
            1) perform_qa ;;
            2) get_latest_answer ;;
            3) generate_image ;;
            4) generate_content ;;
            5) view_docs ;;
            6) check_status ;;
            7) 
                echo -e "${GREEN}Thank you for using the AI Task API!${NC}"
                exit 0
                ;;
            *) 
                echo -e "${RED}Invalid option. Please select 1-7.${NC}"
                echo "Press Enter to continue..."
                read -r
                ;;
        esac
    done
}

# Run the main function
main
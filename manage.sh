#!/bin/bash

# AI Task API Management Script
# This script provides a menu interface for managing the AI Task API project

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python is installed
check_python() {
    if ! command_exists python3 && ! command_exists python; then
        print_error "Python is not installed. Please install Python 3.8+ to use this application."
        exit 1
    fi
}

# Function to check if pip is installed
check_pip() {
    if ! command_exists pip3 && ! command_exists pip; then
        print_error "pip is not installed. Please install pip to manage dependencies."
        exit 1
    fi
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found."
        read -p "Do you want to create a virtual environment? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            create_venv
        else
            print_warning "Proceeding without virtual environment. This may cause conflicts with other Python projects."
        fi
    else
        print_info "Virtual environment found."
        activate_venv
    fi
}

# Function to create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    if command_exists python3; then
        python3 -m venv venv
    else
        python -m venv venv
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created successfully."
        activate_venv
    else
        print_error "Failed to create virtual environment."
        exit 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows Git Bash
        source venv/Scripts/activate
    else
        # Linux/Mac
        source venv/bin/activate
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Virtual environment activated."
    else
        print_error "Failed to activate virtual environment."
    fi
}

# Function to install dependencies
install_dependencies() {
    check_pip
    print_info "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully."
    else
        print_error "Failed to install dependencies."
    fi
}

# Function to start the development server
start_server() {
    print_info "Starting development server..."
    print_info "Server will be available at http://localhost:8000"
    print_info "API documentation at http://localhost:8000/docs"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success ".env file created. Please update it with your configuration values."
        else
            print_error ".env.example file not found. Cannot create .env file."
        fi
    fi
    
    # Start the server
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Function to run tests
run_tests() {
    print_info "Running tests..."
    
    # Check if test files exist
    if ls test_*.py 1> /dev/null 2>&1; then
        python -m pytest
    else
        print_warning "No test files found in the current directory."
        print_info "To run tests, create test files with names starting with 'test_'"
        print_info "and install pytest using: pip install pytest"
    fi
}

# Function to create default user
create_default_user() {
    print_info "Creating default user..."
    
    if [ -f "app/create_default_user.py" ]; then
        python app/create_default_user.py
    else
        print_error "Default user creation script not found."
    fi
}

# Function to check environment variables
check_env_vars() {
    print_info "Checking environment variables..."
    
    if [ -f ".env" ]; then
        print_info "Current .env file contents:"
        echo "----------------------------------------"
        cat .env
        echo "----------------------------------------"
    else
        print_warning ".env file not found."
        if [ -f ".env.example" ]; then
            print_info "Example .env file contents:"
            echo "----------------------------------------"
            cat .env.example
            echo "----------------------------------------"
            print_info "To create .env file, run: cp .env.example .env"
        fi
    fi
}

# Function to create database tables
create_db_tables() {
    print_info "Creating database tables..."
    python -c "
import sys
sys.path.append('.')
from app.database import create_db_and_tables
try:
    create_db_and_tables()
    print('Database tables created successfully.')
except Exception as e:
    print(f'Error creating database tables: {e}')
"
}

# Function to reset database
reset_database() {
    print_warning "This will delete all data in the database!"
    read -p "Are you sure you want to reset the database? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Resetting database..."
        
        # Check if database file exists
        if [ -f "database/ai_task.db" ]; then
            rm database/ai_task.db
            print_success "Database file deleted."
        else
            print_warning "Database file not found."
        fi
        
        # Recreate database tables
        create_db_tables
    else
        print_info "Database reset cancelled."
    fi
}

# Function to show database info
show_database_info() {
    print_info "Database Information:"
    
    if [ -f "database/ai_task.db" ]; then
        print_info "Database file: database/ai_task.db"
        print_info "Database size: $(du -h database/ai_task.db | cut -f1)"
    else
        print_warning "Database file not found."
    fi
    
    print_info "Database tables:"
    python -c "
import sys
sys.path.append('.')
from app.database import Base, engine
try:
    for table in Base.metadata.tables.keys():
        print(f'  - {table}')
except Exception as e:
    print(f'Error retrieving database tables: {e}')
"
}

# Function to show project structure
show_project_structure() {
    print_info "Project Structure:"
    echo "----------------------------------------"
    find . -not -path "*/\.*" -not -path "./venv/*" -type f | sort
    echo "----------------------------------------"
}

# Function to show API endpoints
show_api_endpoints() {
    print_info "API Endpoints:"
    echo "----------------------------------------"
    echo "Authentication:"
    echo "  POST /register         - Register a new user"
    echo "  POST /token            - Get an access token"
    echo ""
    echo "AI Services (requires authentication):"
    echo "  POST /api/v1/ai-task   - Perform an AI task"
    echo "    Tasks: qa, get_latest_answer, generate_image, generate_content"
    echo "----------------------------------------"
    echo "Documentation:"
    echo "  http://localhost:8000/docs  - Swagger UI"
    echo "  http://localhost:8000/redoc - ReDoc"
    echo "----------------------------------------"
}

# Function to run demo API calls
run_demo_api() {
    print_info "Running demo API calls..."
    
    # Check if server is running
    if ! nc -z localhost 8000; then
        print_warning "Server is not running on http://localhost:8000"
        print_info "Please start the server first (option 1) or run in another terminal"
        return 1
    fi
    
    # Get access token
    print_info "Getting access token..."
    TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=admin")
    
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "Failed to get access token. Response: $TOKEN_RESPONSE"
        return 1
    fi
    
    print_success "Access token obtained successfully"
    
    # Demo Q&A service
    print_info "Demo: Question & Answer service"
    curl -s -X POST "http://localhost:8000/api/v1/ai-task" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "task": "qa",
            "prompt": "What is the capital of France?"
        }' | python -m json.tool
    
    echo
    
    # Demo image generation service
    print_info "Demo: Image generation service"
    curl -s -X POST "http://localhost:8000/api/v1/ai-task" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "task": "generate_image",
            "prompt": "A beautiful sunset over the mountains"
        }' | python -m json.tool
    
    echo
    
    # Demo content generation service
    print_info "Demo: Content generation service"
    curl -s -X POST "http://localhost:8000/api/v1/ai-task" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "task": "generate_content",
            "prompt": "AI trends in 2025",
            "platform": "twitter"
        }' | python -m json.tool
    
    echo
    
    # Demo get latest answer
    print_info "Demo: Get latest answer"
    curl -s -X POST "http://localhost:8000/api/v1/ai-task" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "task": "get_latest_answer"
        }' | python -m json.tool
    
    echo
    print_success "Demo API calls completed"
}

# Main menu function
show_menu() {
    clear
    echo "========================================"
    echo "        AI Task API Management"
    echo "========================================"
    echo "1. Start development server"
    echo "2. Run tests"
    echo "3. Create default user"
    echo "4. Check environment variables"
    echo "5. Create database tables"
    echo "6. Reset database"
    echo "7. Show database information"
    echo "8. Show project structure"
    echo "9. Show API endpoints"
    echo "10. Install dependencies"
    echo "11. Create virtual environment"
    echo "12. Run demo API calls"
    echo "0. Exit"
    echo "========================================"
}

# Main function
main() {
    # Check if Python is installed
    check_python
    
    # Check if virtual environment exists and activate it
    check_venv
    
    while true; do
        show_menu
        read -p "Enter your choice (0-12): " choice
        echo
        
        case $choice in
            1)
                start_server
                ;;
            2)
                run_tests
                ;;
            3)
                create_default_user
                ;;
            4)
                check_env_vars
                ;;
            5)
                create_db_tables
                ;;
            6)
                reset_database
                ;;
            7)
                show_database_info
                ;;
            8)
                show_project_structure
                ;;
            9)
                show_api_endpoints
                ;;
            10)
                install_dependencies
                ;;
            11)
                create_venv
                ;;
            12)
                run_demo_api
                ;;
            0)
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please enter a number between 0-12."
                ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Run the main function
main
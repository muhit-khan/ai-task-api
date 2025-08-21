# AI Task API

AI Task API is a FastAPI-based web application that provides various AI-powered services including question answering, image generation, and content creation. The application features JWT-based authentication and user management.

## Features

- User registration and authentication with JWT tokens
- Question & Answer service using HuggingFace models
- Image generation service using Stable Diffusion
- Content generation for different platforms using GPT-2
- SQLite database for storing user data and Q&A history
- MCP (Model Context Protocol) integration for extensibility
- RESTful API design with comprehensive error handling

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

### Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd ai-task-api
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Copy the `.env.example` file to `.env`:

     ```bash
     cp .env.example .env
     ```

   - Update the `.env` file with your configuration values, especially:
     - `SECRET_KEY`: Generate a secure random key
     - `HUGGINGFACE_API_KEY`: Your HuggingFace API key for AI services

6. Create the default user:

   ```bash
   python app/create_default_user.py
   ```

## Usage

1. Start the development server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. The API will be available at `http://localhost:8000`

3. API documentation is available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/register` | POST | Register a new user | No |
| `/token` | POST | Get an access token | No |
| `/api/v1/ai-task` | POST | Perform an AI task | Yes |

### AI Services

| Task | Description | Parameters |
|------|-------------|------------|
| `qa` | Question answering service | `prompt` (string) |
| `get_latest_answer` | Retrieve the latest Q&A | None |
| `generate_image` | Generate an image from text | `prompt` (string) |
| `generate_content` | Generate content for a platform | `prompt` (string), `platform` (string) |

### Examples

1. Register a new user:

   ```bash
   curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "full_name": "Test User",
       "password": "testpassword"
     }'
   ```

2. Get an access token:

   ```bash
   curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin"
   ```

3. Perform a Q&A task:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai-task" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "qa",
       "prompt": "What is the weather like in London?"
     }'
   ```

4. Generate an image:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai-task" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "generate_image",
       "prompt": "A beautiful sunset over the mountains"
     }'
   ```

5. Generate content:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai-task" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "generate_content",
       "prompt": "AI trends in 2025",
       "platform": "twitter"
     }'
   ```

6. Get the latest answer:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai-task" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "get_latest_answer"
     }'
   ```

## Project Structure

```
ai-task-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application setup
│   ├── api.py                  # API routes
│   ├── models.py               # Pydantic models
│   ├── database.py             # Database models and setup
│   ├── create_default_user.py  # Script to create default admin user
│   ├── mcp_integration.py      # Model Context Protocol integration
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py     # Authentication service
│       ├── qa_service.py       # Question answering service
│       ├── image_service.py    # Image generation service
│       └── content_service.py  # Content generation service
├── database/
│   └── ai_task.db              # SQLite database file
├── .env                        # Environment variables
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── LICENSE                     # License information
├── CONTRIBUTING.md             # Contribution guidelines
└── README.md                   # This file
```

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DATABASE_URL` | Database connection URL | `sqlite:///./database/ai_task.db` |
| `SECRET_KEY` | Secret key for JWT encoding | `ertyu76543efgjkvfrtylkjh` |
| `ALGORITHM` | Algorithm for JWT encoding | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` |
| `HUGGINGFACE_API_KEY` | API key for HuggingFace services | `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` |
| `MCP_SERVER_NAME` | MCP server name | `AI Task Server` |
| `MCP_SERVER_VERSION` | MCP server version | `1.0.0` |
| `API_V1_STR` | API version string | `/api/v1` |
| `PROJECT_NAME` | Project name | `AI Task API` |
| `DEBUG` | Debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

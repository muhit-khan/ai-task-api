# AI Task API

An API for handling various AI tasks including Q&A, image generation, and content creation using Hugging Face APIs.

## Features

- **Q&A**: Perform question answering with context using Hugging Face models
- **Latest Answer**: Retrieve the most recent answer
- **Image Generation**: Create images from text prompts using Stable Diffusion
- **Content Generation**: Generate platform-specific content (Twitter, Facebook, LinkedIn, etc.) using Hugging Face models
- **MCP Integration**: Minimal client-server setup for AI tool execution

## Tech Stack

- **Backend**: FastAPI (Python 3.12.7)
- **AI Integrations**: HuggingFace API
- **Database**: SQLite
- **MCP Integration**: Basic client-server setup for AI tool calls

## Project Structure

```
ai_task_project/
├── app/
│   ├── api.py                 # /ai-task route handling
│   ├── models.py              # Pydantic models
│   ├── services/
│   │   ├── qa_service.py      # Agent-based Q&A
│   │   ├── image_service.py   # Image generation
│   │   └── content_service.py # Platform-specific content
│   ├── database.py            # DB setup (SQLite)
│   ├── database/              # Database files will be created here
│   └── mcp_integration.py     # MCP client/server integration
├── main.py                    # Unified FastAPI Entry-point
├── app.sh                     # Unified bash script to run all the sample tasks
├── requirements.txt
├── .env                       # Environment variables
├── README.md
└── LICENSE
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-task-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file based on the `.env.example` file and update the values as needed:
   ```
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Main Endpoint

**POST** `/ai-task`

This endpoint handles all AI tasks. The behavior is determined by the `task` field in the request body.

#### 1. Question & Answer

```json
{
  "task": "qa",
  "question": "What is artificial intelligence?",
  "context": "Artificial intelligence is a branch of computer science..."
}
```

#### 2. Fetch Latest Answer

```json
{
  "task": "latest_answer"
}
```

#### 3. Image Generation

```json
{
  "task": "image_generation",
  "prompt": "A beautiful sunset over the mountains"
}
```

#### 4. Content Generation

```json
{
  "task": "content_generation",
  "prompt": "New AI breakthrough in healthcare",
  "platform": "twitter"
}
```

## MCP Integration

This API includes a minimal implementation of the Model Context Protocol (MCP) client for demonstration purposes. In a production environment, this would connect to a full MCP server implementation.

## Database

The application uses SQLite for data persistence. Database files are stored in the `app/database/` directory.

## Deployment

### Local Development

1. Follow the setup instructions above
2. Run the application:
   ```bash
   python main.py
   ```

### Production Deployment

#### Using Uvicorn (for testing)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Using Gunicorn (recommended for production)

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command:
   ```
   pip install -r requirements.txt
   ```
4. Set the start command:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Add environment variables in the Render dashboard as needed

### Deploy to Heroku

1. Create a `Procfile` with the following content:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Create a `runtime.txt` file specifying the Python version:
   ```
   python-3.12.7
   ```

3. Deploy to Heroku using the Heroku CLI:
   ```bash
   heroku create
   git push heroku main
   ```

## Example Usage

After starting the server, you can test the API using curl:

1. **Q&A Task**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task" -H "Content-Type: application/json" -d '{"task": "qa", "question": "What is FastAPI?", "context": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints."}'
   ```

2. **Latest Answer**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task" -H "Content-Type: application/json" -d '{"task": "latest_answer"}'
   ```

3. **Image Generation**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task" -H "Content-Type: application/json" -d '{"task": "image_generation", "prompt": "A red sports car"}'
   ```

4. **Content Generation**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task" -H "Content-Type: application/json" -d '{"task": "content_generation", "prompt": "New features in Python 3.12", "platform": "twitter"}'
   ```

## API Documentation

Once the server is running, you can access the automatic API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

This project is licensed under the MIT License - see the LICENSE file for details.
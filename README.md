# AI Task API

An API for handling various AI tasks including Q&A, image generation, and content creation using AI models.

## Features

- **Q&A**: Perform question answering with context
- **Latest Answer**: Retrieve the most recent answer
- **Image Generation**: Create images from text prompts
- **Content Generation**: Generate platform-specific content (Twitter, Facebook, LinkedIn, etc.)
- **Modern Web Interface**: ChatGPT-like frontend for easy interaction with all AI tasks
- **MCP Integration**: Minimal client-server setup for AI tool execution

## Tech Stack

- **Backend**: FastAPI (Python 3.12.7)
- **AI Integrations**: OpenRouter API (DeepSeek model) for content generation
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript with modern ChatGPT-like interface
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
│   ├── frontend/              # Modern web interface
│   │   ├── index.html         # Main frontend page
│   │   ├── styles.css         # Styling
│   │   ├── script.js          # Frontend logic
│   │   └── README.md          # Frontend documentation
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
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
   
   The application uses `python-dotenv` and `pydantic-settings` to load and validate environment variables. 
   It will raise an error if required environment variables are not set.

5. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Modern Web Interface

The project includes a modern, ChatGPT-like web interface for easy interaction with all AI tasks:

### Features

- **Chat Interface**: Clean, modern chat interface similar to ChatGPT
- **Multiple AI Tasks**: Support for all API functionalities:
  - Question & Answer with context
  - Content Generation for different platforms (Twitter, Facebook, LinkedIn, Instagram, etc.)
  - Image Generation
  - Latest Answer retrieval
- **Responsive Design**: Works on desktop and mobile devices
- **Chat History**: Local storage of conversation history
- **Real-time Status**: API connection status indicator

### Accessing the Interface

Once the server is running, you can access the web interface at:
- **Web Interface**: http://localhost:8000/frontend/index.html

### Usage

1. Open your web browser and navigate to http://localhost:8000/frontend/index.html
2. Select the desired task type from the dropdown:
   - **Question & Answer**: Ask questions with optional context
   - **Content Generation**: Generate platform-specific content (select target platform)
   - **Image Generation**: Create images from text prompts
   - **Latest Answer**: Retrieve the most recent answer from history
3. Enter your prompt/message in the input area
4. For Q&A tasks, optionally provide context in the context input field
5. For Content Generation, select the target platform from the platform dropdown
6. Press Enter or click the send button to submit your request

### Task Types

- **Question & Answer**: Ask questions with optional context
- **Content Generation**: Generate platform-specific content (Twitter, Facebook, LinkedIn, Instagram, YouTube, TikTok)
- **Image Generation**: Create images from text prompts
- **Latest Answer**: Retrieve the most recent answer from history

## API Endpoints

### Main Endpoint

**POST** `/ai-task/`

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
   curl -X POST "http://localhost:8000/ai-task/" -H "Content-Type: application/json" -d '{"task": "qa", "question": "What is FastAPI?", "context": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints."}'
   ```

2. **Latest Answer**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task/" -H "Content-Type: application/json" -d '{"task": "latest_answer"}'
   ```

3. **Image Generation**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task/" -H "Content-Type: application/json" -d '{"task": "image_generation", "prompt": "A red sports car"}'
   ```

4. **Content Generation**:
   ```bash
   curl -X POST "http://localhost:8000/ai-task/" -H "Content-Type: application/json" -d '{"task": "content_generation", "prompt": "New features in Python 3.12", "platform": "twitter"}'
   ```

## API Documentation

Once the server is running, you can access the automatic API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Web Interface**: http://localhost:8000/frontend/index.html

## License

This project is licensed under the MIT License - see the LICENSE file for details.
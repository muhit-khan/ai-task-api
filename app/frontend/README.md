# AI Task Interface Frontend

A modern, ChatGPT-like interface for the AI Task API.

## Features

- **Chat Interface**: Clean, modern chat interface similar to ChatGPT
- **Multiple AI Tasks**: Support for all API functionalities:
  - Question & Answer with context
  - Content Generation for different platforms
  - Image Generation
  - Latest Answer retrieval
- **Responsive Design**: Works on desktop and mobile devices
- **Chat History**: Local storage of conversation history
- **Real-time Status**: API connection status indicator

## Usage

1. Open `index.html` in a web browser
2. Select the desired task type from the dropdown
3. Enter your prompt/message
4. For Q&A tasks, optionally provide context
5. For Content Generation, select the target platform

## Task Types

- **Question & Answer**: Ask questions with optional context
- **Content Generation**: Generate platform-specific content (Twitter, Facebook, LinkedIn, etc.)
- **Image Generation**: Create images from text prompts
- **Latest Answer**: Retrieve the most recent answer from history

## Technical Details

- Pure HTML/CSS/JavaScript frontend
- No build tools required
- Uses Fetch API for communication with backend
- LocalStorage for chat history persistence
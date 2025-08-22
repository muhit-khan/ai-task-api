#!/bin/bash

# app.sh - Run sample tasks for the AI Task API

# Start the server in the background
echo "Starting the AI Task API server..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Give the server a moment to start
sleep 3

echo "Running sample tasks..."

# 1. Q&A Task
echo "1. Running Q&A task..."
curl -X POST "http://localhost:8000/ai-task" \
  -H "Content-Type: application/json" \
  -d '{"task": "qa", "question": "What is artificial intelligence?", "context": "Artificial intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."}'

echo -e "\n---\n"

# 2. Latest Answer Task
echo "2. Fetching latest answer..."
curl -X POST "http://localhost:8000/ai-task" \
  -H "Content-Type: application/json" \
  -d '{"task": "latest_answer"}'

echo -e "\n---\n"

# 3. Image Generation Task
echo "3. Running image generation task..."
curl -X POST "http://localhost:8000/ai-task" \
  -H "Content-Type: application/json" \
  -d '{"task": "image_generation", "prompt": "A beautiful mountain landscape"}'

echo -e "\n---\n"

# 4. Content Generation Task
echo "4. Running content generation task..."
curl -X POST "http://localhost:8000/ai-task" \
  -H "Content-Type: application/json" \
  -d '{"task": "content_generation", "prompt": "Exciting new features in FastAPI", "platform": "twitter"}'

echo -e "\n---\n"

# Kill the server
echo "Stopping the server..."
kill $SERVER_PID

echo "All tasks completed!"
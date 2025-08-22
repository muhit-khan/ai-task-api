# Model Configuration Guide

## Overview

The AI Task API now supports flexible model configuration through environment variables, allowing you to easily switch between different AI models without modifying code.

## Configuration Files

### `.env` File

Your main configuration file. Copy from `.env.example` and customize:

```bash
# API Keys
OPENROUTER_API_KEY=your_actual_openrouter_api_key_here

# Primary Models
CHAT_MODEL=deepseek/deepseek-chat
IMAGE_MODEL=openai/dall-e-3

# Fallback Models (used if primary fails)
CHAT_MODEL_ALTERNATIVE=anthropic/claude-3.5-sonnet
IMAGE_MODEL_ALTERNATIVE=stabilityai/stable-diffusion-xl-base-1.0

# Model Parameters
CHAT_TEMPERATURE=0.7
CHAT_MAX_TOKENS=500
CONTENT_TEMPERATURE=0.8
CONTENT_MAX_TOKENS=300
IMAGE_SIZE=1024x1024
```

## Supported Models

### Chat Models (for Q&A and Content Generation)

- `deepseek/deepseek-chat` - Fast, cost-effective (recommended)
- `anthropic/claude-3.5-sonnet` - High quality, good reasoning
- `openai/gpt-4o` - OpenAI's latest flagship model
- `openai/gpt-4o-mini` - Smaller, faster OpenAI model
- `anthropic/claude-3-opus` - Anthropic's most capable model
- `google/gemini-pro-1.5` - Google's advanced model
- `meta-llama/llama-3.1-405b-instruct` - Meta's large model
- `mistralai/mixtral-8x7b-instruct` - Mistral's mixture of experts

### Image Models

- `openai/dall-e-3` - Latest DALL-E, high quality (recommended)
- `openai/dall-e-2` - Previous DALL-E, good quality, faster
- `stabilityai/stable-diffusion-xl-base-1.0` - Open source, high quality
- `stabilityai/stable-diffusion-3-large` - Latest Stability AI model
- `runwayml/stable-diffusion-v1-5` - Classic Stable Diffusion

## Model Parameters

### Temperature (0.0 - 2.0)

- `0.0-0.3`: Very focused, deterministic responses
- `0.4-0.7`: Balanced creativity and accuracy (recommended)
- `0.8-1.2`: More creative and varied responses
- `1.3-2.0`: Highly creative but potentially inconsistent

### Max Tokens

- `CHAT_MAX_TOKENS`: 100-4000 (500 recommended for Q&A)
- `CONTENT_MAX_TOKENS`: 50-1000 (300 recommended for social media)

### Image Sizes

- `256x256`: Small, fast generation
- `512x512`: Standard size
- `1024x1024`: High quality (recommended)
- `1792x1024`: Wide format (DALL-E 3 only)
- `1024x1792`: Tall format (DALL-E 3 only)

## API Management Endpoints

Monitor and manage your model configuration:

### Get Model Information

```bash
curl http://localhost:8000/ai-task/models/info
```

### Check Current Status

```bash
curl http://localhost:8000/ai-task/models/status
```

### List Popular Models

```bash
curl http://localhost:8000/ai-task/models/popular
```

### Validate Configuration

```bash
curl http://localhost:8000/ai-task/models/validate
```

## Fallback System

The API automatically uses fallback models if the primary model fails:

1. **Primary Model** - Your configured model tries first
2. **Fallback Model** - Alternative model if primary fails
3. **Template Response** - Hard-coded response if both models fail

## Best Practices

### Cost Optimization

- Use `deepseek/deepseek-chat` for cost-effective performance
- Set appropriate max_tokens to control costs
- Use DALL-E 2 for faster, cheaper image generation

### Quality Optimization

- Use `anthropic/claude-3.5-sonnet` for high-quality text
- Use `openai/dall-e-3` for best image quality
- Set temperature around 0.7 for balanced results

### Speed Optimization

- Use smaller models like `openai/gpt-4o-mini`
- Reduce max_tokens for faster responses
- Use 512x512 images for faster generation

## Troubleshooting

### Common Issues

1. **API Key Not Set**

   ```
   Error: OPENROUTER_API_KEY environment variable is not set
   ```

   Solution: Add your OpenRouter API key to `.env`

2. **Model Not Available**

   ```
   Error: Model not found or not available
   ```

   Solution: Check model name spelling or try alternative model

3. **Rate Limiting**

   ```
   Error: Rate limit exceeded
   ```

   Solution: Wait a moment or switch to different model

### Validation

Run the validation endpoint to check your configuration:

```bash
curl http://localhost:8000/ai-task/models/validate
```

## Example Configurations

### High Performance Setup

```bash
CHAT_MODEL=openai/gpt-4o
CHAT_MODEL_ALTERNATIVE=anthropic/claude-3.5-sonnet
IMAGE_MODEL=openai/dall-e-3
CHAT_TEMPERATURE=0.7
CONTENT_TEMPERATURE=0.8
IMAGE_SIZE=1024x1024
```

### Cost-Effective Setup

```bash
CHAT_MODEL=deepseek/deepseek-chat
CHAT_MODEL_ALTERNATIVE=openai/gpt-4o-mini
IMAGE_MODEL=openai/dall-e-2
CHAT_TEMPERATURE=0.6
CONTENT_TEMPERATURE=0.7
IMAGE_SIZE=512x512
```

### Creative Content Setup

```bash
CHAT_MODEL=anthropic/claude-3.5-sonnet
CHAT_MODEL_ALTERNATIVE=openai/gpt-4o
IMAGE_MODEL=openai/dall-e-3
CHAT_TEMPERATURE=0.9
CONTENT_TEMPERATURE=1.0
CONTENT_MAX_TOKENS=500
IMAGE_SIZE=1024x1024
```

## Getting OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Sign up for an account
3. Generate an API key
4. Add credits to your account
5. Copy the key to your `.env` file

## Model Pricing

Check current pricing at [OpenRouter Models](https://openrouter.ai/models) - prices vary by model and usage.

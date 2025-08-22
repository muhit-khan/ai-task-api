import httpx
from typing import Optional
from app.database import ContentRecord, get_db
from app.settings import settings
from sqlalchemy.orm import Session
import json

# Get OpenRouter API key from settings
OPENROUTER_API_KEY = settings.openrouter_api_key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_content(prompt: str, platform: str, db: Optional[Session] = None) -> str:
    """
    Generate 3 platform-specific content variations based on a prompt using OpenRouter API with DeepSeek model
    """
    # Create platform-specific instructions for 3 variations
    platform_instructions = {
        "twitter": f"""
        Create 3 different engaging tweets about: {prompt}.
        
        For each tweet:
        - Must be under 280 characters
        - Use different hooks or trending phrases
        - Include 1–3 relevant trending hashtags
        - Add appropriate emojis
        - Make each tweet unique in style (professional, casual, humorous)
        
        Format your response as:
        **Tweet 1:**
        [first tweet content]
        
        **Tweet 2:**
        [second tweet content]
        
        **Tweet 3:**
        [third tweet content]
        """,
    
        "facebook": f"""
        Create 3 different Facebook posts about: {prompt}.
        
        For each post:
        - Include engaging hooks
        - Keep them personal and community-driven
        - Use different tones (inspirational, conversational, storytelling)
        - Add appropriate call-to-actions
        - Include relevant emojis
        
        Format your response as:
        **Post 1:**
        [first post content]
        
        **Post 2:**
        [second post content]
        
        **Post 3:**
        [third post content]
        """,
    
        "linkedin": f"""
        Create 3 different professional LinkedIn posts about: {prompt}.
        
        For each post:
        - Use professional, insightful tone
        - Include thought-provoking questions or insights
        - Emphasize career growth and industry relevance
        - Use different structures and approaches
        - Include industry-relevant hashtags
        
        Format your response as:
        **Post 1:**
        [first post content]
        
        **Post 2:**
        [second post content]
        
        **Post 3:**
        [third post content]
        """,
    
        "instagram": f"""
        Create 3 different Instagram captions about: {prompt}.
        
        For each caption:
        - Use different aesthetic and emotional hooks
        - Make them fun, creative, and visual
        - Include varied emoji combinations
        - Add relevant hashtags (mix of niche and popular)
        - Include different call-to-actions
        
        Format your response as:
        **Caption 1:**
        [first caption content]
        
        **Caption 2:**
        [second caption content]
        
        **Caption 3:**
        [third caption content]
        """,
    
        "youtube": f"""
        Create 3 different YouTube video descriptions about: {prompt}.
        
        For each description:
        - Begin with attention-grabbing hooks
        - Summarize video content differently
        - Include various call-to-actions
        - Use SEO-friendly keywords naturally
        - Add relevant hashtags
        
        Format your response as:
        **Description 1:**
        [first description content]
        
        **Description 2:**
        [second description content]
        
        **Description 3:**
        [third description content]
        """,
    
        "tiktok": f"""
        Create 3 different TikTok captions about: {prompt}.
        
        For each caption:
        - Keep them short, punchy, and fun
        - Use different trendy styles
        - Include varied trending hashtags
        - Add different emoji combinations
        - Use different engagement hooks
        
        Format your response as:
        **Caption 1:**
        [first caption content]
        
        **Caption 2:**
        [second caption content]
        
        **Caption 3:**
        [third caption content]
        """,
    
        "default": f"""
        Create 3 different engaging posts about: {prompt}.
        
        For each post:
        - Use different tones and approaches
        - Make them appealing to broad audiences
        - Include varied structures and styles
        
        Format your response as:
        **Post 1:**
        [first post content]
        
        **Post 2:**
        [second post content]
        
        **Post 3:**
        [third post content]
        """
    }

    # Get the instruction for the platform
    instruction = platform_instructions.get(platform.lower(), platform_instructions["default"])
    
    # Prepare the payload for OpenRouter API
    payload = {
        "model": settings.chat_model,
        "messages": [
            {
                "role": "system",
                "content": f"You are a creative content writer specializing in {platform} content. Create 3 engaging, platform-appropriate content variations that are distinct and unique from each other."
            },
            {
                "role": "user",
                "content": instruction
            }
        ],
        "temperature": settings.content_temperature,
        "max_tokens": settings.content_max_tokens
    }
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Task API"
    }
    
    # Make the API call using httpx
    try:
        with httpx.Client() as client:
            response = client.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Debug logging
            print(f"API Response for {platform}: {len(content)} characters")
            if len(content) < 100:
                print(f"Warning: Short response for {platform}: {content}")
            
            # If content is empty or too short, use fallback
            if not content.strip() or len(content.strip()) < 50:
                raise Exception("Empty or incomplete response from API")
                
    except Exception as e:
        # Try fallback model if primary model fails
        try:
            payload["model"] = settings.chat_model_alternative
            with httpx.Client() as client:
                response = client.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                print(f"Fallback API Response for {platform}: {len(content)} characters")
                
                if content.strip() and len(content.strip()) >= 50:
                    content += f"\n\n(Generated using fallback model: {settings.chat_model_alternative})"
                else:
                    raise Exception("Empty or incomplete response from fallback model")
                    
        except Exception as fallback_error:
            # Fallback to template-based content if both API calls fail
            platform_templates = {
                "twitter": f"**Tweet 1:**\n🚀 Exciting developments in {prompt}! The future is here. #AI #Tech #Innovation\n\n**Tweet 2:**\n✨ Just discovered something amazing about {prompt}! Mind = blown 🤯 #Technology #Future\n\n**Tweet 3:**\n🔥 {prompt} is changing everything we know! Ready for this? #Innovation #TechNews",
                "facebook": f"**Post 1:**\n🌟 {prompt}\n\nJust discovered something amazing about this topic! The possibilities are endless when technology meets creativity. What are your thoughts?\n\n**Post 2:**\nWow! {prompt} is incredible! 🚀 The future is happening now and it's more exciting than we imagined. Can't wait to see what comes next!\n\n**Post 3:**\nFriends, have you heard about {prompt}? It's absolutely fascinating how this technology is evolving. Drop a comment with your thoughts!",
                "linkedin": f"**Post 1:**\n🔍 Insights on {prompt}\n\nAs we navigate the evolving landscape of technology, it's crucial to stay informed about developments like this. What's your perspective?\n\n**Post 2:**\n💡 The impact of {prompt} on our industry\n\nThis advancement represents a significant shift in how we approach innovation. How is your organization adapting?\n\n**Post 3:**\n🚀 Future implications of {prompt}\n\nThe intersection of technology and human creativity continues to yield remarkable results. Thoughts on the opportunities ahead?",
                "instagram": f"**Caption 1:**\n✨ {prompt} ✨\n\nWhen technology meets creativity, magic happens! 🎨🤖\n#AI #TechLife #Innovation\n\n**Caption 2:**\n🔥 Mind blown by {prompt} today! 🤯\n\nThe future is literally happening right now ✨\n#FutureTech #Innovation #DigitalLife\n\n**Caption 3:**\n💫 {prompt} vibes 💫\n\nThis is why I love technology - it never stops amazing us! 🚀\n#TechLove #Innovation #Future",
                "youtube": f"**Description 1:**\n🎥 {prompt} - Everything You Need to Know!\n\nIn this video, we explore the fascinating world of this technology. Don't forget to like and subscribe!\n\n**Description 2:**\n🔥 The Future is Here: {prompt} Explained\n\nJoin me as we dive deep into this incredible advancement. Subscribe for more tech content!\n\n**Description 3:**\n⚡ {prompt}: Game Changer or Hype?\n\nLet's analyze this technology together. Hit that notification bell for updates!",
                "tiktok": f"**Caption 1:**\n🔥 {prompt} is trending! ✨ Mind = blown 🤯 #AI #Tech #Viral\n\n**Caption 2:**\nPOV: You just discovered {prompt} 🚀 This changes everything! #TechTok #Innovation\n\n**Caption 3:**\nWait until you see this! {prompt} is insane 🤯 #FYP #Technology #MindBlown",
                "default": f"**Post 1:**\nDiscover the amazing world of {prompt}! This cutting-edge topic represents the future of technology and innovation.\n\n**Post 2:**\nExploring {prompt} - where creativity meets technology. The possibilities are truly endless!\n\n**Post 3:**\nThe fascinating realm of {prompt} continues to evolve. What an exciting time to be alive!"
            }
            content = platform_templates.get(platform.lower(), platform_templates["default"])
    
    # Store in database
    if db:
        content_record = ContentRecord(prompt=prompt, platform=platform, content=content)
        db.add(content_record)
        db.commit()
        db.refresh(content_record)
    
    # Final validation - ensure content has multiple posts
    post_count = max(
        content.count("**Post"),
        content.count("**Tweet"), 
        content.count("**Caption"),
        content.count("**Description")
    )
    
    if post_count < 3:
        print(f"Warning: Only {post_count} posts detected in final content for {platform}")
        print(f"Content length: {len(content)}")
        print(f"Content preview: {content[:200]}...")
    
    return content
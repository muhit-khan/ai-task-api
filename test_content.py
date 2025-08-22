#!/usr/bin/env python3
"""
Test script to verify content generation is working correctly
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.content_service import generate_content

async def test_content_generation():
    """Test content generation for different platforms"""
    
    test_prompt = "I am graduated recently"
    platforms = ["facebook", "twitter", "linkedin", "instagram"]
    
    print("Testing Content Generation Service")
    print("=" * 50)
    
    for platform in platforms:
        print(f"\n🔍 Testing {platform.upper()} content generation...")
        print("-" * 30)
        
        try:
            content = generate_content(test_prompt, platform, db=None)
            print(f"✅ Generated content length: {len(content)} characters")
            print(f"📝 Content preview:\n{content[:200]}...")
            
            # Check for multiple posts
            post_markers = ["**Post 1:**", "**Tweet 1:**", "**Caption 1:**", "**Description 1:**"]
            has_multiple = any(marker in content for marker in post_markers)
            print(f"🔢 Contains multiple posts: {'✅ Yes' if has_multiple else '❌ No'}")
            
            # Count posts
            post_count = max(
                content.count("**Post"),
                content.count("**Tweet"),
                content.count("**Caption"),
                content.count("**Description")
            )
            print(f"📊 Number of posts detected: {post_count}")
            
            if post_count < 3:
                print("❌ WARNING: Less than 3 posts generated!")
                print(f"Full content:\n{content}")
            
        except Exception as e:
            print(f"❌ Error generating content: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_content_generation())
"""
Interactive Avatar Server
FastAPI server for Tavus CVI real-time avatar conversations
"""

import os
import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Interactive Avatar",
    description="Real-time AI avatar conversation platform",
    version="1.0.0"
)


@app.get("/")
async def get():
    """Serve the main HTML page"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/create-conversation")
async def create_conversation():
    """
    Create a new Tavus conversation session
    
    Returns:
        JSON with conversation_url and conversation_id on success
        JSON with error message on failure
    """
    try:
        # Get API key from environment
        api_key = os.getenv("TAVUS_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "TAVUS_API_KEY not configured in .env file"
            }
        
        # Create HTTP session
        async with aiohttp.ClientSession() as session:
            url = "https://tavusapi.com/v2/conversations"
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            # Build conversation payload
            payload = {
                "replica_id": os.getenv("TAVUS_REPLICA_ID", "r18d46c93e"),
                "conversation_name": f"Interactive Demo {asyncio.get_event_loop().time()}",
                "conversational_context": "You are Ajay's AI assistant for product demos. Keep responses short (1-2 sentences). Be enthusiastic and helpful!"
            }
            
            # Add persona_id if configured
            persona_id = os.getenv("TAVUS_PERSONA_ID")
            if persona_id:
                payload["persona_id"] = persona_id
            
            logger.info("🎬 Creating Tavus conversation...")
            
            # Make API request
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    conversation_url = result.get("conversation_url")
                    conversation_id = result.get("conversation_id")
                    
                    logger.info(f"✅ Conversation created: {conversation_id}")
                    logger.info(f"🔗 URL: {conversation_url}")
                    
                    return {
                        "success": True,
                        "conversation_url": conversation_url,
                        "conversation_id": conversation_id
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Error {response.status}: {error_text}")
                    return {
                        "success": False,
                        "error": error_text
                    }
                    
    except Exception as e:
        logger.error(f"❌ Error creating conversation: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Interactive Avatar"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Interactive Avatar Server...")
    logger.info("📍 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

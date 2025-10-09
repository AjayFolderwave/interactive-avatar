import os
import asyncio
import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

app = FastAPI()

@app.get("/")
async def get():
    with open("index_tavus.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/create-conversation")
async def create_conversation():
    """Create a new Tavus conversation and return the Daily room URL"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://tavusapi.com/v2/conversations"
            headers = {
                "x-api-key": os.getenv("TAVUS_API_KEY"),
                "Content-Type": "application/json"
            }
            
            payload = {
                "replica_id": os.getenv("TAVUS_REPLICA_ID"),
                "persona_id": os.getenv("TAVUS_PERSONA_ID"),
                "conversation_name": f"Interactive Demo {asyncio.get_event_loop().time()}",
                "conversational_context": "You are Ajay's AI assistant for product demos. Keep responses short (1-2 sentences). Be enthusiastic and helpful!"
            }
            
            logger.info("🎬 Creating Tavus conversation...")
            
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
                    logger.error(f"Error {response.status}: {error_text}")
                    return {"success": False, "error": error_text}
                    
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
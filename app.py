import os
import asyncio
import wave
from datetime import datetime
from dotenv import load_dotenv
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_response import (
    LLMAssistantResponseAggregator,
    LLMUserResponseAggregator,
)
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.whisper.stt import WhisperSTTService
from pipecat.services.anthropic.llm import AnthropicLLMService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams
from pipecat.frames.frames import LLMMessagesFrame, AudioRawFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from loguru import logger

load_dotenv()

class AudioSaver(FrameProcessor):
    """Save audio frames to WAV file"""
    def __init__(self):
        super().__init__()
        self.audio_frames = []
        self.filename = f"output_{datetime.now().strftime('%H%M%S')}.wav"
        logger.info(f"💾 Will save audio to: {self.filename}")
        
    async def process_frame(self, frame, direction):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, AudioRawFrame):
            self.audio_frames.append(frame.audio)
            # Auto-save every 10 chunks
            if len(self.audio_frames) % 10 == 0:
                self._save()
        
        await self.push_frame(frame, direction)
    
    def _save(self):
        if not self.audio_frames:
            return
            
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            for audio in self.audio_frames:
                wf.writeframes(audio)
        
        logger.info(f"💾 Saved {len(self.audio_frames)} chunks to {self.filename}")

async def main():
    logger.info("🎤 Initializing...")
    
    transport = LocalAudioTransport(
        params=LocalAudioTransportParams()
    )
    
    logger.info("🎧 Loading Whisper...")
    stt = WhisperSTTService()
    
    logger.info("🗣️ Connecting to Cartesia...")
    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id=os.getenv("CARTESIA_VOICE_ID"),
    )
    
    logger.info("🤖 Connecting to Claude...")
    llm = AnthropicLLMService(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-4-20250514"
    )
    
    messages = [
        {
            "role": "system",
            "content": "You are Ajay's AI assistant. Keep responses very short (1-2 sentences). Be enthusiastic!"
        }
    ]
    
    user_response = LLMUserResponseAggregator(messages)
    assistant_response = LLMAssistantResponseAggregator(messages)
    audio_saver = AudioSaver()
    
    pipeline = Pipeline([
        transport.input(),
        stt,
        user_response,
        llm,
        tts,
        audio_saver,  # Capture audio here
        transport.output(),
        assistant_response,
    ])
    
    task = PipelineTask(pipeline, params=PipelineParams(allow_interruptions=True))
    await task.queue_frames([LLMMessagesFrame(messages)])
    
    runner = PipelineRunner()
    
    logger.info("✅ Everything connected!")
    logger.info("🎙️ SPEAK INTO YOUR MICROPHONE!")
    logger.info("📁 Audio will be saved to WAV files")
    logger.info("Press Ctrl+C to stop\n")
    
    try:
        await runner.run(task)
    except KeyboardInterrupt:
        filename = audio_saver.save_to_file()
        logger.info("\n👋 Goodbye! Check your WAV files!")

if __name__ == "__main__":
    asyncio.run(main())
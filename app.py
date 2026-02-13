# app.py
import os
import pandas as pd
import asyncio
from config import OUTPUT_DIR, MIN_GAP
from Desision.pipeline.orchestrator import PatternPipeline

async def main():
    pipeline = PatternPipeline()
    await pipeline.run()
    
if __name__ == "__main__":
    asyncio.run(main())

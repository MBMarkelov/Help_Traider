# app.py
import os
import pandas as pd
import asyncio
from config import OUTPUT_DIR, MIN_GAP
from Desision.pipeline.orchestrator import PatternPipeline

os.makedirs(OUTPUT_DIR, exist_ok=True)

def suppress_nearby(pattern_indices, min_gap=MIN_GAP):
    if not pattern_indices:
        return []
    pattern_indices = sorted(pattern_indices)
    filtered = [pattern_indices[0]]
    for idx in pattern_indices[1:]:
        if idx - filtered[-1] >= min_gap:
            filtered.append(idx)
    return filtered

async def main():
    pipeline = PatternPipeline()
    await pipeline.run()
    
if __name__ == "__main__":
    asyncio.run(main())

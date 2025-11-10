# ai_processing.py
"""
Step 3: Generative AI Processing
Summarize chunks & extract obligations, rights, risks, penalties, and dates
"""

import os
import time
from pathlib import Path
from openai import OpenAI

# --------- Configure OpenAI API ---------
# Make sure you set your API key before running:
#   setx OPENAI_API_KEY "your_api_key"   (Windows permanent)
#   $env:OPENAI_API_KEY="your_api_key"   (PowerShell temporary)
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# --------- Function to process a chunk ---------
def process_chunk(chunk: str) -> str:
    """
    Sends a chunk of text to GPT and returns the simplified output.
    """
    prompt = f"""
    You are a legal document simplifier. Read the following text and:
    1. Summarize it in plain, simple English.
    2. List any obligations, rights, risks, penalties, and critical dates clearly.

    Text:
    {chunk}
    """

    response = client.chat.completions.create(
        model="phi",  # or "gpt-4o"
        messages=[
            {"role": "system", "content": "You simplify legal documents into clear summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


# --------- Main Program ---------
if __name__ == "__main__":
    chunks_dir = Path("chunks")
    output_dir = Path("ai_summaries")
    output_dir.mkdir(exist_ok=True)

    if not chunks_dir.exists():
        print("⚠️ No 'chunks/' folder found. Run preprocessing first.")
        exit()

    chunk_files = sorted(chunks_dir.glob("chunk_*.txt"))
    print(f"Found {len(chunk_files)} chunks. Processing...")

    for i, chunk_file in enumerate(chunk_files, start=1):
        text = chunk_file.read_text(encoding="utf-8")

        # Retry mechanism for stability
        for attempt in range(3):
            try:
                simplified = process_chunk(text)
                (output_dir / f"simplified_{i}.txt").write_text(simplified, encoding="utf-8")
                print(f"✅ Processed chunk {i}/{len(chunk_files)}")
                break
            except Exception as e:
                print(f"❌ Error processing chunk {i}, attempt {attempt+1}: {e}")
                time.sleep(3)
        else:
            print(f"⚠️ Failed to process chunk {i} after 3 attempts.")

    print(f"\n🎉 Summaries saved in 'ai_summaries/' folder")                                                     
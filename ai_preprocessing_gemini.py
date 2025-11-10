# ai_processing_gemini.py
"""
Step 3: Generative AI Processing using Gemini
Summarize chunks & extract obligations, rights, risks, penalties, and dates
"""

import os
import time
from pathlib import Path
import google.generativeai as genai

# --------- Configure Gemini API ---------
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ GOOGLE_API_KEY not found. Set it before running the script.")
genai.configure(api_key=api_key)

# --------- Model selection ---------
model = genai.GenerativeModel("models/gemini-2.5-pro")

# --------- Function to process a chunk ---------
def process_chunk(chunk: str) -> str:
    """
    Sends a chunk of text to Gemini and returns the simplified output.
    """
    prompt = f"""
    You are a legal document simplifier. Read the following text and:
    1. Summarize it in plain, simple English.
    2. List any obligations, rights, risks, penalties, and critical dates clearly.

    Text:
    {chunk}
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# --------- Main Program ---------
if __name__ == "__main__":
    chunks_dir = Path("chunks")
    output_dir = Path("gemini_ai_summaries")
    output_dir.mkdir(exist_ok=True)

    if not chunks_dir.exists():
        print("⚠️ No 'chunks/' folder found. Run preprocessing first.")
        exit()

    chunk_files = sorted(chunks_dir.glob("chunk_*.txt"))
    print(f"Found {len(chunk_files)} chunks. Processing...")

    for i, chunk_file in enumerate(chunk_files, start=1):
        text = chunk_file.read_text(encoding="utf-8")

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

    print("\n🎉 Summaries saved in 'gemini_ai_summaries/' folder")

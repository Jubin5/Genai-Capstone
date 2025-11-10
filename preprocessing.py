# preprocessing.py
"""
Step 2: Preprocessing
Clean and chunk extracted text
"""

import re
from pathlib import Path

# --------- Function to clean text ---------
def clean_text(text: str) -> str:
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters (keep only basic text & punctuation)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


# --------- Function to split text into chunks ---------
def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list:
    """
    Splits text into chunks of `chunk_size` characters with `overlap` for context.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


# --------- Main Program ---------
if __name__ == "__main__":
    input_file = Path("GovReport_extracted.txt")

    if input_file.exists():
        raw_text = input_file.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        # Split into chunks
        chunks = split_text(cleaned_text, chunk_size=1200, overlap=200)

        print(f"✅ Cleaned text length: {len(cleaned_text)} chars")
        print(f"✅ Split into {len(chunks)} chunks")

        print("\n--- First Chunk Preview (First 100000 chars) ---\n")
        print(chunks[0][:500])

        # Save chunks into separate files
        output_dir = Path("chunks")
        output_dir.mkdir(exist_ok=True)
        for i, chunk in enumerate(chunks, start=1):
            (output_dir / f"chunk_{i}.txt").write_text(chunk, encoding="utf-8")

        print(f"\n✅ {len(chunks)} chunks saved in 'chunks/' folder")
    else:
        print(f"{input_file} not found!")

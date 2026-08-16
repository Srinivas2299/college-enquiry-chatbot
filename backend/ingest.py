"""
ingest.py
---------
Standalone script to bulk-load every PDF in ./data into ChromaDB.
Run this whenever you add new documents.

Usage:
    python ingest.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

from chroma_utils import add_pdf

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

if __name__ == "__main__":
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"No PDFs found in {DATA_DIR}. Add some real college documents and re-run.")
        exit()

    succeeded = []
    skipped = []
    failed = []

    for filename in pdf_files:
        path = os.path.join(DATA_DIR, filename)
        try:
            num_chunks = add_pdf(path, source_name=filename)
            if num_chunks == 0:
                print(f"SKIPPED (no extractable text): {filename}")
                skipped.append(filename)
            else:
                print(f"Ingested {filename}: {num_chunks} chunks added.")
                succeeded.append(filename)
        except Exception as e:
            print(f"FAILED: {filename} -> {e}")
            failed.append(filename)

    print("\n--- Summary ---")
    print(f"Succeeded: {len(succeeded)}")
    print(f"Skipped (no text): {len(skipped)} -> {skipped}")
    print(f"Failed (errors): {len(failed)} -> {failed}")
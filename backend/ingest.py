"""
ingest.py
---------
Bulk-loads every PDF and TXT file in ./data into ChromaDB.
Run this whenever you add new documents.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from chroma_utils import add_document

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

if __name__ == "__main__":
    files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith((".pdf", ".txt"))]

    if not files:
        print(f"No PDF or TXT files found in {DATA_DIR}.")
        exit()

    succeeded, skipped, failed = [], [], []

    for filename in files:
        path = os.path.join(DATA_DIR, filename)
        try:
            num_chunks = add_document(path, source_name=filename)
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
    print(f"Skipped: {len(skipped)} -> {skipped}")
    print(f"Failed: {len(failed)} -> {failed}")
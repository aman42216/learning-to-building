import json
from pathlib import Path

from chunking import process_pdf_directory
from faq_chunking import process_faq_records


PDF_DIR = Path("Day-03/data/raw")
OUTPUT_FILE = Path("Day-07/data/processed/chunks.json")


def main():
    # Process official PDF documents
    pdf_chunks = process_pdf_directory(PDF_DIR)

    # Process structured FAQ records
    faq_chunks = process_faq_records()

    # Combine both datasets
    all_chunks = pdf_chunks + faq_chunks

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_chunks, file, indent=4, ensure_ascii=False)

    print("PDF chunks:", len(pdf_chunks))
    print("FAQ chunks:", len(faq_chunks))
    print("Total chunks saved:", len(all_chunks))
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
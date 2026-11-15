
from pathlib import Path
from pypdf import PdfReader
import hashlib

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def file_hash(pdf_path):
    sha256 = hashlib.sha256()

    with open(pdf_path, "rb") as file:
        for block in iter(lambda: file.read(65536), b""):
            sha256.update(block)

    return sha256.hexdigest()


def process_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))

    document_title = pdf_path.stem
    all_chunks = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        page_chunks = chunk_text(text)

        for chunk_index, content in enumerate(page_chunks):
            chunk_id = hashlib.sha256(
                f"{pdf_path.name}:{page_number}:{chunk_index}:{content}".encode("utf-8")
            ).hexdigest()

            all_chunks.append({
                "id": chunk_id,
                "text": content,
                "metadata": {
                    "source": pdf_path.name,
                    "page": page_number,
                    "title": document_title,
                    "chunk_index": chunk_index
                }
            })

    return all_chunks


def process_pdf_directory(directory):
    directory = Path(directory)
    results = []
    seen_hashes = set()
    skipped_files = []

    for pdf_path in sorted(directory.glob("*.pdf")):
        pdf_hash = file_hash(pdf_path)

        if pdf_hash in seen_hashes:
            skipped_files.append(pdf_path.name)
            continue

        seen_hashes.add(pdf_hash)
        results.extend(process_pdf(pdf_path))

    print("Skipped duplicate PDFs:", skipped_files)

    return results


from pathlib import Path
from pypdf import PdfReader
import hashlib

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

AUTHORITY = "Ministry of Labour and Employment"

DOCUMENT_METADATA = {
    "de4758d5bfeffc456d7de97a801891b0.pdf": {
        "title": "FAQs on Labour Codes",
        "document_type": "faq",
        "published_date": "2025-12-30",
        "version": "2025-12",
        "legal_status": "official_faq_guidance",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/01/de4758d5bfeffc456d7de97a801891b0.pdf"
    },

    "labour_faqs_2025.pdf": {
        "title": "FAQs on Labour Codes",
        "document_type": "faq",
        "published_date": "2025-12-30",
        "version": "2025-12",
        "legal_status": "official_faq_guidance",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/01/de4758d5bfeffc456d7de97a801891b0.pdf"
    },

    "additional_faqs_2026.pdf": {
        "title": "Additional FAQs on Labour Codes",
        "document_type": "additional_faq",
        "published_date": "2026-03-16",
        "version": "2026-03",
        "legal_status": "official_faq_guidance",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/03/a4ccf4c6d97c4f1f36a6d83f8c64213d.pdf"
    },

    "social_security_code.pdf": {
        "title": "Code on Social Security",
        "document_type": "code",
        "published_date": "",
        "version": "2020",
        "legal_status": "date_unverified",
        "source_url": ""
    },

    "labour_codes_faqs_2026-10-25.pdf": {
        "title": "Compilation of FAQs on Four Labour Codes and Central Rules",
        "document_type": "consolidated_faq",
        "as_of_date": "2026-10-25",
        "version": "2026-10",
        "jurisdiction": "India",
        "legal_status": "official_faq_guidance",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/11/da640b1558a315e81e22ce5ac12f463f.pdf"
    },

    "code_on_wages_central_rules_2026-05-08.pdf": {
        "title": "Code on Wages (Central) Rules, 2026",
        "document_type": "central_rules",
        "published_date": "2026-05-08",
        "effective_date": "2026-05-08",
        "version": "2026-05",
        "jurisdiction": "Central",
        "notification_number": "G.S.R. 343(E)",
        "legal_status": "notified_rules",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/05/6eb0c35ba63b776487a025e5123b6b12.pdf"
    },

    "industrial_relations_central_rules_2026-05-08.pdf": {
        "title": "Industrial Relations (Central) Rules, 2026",
        "document_type": "central_rules",
        "published_date": "2026-05-08",
        "effective_date": "2026-05-08",
        "version": "2026-05",
        "jurisdiction": "Central",
        "notification_number": "G.S.R. 342(E)",
        "legal_status": "notified_rules",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/05/f05a2c220dcdec0ea9c55e84d9ff791f.pdf"
    },

    "social_security_central_rules_2026-05-08.pdf": {
        "title": "Social Security (Central) Rules, 2026",
        "document_type": "central_rules",
        "published_date": "2026-05-08",
        "effective_date": "2026-05-08",
        "version": "2026-05",
        "jurisdiction": "Central",
        "notification_number": "G.S.R. 344(E)",
        "legal_status": "notified_rules",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/05/49aa9b62c2125499c37399b90e969d67.pdf"
    },

    "oshwc_central_rules_2026-05-08.pdf": {
        "title": "Occupational Safety, Health and Working Conditions (Central) Rules, 2026",
        "document_type": "central_rules",
        "published_date": "2026-05-08",
        "effective_date": "2026-05-08",
        "version": "2026-05",
        "jurisdiction": "Central",
        "notification_number": "G.S.R. 345(E)",
        "legal_status": "notified_rules",
        "source_url": "https://www.labour.gov.in/static/uploads/2026/05/ee246f790cad0b8e99c3828f34fa09a6.pdf"
    }
}

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

    document_metadata = DOCUMENT_METADATA.get(
        pdf_path.name,
        {
            "title": pdf_path.stem,
            "document_type": "unknown",
            "published_date": "",
            "version": "",
            "legal_status": "unverified",
            "source_url": ""
        }
    )

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
                    **document_metadata,
                    "authority": AUTHORITY,
                    "source": pdf_path.name,
                    "page": page_number,
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
    print("Total PDF chunks:", len(results))

    return results

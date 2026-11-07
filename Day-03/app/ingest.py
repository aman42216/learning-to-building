
import json
import re
from pathlib import Path
import pdfplumber

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "data" / "records.json"


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\uf0b7", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_records(filename, faq_date, code_name, source_url, limit):
    records = []
    file_path = RAW_FOLDER / filename

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                tables = page.extract_tables()

                for table in tables:
                    for row in table:

                        try:
                            if not row or len(row) < 3:
                                continue

                            serial = clean_text(row[0])

                            # Skip headings and non-numbered rows
                            if not re.fullmatch(r"\d+\.?", serial):
                                continue

                            question = clean_text(row[1])
                            answer = clean_text(row[2])

                            if not question or not answer:
                                continue

                            records.append({
                                "topic": "General Labour",
                                "code_name": code_name,
                                "question": question,
                                "official_answer": answer,
                                "faq_date": faq_date,
                                "source_url": source_url
                            })

                            if len(records) >= limit:
                                return records

                        except (ValueError, TypeError, IndexError) as error:
                            print("Bad row skipped:", error)

    except Exception as error:
        print(f"Error reading {filename}: {error}")

    return records


def main():

    first_records = extract_records(
        "labour_faqs_2025.pdf",
        "30-12-2025",
        "All Four Labour Codes",
        "https://labour.gov.in/static/uploads/2026/01/de4758d5bfeffc456d7de97a801891b0.pdf",
        17
    )

    additional_records = extract_records(
        "additional_faqs_2026.pdf",
        "16-03-2026",
        "Additional FAQs on Labour Codes",
        "https://www.labour.gov.in/static/uploads/2026/03/a4ccf4c6d97c4f1f36a6d83f8c64213d.pdf",
        3
    )

    all_records = first_records + additional_records

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_records, file, indent=4, ensure_ascii=False)

    print("\n========== EXTRACTION REPORT ==========")
    print("2025 FAQs:", len(first_records), "/ 17")
    print("2026 FAQs:", len(additional_records), "/ 3")
    print("Total Records:", len(all_records))

    if len(all_records) == 20:
        print("SUCCESS: All 20 records extracted!")
    else:
        print("WARNING: Some required records could not be extracted.")

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

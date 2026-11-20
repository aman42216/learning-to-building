
import json
from pathlib import Path

RECORDS_FILE = (
    Path(__file__).resolve().parents[1]
    / "Day-03"
    / "data"
    / "records.json"
)


def load_records():
    with open(RECORDS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def test_records_file_exists():
    assert RECORDS_FILE.exists()


def test_records_is_not_empty():
    records = load_records()
    assert len(records) > 0


def test_records_have_required_fields():
    records = load_records()

    required_fields = {
        "topic",
        "code_name",
        "question",
        "official_answer",
        "faq_date",
        "source_url",
    }

    for record in records:
        assert required_fields.issubset(record.keys())


def test_records_questions_are_not_empty():
    records = load_records()

    for record in records:
        assert record["question"].strip()


def test_records_answers_are_not_empty():
    records = load_records()

    for record in records:
        assert record["official_answer"].strip()


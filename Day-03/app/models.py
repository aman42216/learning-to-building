
from dataclasses import dataclass, asdict


@dataclass
class Record:
    topic: str
    code_name: str
    question: str
    official_answer: str
    faq_date: str
    source_url: str

    def to_dict(self):
        return asdict(self)


# Testing
if __name__ == "__main__":

    record = Record(
        topic="Gratuity",
        code_name="Code on Social Security, 2020",
        question="What is gratuity?",
        official_answer="Gratuity is a benefit payable to eligible employees.",
        faq_date="30-12-2025",
        source_url="Official Labour Ministry PDF"
    )

    print("Record Created Successfully!")
    print(record.to_dict())

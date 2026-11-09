
import pandas as pd
import json
from pathlib import Path

# Load JSON data
BASE_DIR = Path(__file__).resolve().parents[2]
FILE_PATH = BASE_DIR / "Day-03" / "data" / "records.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert JSON into DataFrame
df = pd.DataFrame(data)

print("===== SHRMIKSATHI DATA ANALYSIS =====")

# Fact 1: Total records
print("\n1. Total Records:", len(df))

# Fact 2: FAQs by date
print("\n2. FAQs by Date:")
print(df["faq_date"].value_counts())

# Fact 3: FAQs by Labour Code
print("\n3. FAQs by Labour Code:")
print(df["code_name"].value_counts())

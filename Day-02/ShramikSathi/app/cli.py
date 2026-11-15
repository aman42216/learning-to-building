
from .records import load_records, search, count_by, get_by_id


def display_record(record):
    print("\n" + "=" * 60)
    print("SHRAMIKSATHI - FAQ ANSWER")
    print("=" * 60)
    print("ID:", record.get("id"))
    print("Topic:", record.get("topic"))
    print("Question:", record.get("question"))
    print("\nOfficial Answer:")
    print(record.get("official_answer", "Answer unavailable"))
    print("Labour Code:", record.get("code_name"))
    print("Old Law:", record.get("old_law"))
    print("FAQ Date:", record.get("faq_date"))
    print("Source:", record.get("source_url"))
    print("=" * 60)


def run_cli():
    records = load_records()

    while True:
        print("\n===== WELCOME TO SHRAMIKSATHI =====")
        print("1. Ask a Labour Law Question")
        print("2. View All FAQs")
        print("3. Count FAQs by Topic")
        print("4. Find FAQ by ID")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            query = input("Enter your question: ")
            results = search(records, query)

            if results:
                display_record(results[0])
            else:
                print("No matching FAQ found.")

        elif choice == "2":
            for record in records:
                print(record.get("id"), "-", record.get("question"))

        elif choice == "3":
            print("\nFAQ Count by Topic:")
            for topic, total in count_by(records, "topic").items():
                print(topic, ":", total)

        elif choice == "4":
            try:
                record_id = int(input("Enter FAQ ID: "))
                record = get_by_id(records, record_id)

                if record:
                    display_record(record)
                else:
                    print("FAQ ID not found.")

            except ValueError:
                print("Please enter a valid numeric ID.")

        elif choice == "5":
            print("Thank you for using ShramikSathi!")
            break

        else:
            print("Invalid choice. Select between 1 and 5.")

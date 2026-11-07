
import json
import os
import re

# -----------------------------------------
# SHRMIKSATHI - LABOUR RIGHTS ASSISTANT
# -----------------------------------------

DATA_FILE = os.path.join("data", "faqs.json")
GRATUITY_LIMIT = 2000000


# Load FAQ dataset
def load_faqs():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            faqs = data.get("faqs", data.get("data", []))
        else:
            faqs = data

        if not isinstance(faqs, list):
            print("Invalid FAQ data format.")
            return []

        print(f"\nSuccessfully loaded {len(faqs)} FAQs.")
        return faqs

    except FileNotFoundError:
        print("\nError: data/faqs.json file not found!")
        return []
    except json.JSONDecodeError:
        print("\nError: Invalid JSON format in FAQ file!")
        return []


# Display a single FAQ
def display_faq(faq):
    print("\n" + "=" * 65)
    print("              SHRMIKSATHI - FAQ ANSWER")
    print("=" * 65)

    print("\nTopic:",
          faq.get("topic", "Not available"))

    print("Question:",
          faq.get("question", "Not available"))

    print("\nOfficial Answer:")
    answer = (
        faq.get("official_answer")
        or faq.get("answer")
        or "No official answer is available in the dataset."
    )
    print(answer)

    print("\nLabour Code:",
          faq.get("code_name", "Not specified"))

    print("Old Law:",
          faq.get("old_law", "Refer to the applicable previous law"))

    print("FAQ Date:",
          faq.get("faq_date", "Not available"))

    print("Source URL:",
          faq.get("source_url", "Not available"))

    print("=" * 65)


# Search FAQ using keyword matching
def search_faq(faqs):
    print("\n--- ASK YOUR LABOUR LAW QUESTION ---")
    question = input("Enter your question: ").strip().lower()

    if not question:
        print("Please enter a valid question.")
        return

    stop_words = {
        "what", "is", "are", "the", "a", "an", "of", "to",
        "in", "for", "how", "can", "i", "my", "do", "does",
        "tell", "me", "about", "please", "under", "and"
    }

    query_words = set(re.findall(r"[a-z0-9]+", question))
    query_words -= stop_words

    best_faq = None
    best_score = 0

    for faq in faqs:
        searchable_text = " ".join([
            str(faq.get("topic", "")),
            str(faq.get("question", "")),
            str(faq.get("official_answer", "")),
            str(faq.get("answer", "")),
            str(faq.get("code_name", ""))
        ]).lower()

        faq_words = set(re.findall(r"[a-z0-9]+", searchable_text))
        score = len(query_words.intersection(faq_words))

        if score > best_score:
            best_score = score
            best_faq = faq

    if best_faq and best_score > 0:
        display_faq(best_faq)
        print("\nNote: This answer is retrieved from the FAQ dataset.")
    else:
        print("\nSorry! No matching FAQ was found.")
        print("Try using keywords like:")
        print("Gratuity, Wages, Leave, Salary, Contract Labour,")
        print("Social Security or Minimum Wages.")


# Display all FAQs
def view_all_faqs(faqs):
    print("\n========== AVAILABLE LABOUR FAQs ==========")

    if not faqs:
        print("No FAQs available.")
        return

    for index, faq in enumerate(faqs, start=1):
        print(f"\n{index}. {faq.get('question', 'Question unavailable')}")
        print(f"   Topic: {faq.get('topic', 'Not specified')}")

    choice = input("\nEnter FAQ number to view details (0 to go back): ")

    if not choice.isdigit():
        print("Invalid input.")
        return

    number = int(choice)

    if number == 0:
        return
    elif 1 <= number <= len(faqs):
        display_faq(faqs[number - 1])
    else:
        print("Invalid FAQ number.")


# Gratuity calculator
def gratuity_calculator():
    print("\n========== GRATUITY CALCULATOR ==========")

    try:
        basic = float(input("Enter monthly basic wages (₹): "))
        allowances = float(input("Enter monthly excluded allowances (₹): "))
        years = int(input("Enter completed years of service: "))

        if basic < 0 or allowances < 0 or years <= 0:
            print("Please enter valid positive values.")
            return

        total_remuneration = basic + allowances

        # Illustrative 50% wage rule calculation
        allowed_excluded_amount = total_remuneration * 0.50
        excess_allowances = max(
            0, allowances - allowed_excluded_amount
        )

        adjusted_wages = basic + excess_allowances

        # Gratuity formula
        gratuity = (15 / 26) * adjusted_wages * years

        # Maximum statutory ceiling used in this calculator
        final_amount = min(gratuity, GRATUITY_LIMIT)

        print("\n========== CALCULATION RESULT ==========")
        print(f"Basic Monthly Wages: ₹{basic:,.2f}")
        print(f"Monthly Allowances: ₹{allowances:,.2f}")
        print(f"Total Remuneration: ₹{total_remuneration:,.2f}")
        print(f"Adjusted Monthly Wages: ₹{adjusted_wages:,.2f}")
        print(f"Completed Service: {years} years")

        print("\nEstimated Gratuity: ₹{:,.2f}".format(final_amount))

        if gratuity > GRATUITY_LIMIT:
            print("Note: The calculated amount exceeds the ₹20 lakh cap.")

        print("\nDisclaimer:")
        print("This is an illustrative estimate, not a final legal")
        print("determination. Actual wage components, eligibility,")
        print("service rules and applicable law must be verified.")

        print("=" * 65)

    except ValueError:
        print("Invalid input! Please enter numeric values.")


# Main menu
def main():
    faqs = load_faqs()

    while True:
        print("\n")
        print("=" * 65)
        print("             WELCOME TO SHRMIKSATHI")
        print("       LABOUR RIGHTS INFORMATION ASSISTANT")
        print("=" * 65)

        print("\n1. Ask a Labour Law Question")
        print("2. Gratuity Calculator")
        print("3. View All Labour FAQs")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            search_faq(faqs)

        elif choice == "2":
            gratuity_calculator()

        elif choice == "3":
            view_all_faqs(faqs)

        elif choice == "4":
            print("\nThank you for using ShramikSathi!")
            print("Know your rights. Stay informed.")
            break

        else:
            print("\nInvalid choice! Please select between 1 and 4.")


# Program execution
if __name__ == "__main__":
    main()

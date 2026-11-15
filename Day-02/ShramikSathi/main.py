
from app.cli import run_cli
from app.records import load_records


def gratuity_calculator():
    print("\n===== GRATUITY CALCULATOR =====")

    try:
        basic = float(input("Enter monthly basic wages: "))
        allowances = float(input("Enter monthly excluded allowances: "))
        years = int(input("Enter completed years of service: "))

        if basic < 0 or allowances < 0 or years <= 0:
            print("Please enter valid values.")
            return

        total = basic + allowances
        allowed_excluded = total * 0.50
        excess = max(0, allowances - allowed_excluded)
        adjusted_wages = basic + excess

        gratuity = (15 / 26) * adjusted_wages * years
        final_amount = min(gratuity, 2000000)

        print(f"Estimated Gratuity: Rs. {final_amount:,.2f}")
        print("Note: This is an illustrative estimate.")

    except ValueError:
        print("Please enter valid numeric values.")


def main():
    while True:
        print("\n===== SHRMIKSATHI =====")
        print("1. Labour FAQ Assistant")
        print("2. Gratuity Calculator")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            run_cli()

        elif choice == "2":
            gratuity_calculator()

        elif choice == "3":
            print("Thank you for using ShramikSathi!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

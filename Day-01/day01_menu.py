
# Day 01 - Menu Driven Program

while True:

    print("\n===== SHRMIKSATHI MENU =====")
    print("1. About ShramikSathi")
    print("2. Sample Questions")
    print("3. Check Labour Rule")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nShramikSathi is a Labour Rights Assistant.")
        print("It helps workers understand labour laws.")

    elif choice == "2":
        print("\nSample Questions:")
        print("1. What is minimum wage?")
        print("2. What is gratuity?")
        print("3. What are Labour Codes?")

    elif choice == "3":
        salary = float(input("Enter monthly salary: "))

        if salary < 0:
            print("Please enter a valid salary.")
        elif salary < 15000:
            print("Salary is below Rs. 15,000.")
        else:
            print("Salary is Rs. 15,000 or above.")

        print("This is only a sample rule check.")

    elif choice == "0":
        print("Thank you for using ShramikSathi!")
        break

    else:
        print("Invalid choice! Try again.")

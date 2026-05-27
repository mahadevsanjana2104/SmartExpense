import json

FILE_NAME = "data.json"


# EXPENSE CLASS
class Expense:

    def __init__(self, category, amount):

        self.category = category
        self.amount = amount

    def display(self):

        print(f"{self.category} → ₹{self.amount}")


# LOAD DATA
def load_data():

    try:

        with open(FILE_NAME, "r") as file:

            data = json.load(file)

            salary = data["salary"]

            expenses = []

            for item in data["expenses"]:

                expense = Expense(
                    item["category"],
                    item["amount"]
                )

                expenses.append(expense)

    except:

        salary = float(input("Enter your monthly salary: ₹"))
        expenses = []

    return salary, expenses


# SAVE DATA
def save_data(salary, expenses):

    data = {
        "salary": salary,
        "expenses": []
    }

    for expense in expenses:

        expense_data = {
            "category": expense.category,
            "amount": expense.amount
        }

        data["expenses"].append(expense_data)

    with open(FILE_NAME, "w") as file:

        json.dump(data, file)

    print("Data saved successfully!")


# ADD EXPENSE
def add_expense(expenses):

    category = input("Enter expense category: ")
    amount = float(input("Enter expense amount: ₹"))

    expense = Expense(category, amount)

    expenses.append(expense)

    print(f"₹{amount} added for {category}")


# VIEW EXPENSES
def view_expenses(expenses):

    if len(expenses) == 0:

        print("No expenses found.")
        return

    print("\n----- Your Expenses -----")

    for expense in expenses:

        expense.display()


# VIEW SUMMARY
def view_summary(salary, expenses):

    total_expenses = 0

    for expense in expenses:

        total_expenses += expense.amount

    remaining_money = salary - total_expenses

    print("\n----- Monthly Summary -----")

    print(f"Salary: ₹{salary}")
    print(f"Total Expenses: ₹{total_expenses}")
    print(f"Remaining Money: ₹{remaining_money}")

    if remaining_money < 0:

        print("Warning: You are overspending!")

    elif remaining_money > 20000:

        print("Excellent savings this month!")

    else:

        print("Good job managing your expenses.")


# DELETE EXPENSE
def delete_expense(expenses):

    delete_category = input(
        "Enter the category of the expense to delete: "
    )

    updated_expenses = []

    for expense in expenses:

        if expense.category != delete_category:

            updated_expenses.append(expense)

    expenses.clear()
    expenses.extend(updated_expenses)

    print(f"Expenses in category '{delete_category}' deleted.")


# SHOW MENU
def show_menu():

    print("\n===== Expense Tracker =====")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Summary")
    print("4. Save Data")
    print("5. Delete an Expense")
    print("6. Exit")


# MAIN PROGRAM
salary, expenses = load_data()

while True:

    show_menu()

    choice = input("Choose an option: ")

    if choice == "1":

        add_expense(expenses)

    elif choice == "2":

        view_expenses(expenses)

    elif choice == "3":

        view_summary(salary, expenses)

    elif choice == "4":

        save_data(salary, expenses)

    elif choice == "5":

        delete_expense(expenses)

    elif choice == "6":

        print("Exiting Expense Tracker...")
        break

    else:

        print("Invalid option. Please try again.")
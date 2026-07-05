from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ======================================
# GLOBAL VARIABLES
# ======================================

salary = 0
expenses = []
goal_name = ""
goal_amount = 0


# ======================================
# HELPER FUNCTIONS
# ======================================

def get_category(category_name):
    """
    Converts user input into one of the
    standard categories.
    """

    name = category_name.strip().lower()

    if any(word in name for word in [
        "food", "foods", "grocery", "groceries",
        "restaurant", "zomato", "swiggy"
    ]):
        return "Food"

    elif any(word in name for word in [
        "rent", "house", "flat"
    ]):
        return "Rent"

    elif any(word in name for word in [
        "transport", "travel", "uber",
        "ola", "rapido", "petrol",
        "fuel", "bus", "metro"
    ]):
        return "Transport"

    elif any(word in name for word in [
        "shopping", "shop", "amazon",
        "flipkart", "myntra",
        "ajio", "clothes"
    ]):
        return "Shopping"

    elif any(word in name for word in [
        "movie", "movies",
        "netflix", "spotify",
        "prime", "entertainment"
    ]):
        return "Entertainment"

    elif any(word in name for word in [
        "utility", "utilities",
        "electricity", "water",
        "gas", "wifi",
        "internet", "bill", "bills"
    ]):
        return "Utilities"

    elif any(word in name for word in [
        "investment", "investments",
        "sip", "mutual",
        "stock", "stocks",
        "fd", "ppf",
        "zerodha", "groww"
    ]):
        return "Investment"

    return "Other"


# ======================================
# LANDING PAGE
# ======================================

@app.route("/")
def landing():

    return render_template("landing.html")


# ======================================
# DASHBOARD
# ======================================

@app.route("/dashboard")
def dashboard():

    global salary
    global expenses

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    remaining_balance = salary - total_expenses

    category_budget = {

        "Food": salary * 0.15,
        "Transport": salary * 0.10,
        "Rent": salary * 0.30,
        "Shopping": salary * 0.10,
        "Entertainment": salary * 0.05,
        "Utilities": salary * 0.10,
        "Investment": salary * 0.20

    }

    category_spending = {

        "Food": 0,
        "Transport": 0,
        "Rent": 0,
        "Shopping": 0,
        "Entertainment": 0,
        "Utilities": 0,
        "Investment": 0

    }

    for expense in expenses:

        category = get_category(
            expense["category"]
        )

        if category in category_spending:

            category_spending[category] += expense["amount"]

    budget_progress = []

    for category in category_budget:

        spent = category_spending[category]

        limit = category_budget[category]

        percentage = 0

        if limit > 0:

            percentage = (spent / limit) * 100

        if percentage < 60:

            status = "Healthy"
            color = "green"

        elif percentage < 90:

            status = "Near Limit"
            color = "yellow"

        else:

            status = "Overspent"
            color = "red"

        budget_progress.append({

            "category": category,
            "spent": spent,
            "limit": limit,
            "percentage": round(percentage, 1),
            "status": status,
            "color": color

        })

    return render_template(

        "dashboard.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        budget_progress=budget_progress

    )
# ======================================
# ANALYTICS
# ======================================

@app.route("/analytics")
def analytics():

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    remaining_balance = salary - total_expenses

    spending_percentage = 0

    if salary > 0:
        spending_percentage = (
            total_expenses / salary
        ) * 100

    highest_expense = None

    if expenses:
        highest_expense = max(
            expenses,
            key=lambda x: x["amount"]
        )

    if remaining_balance < 0:
        savings_message = "You are overspending this month."

    elif remaining_balance > salary * 0.30:
        savings_message = "Excellent savings habit!"

    else:
        savings_message = "Your finances are stable."

    return render_template(

        "analytics.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        highest_expense=highest_expense,

        spending_percentage=spending_percentage,

        savings_message=savings_message

    )


# ======================================
# GOALS
# ======================================

@app.route("/goals")
def goals():

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    remaining_balance = salary - total_expenses

    months_needed = None

    if remaining_balance > 0 and goal_amount > 0:

        months_needed = (
            goal_amount /
            remaining_balance
        )

    return render_template(

        "goals.html",

        salary=salary,

        expenses=expenses,

        remaining_balance=remaining_balance,

        goal_name=goal_name,

        goal_amount=goal_amount,

        months_needed=months_needed

    )


# ======================================
# BUDGET PLANNER
# ======================================

@app.route("/budget")
def budget():

    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )

    remaining_balance = salary - total_expenses

    needs_budget = salary * 0.50
    wants_budget = salary * 0.30
    savings_budget = salary * 0.20

    food_budget = salary * 0.15
    rent_budget = salary * 0.30
    entertainment_budget = salary * 0.05
    travel_budget = salary * 0.10
    shopping_budget = salary * 0.10

    food_spending = 0
    rent_spending = 0
    entertainment_spending = 0
    investment_spending = 0

    for expense in expenses:

        category = get_category(
            expense["category"]
        )

        amount = expense["amount"]

        if category == "Food":
            food_spending += amount

        elif category == "Rent":
            rent_spending += amount

        elif category == "Entertainment":
            entertainment_spending += amount

        elif category == "Investment":
            investment_spending += amount

    budget_alerts = []

    if food_spending > food_budget:

        budget_alerts.append(
            "🍔 Food spending is above the recommended limit."
        )

    if rent_spending > rent_budget:

        budget_alerts.append(
            "🏠 Rent is taking a large portion of your salary."
        )

    if investment_spending > 0:

        budget_alerts.append(
            "📈 Great job! You are investing."
        )

    if remaining_balance < salary * 0.10:

        budget_alerts.append(
            "⚠️ Your remaining balance is getting low."
        )

    if not budget_alerts:

        budget_alerts.append(
            "✅ Your budget looks healthy."
        )

    return render_template(

        "budget.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        needs_budget=needs_budget,

        wants_budget=wants_budget,

        savings_budget=savings_budget,

        food_budget=food_budget,

        rent_budget=rent_budget,

        entertainment_budget=entertainment_budget,

        travel_budget=travel_budget,

        shopping_budget=shopping_budget,

        food_spending=food_spending,

        rent_spending=rent_spending,

        entertainment_spending=entertainment_spending,

        investment_spending=investment_spending,

        budget_alerts=budget_alerts

    )
# ======================================
# SAVE SALARY
# ======================================

@app.route("/salary", methods=["POST"])
def save_salary():

    global salary

    try:
        salary = float(request.form["salary"])

        if salary < 0:
            salary = 0

    except:
        salary = 0

    return redirect("/dashboard")


# ======================================
# ADD EXPENSE
# ======================================

@app.route("/add", methods=["POST"])
def add_expense():

    global expenses

    category = request.form["category"].strip()

    try:
        amount = float(request.form["amount"])

        if amount < 0:
            amount = 0

    except:
        amount = 0

    expenses.append({

        "category": category,

        "amount": amount

    })

    return redirect("/dashboard")


# ======================================
# DELETE EXPENSE
# ======================================

@app.route("/delete/<int:index>")
def delete_expense(index):

    if 0 <= index < len(expenses):

        expenses.pop(index)

    return redirect("/dashboard")


# ======================================
# EDIT EXPENSE
# ======================================

@app.route("/edit/<int:index>")
def edit_expense(index):

    if index < 0 or index >= len(expenses):

        return redirect("/dashboard")

    return render_template(

        "edit.html",

        expense=expenses[index],

        index=index

    )


# ======================================
# UPDATE EXPENSE
# ======================================

@app.route("/update/<int:index>", methods=["POST"])
def update_expense(index):

    if index < 0 or index >= len(expenses):

        return redirect("/dashboard")

    category = request.form["category"].strip()

    try:

        amount = float(request.form["amount"])

        if amount < 0:
            amount = 0

    except:

        amount = 0

    expenses[index]["category"] = category
    expenses[index]["amount"] = amount

    return redirect("/dashboard")


# ======================================
# SAVE GOAL
# ======================================

@app.route("/goal", methods=["POST"])
def save_goal():

    global goal_name
    global goal_amount

    goal_name = request.form["goal_name"].strip()

    try:

        goal_amount = float(
            request.form["goal_amount"]
        )

        if goal_amount < 0:
            goal_amount = 0

    except:

        goal_amount = 0

    return redirect("/goals")


# ======================================
# RUN APP
# ======================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# =========================
# GLOBAL VARIABLES
# =========================

salary = 0

expenses = []

goal_name = ""

goal_amount = 0


# =========================
# LANDING PAGE
# =========================

@app.route("/")
def landing():

    return render_template(
        "landing.html"
    )


# =========================
# DASHBOARD PAGE
# =========================

@app.route("/dashboard")
def dashboard():

    global salary
    global expenses

    return render_template(

        "dashboard.html",

        salary=salary,

        expenses=expenses
    )

    # =========================
# BUDGET PLANNER PAGE
# =========================

@app.route("/budget")
def budget():

    global salary
    global expenses

    # =========================
    # 50 / 30 / 20 RULE
    # =========================

    needs_budget = salary * 0.5

    wants_budget = salary * 0.3

    savings_budget = salary * 0.2


    # CATEGORY SUGGESTIONS

    food_budget = needs_budget * 0.3

    rent_budget = needs_budget * 0.5

    transport_budget = needs_budget * 0.2

    entertainment_budget = wants_budget * 0.4

    shopping_budget = wants_budget * 0.3

    travel_budget = wants_budget * 0.3


    # =========================
    # ACTUAL CATEGORY SPENDING
    # =========================

    food_spending = 0

    rent_spending = 0

    entertainment_spending = 0

    investment_spending = 0


    for expense in expenses:

        category = (

            expense["category"].lower()
        )

        amount = expense["amount"]


        if category == "food":

            food_spending += amount


        elif category == "rent":

            rent_spending += amount


        elif category == "entertainment":

            entertainment_spending += amount


        elif category in [

            "investment",
            "sip",
            "stocks",
            "mutual fund"

        ]:

            investment_spending += amount


    # =========================
    # SMART ALERTS
    # =========================

    budget_alerts = []


    if food_spending > food_budget:

        budget_alerts.append(

            "⚠️ Your food expenses are above the recommended budget."
        )


    if entertainment_spending > entertainment_budget:

        budget_alerts.append(

            "🎬 Entertainment spending is higher than recommended."
        )


    if investment_spending > 0:

        budget_alerts.append(

            "📈 Excellent! You're actively investing for your future."
        )


    if not budget_alerts:

        budget_alerts.append(

            "✅ Your spending habits look financially healthy."
        )


    return render_template(

        "budget.html",

        salary=salary,

        needs_budget=needs_budget,

        wants_budget=wants_budget,

        savings_budget=savings_budget,

        food_budget=food_budget,

        rent_budget=rent_budget,

        transport_budget=transport_budget,

        entertainment_budget=entertainment_budget,

        shopping_budget=shopping_budget,

        travel_budget=travel_budget,

        food_spending=food_spending,

        rent_spending=rent_spending,

        entertainment_spending=entertainment_spending,

        investment_spending=investment_spending,

        budget_alerts=budget_alerts
    )


# =========================
# ANALYTICS PAGE
# =========================

@app.route("/analytics")
def analytics():

    global salary
    global expenses

    # TOTAL EXPENSES

    total_expenses = sum(

        expense["amount"]

        for expense in expenses
    )

    # REMAINING BALANCE

    remaining_balance = (

        salary - total_expenses
    )

    # SPENDING PERCENTAGE

    spending_percentage = 0

    if salary > 0:

        spending_percentage = (

            total_expenses / salary
        ) * 100


    # HIGHEST EXPENSE

    highest_expense = None

    if expenses:

        highest_expense = max(

            expenses,

            key=lambda x: x["amount"]
        )


    # SAVINGS MESSAGE

    if remaining_balance < 0:

        savings_message = (

            "You are overspending this month."
        )

    elif remaining_balance > 20000:

        savings_message = (

            "Excellent savings this month!"
        )

    else:

        savings_message = (

            "Your financial management looks stable."
        )


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


# =========================
# ADVISOR PAGE
# =========================

@app.route("/advisor")
def advisor():

    global salary
    global expenses

    # TOTAL EXPENSES

    total_expenses = sum(

        expense["amount"]

        for expense in expenses
    )

    # REMAINING BALANCE

    remaining_balance = (

        salary - total_expenses
    )

    # SPENDING PERCENTAGE

    spending_percentage = 0

    if salary > 0:

        spending_percentage = (

            total_expenses / salary
        ) * 100


    # HIGHEST EXPENSE

    highest_expense = None

    if expenses:

        highest_expense = max(

            expenses,

            key=lambda x: x["amount"]
        )


    # =========================
    # SMART INVESTMENT DETECTION
    # =========================

    investment_keywords = [

        "investment",
        "sip",
        "mutual fund",
        "stocks",
        "crypto",
        "savings",
        "fd",
        "ppf",
        "nps"
    ]


    total_investments = 0

    for expense in expenses:

        category_lower = (

            expense["category"].lower()
        )

        if category_lower in investment_keywords:

            total_investments += (

                expense["amount"]
            )


    # =========================
    # ADVISOR MESSAGES
    # =========================

    advisor_messages = []


    # HIGH SPENDING WARNING

    if spending_percentage > 80:

        advisor_messages.append(

            "⚠️ Your expenses are very high compared to your salary."
        )


    # HIGHEST EXPENSE MESSAGE

    if highest_expense:

        if highest_expense["category"].lower() in investment_keywords:

            advisor_messages.append(

                f"📈 Excellent! Your highest allocation is towards "
                f"{highest_expense['category']}, which improves "
                f"your long-term financial growth."
            )

        else:

            advisor_messages.append(

                f"💸 Your highest spending is on "
                f"{highest_expense['category']}."
            )


    # INVESTMENT MESSAGE

    if total_investments > 0:

        advisor_messages.append(

            f"✅ Great job! You've invested ₹{total_investments} "
            f"towards your future wealth."
        )

    else:

        advisor_messages.append(

            "💡 Consider investing part of your income into SIPs, "
            "mutual funds, or emergency savings."
        )


    # LOW BALANCE WARNING

    if remaining_balance < 5000:

        advisor_messages.append(

            "⚠️ Your remaining balance is low. "
            "Try reducing unnecessary expenses."
        )


    # GOOD SAVINGS MESSAGE

    if remaining_balance > 20000:

        advisor_messages.append(

            "🚀 You have strong savings potential this month."
        )


    # HEALTH SCORE

    financial_health_score = 100

    if spending_percentage > 90:

        financial_health_score = 40

    elif spending_percentage > 75:

        financial_health_score = 60

    elif spending_percentage > 50:

        financial_health_score = 80


    return render_template(

        "advisor.html",

        advisor_messages=advisor_messages,

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        highest_expense=highest_expense,

        spending_percentage=spending_percentage,

        total_investments=total_investments,

        financial_health_score=financial_health_score
    )


# =========================
# GOALS PAGE
# =========================

@app.route("/goals")
def goals():

    global salary
    global expenses
    global goal_name
    global goal_amount

    # TOTAL EXPENSES

    total_expenses = sum(

        expense["amount"]

        for expense in expenses
    )

    # REMAINING BALANCE

    remaining_balance = (

        salary - total_expenses
    )

    # SPENDING PERCENTAGE

    spending_percentage = 0

    if salary > 0:

        spending_percentage = (

            total_expenses / salary

        ) * 100


    # MONTHS NEEDED

    months_needed = None

    if remaining_balance > 0 and goal_amount > 0:

        months_needed = (

            goal_amount / remaining_balance
        )


    return render_template(

        "goals.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        spending_percentage=spending_percentage,

        goal_name=goal_name,

        goal_amount=goal_amount,

        months_needed=months_needed
    )


# =========================
# SAVE SALARY
# =========================

@app.route("/salary", methods=["POST"])
def save_salary():

    global salary

    salary = float(

        request.form["salary"]
    )

    return redirect("/dashboard")


# =========================
# ADD EXPENSE
# =========================

@app.route("/add", methods=["POST"])
def add_expense():

    global expenses

    category = request.form["category"]

    amount = float(

        request.form["amount"]
    )

    expense = {

        "category": category,

        "amount": amount
    }

    expenses.append(expense)

    return redirect("/dashboard")


# =========================
# DELETE EXPENSE
# =========================

@app.route("/delete/<int:index>")
def delete_expense(index):

    global expenses

    expenses.pop(index)

    return redirect("/dashboard")


# =========================
# EDIT EXPENSE PAGE
# =========================

@app.route("/edit/<int:index>")
def edit_expense(index):

    global expenses

    expense = expenses[index]

    return render_template(

        "edit.html",

        expense=expense,

        index=index
    )


# =========================
# UPDATE EXPENSE
# =========================

@app.route("/update/<int:index>", methods=["POST"])
def update_expense(index):

    global expenses

    updated_category = request.form["category"]

    updated_amount = float(

        request.form["amount"]
    )

    expenses[index]["category"] = (

        updated_category
    )

    expenses[index]["amount"] = (

        updated_amount
    )

    return redirect("/dashboard")


# =========================
# SAVE GOAL
# =========================

@app.route("/goal", methods=["POST"])
def save_goal():

    global goal_name
    global goal_amount

    goal_name = request.form["goal_name"]

    goal_amount = float(

        request.form["goal_amount"]
    )

    return redirect("/goals")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)
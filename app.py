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
# SMART EXPENSE CATEGORIZATION
# =========================

CATEGORY_KEYWORDS = {

    "Food 🍔": {

        "subcategories":[
            "Restaurants",
            "Online Food",
            "Groceries"
        ],

        "keywords":[
            "dominos",
            "pizza",
            "zomato",
            "swiggy"
        ]
    },


    "Utilities ⚡": {

        "subcategories":[
            "Electricity Bill",
            "Water Bill",
            "Gas Bill",
            "Internet"
        ],

        "keywords":[
            "electricity",
            "water",
            "gas",
            "wifi"
        ]
    }

}

def categorize_expense(text):

    text = text.lower()


    for category, keywords in CATEGORY_KEYWORDS.items():

        for word in keywords:

            if word in text:

                return category


    return "Other"



# =========================
# LANDING PAGE
# =========================


@app.route("/")
def landing():

    return render_template(
        "landing.html"
    )



# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    global salary
    global expenses


    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )


    remaining_balance = salary - total_expenses


    return render_template(
        "dashboard.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance
    )



# =========================
# ANALYTICS
# =========================


@app.route("/analytics")
def analytics():


    total_expenses = sum(

        e["amount"]

        for e in expenses
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

            key=lambda x:x["amount"]

        )



    if remaining_balance < 0:

        savings_message = (

            "You are overspending this month."

        )


    elif remaining_balance > 20000:

        savings_message = (

            "Excellent savings habit!"

        )


    else:

        savings_message = (

            "Your finances are stable."

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
# ADVISOR
# =========================


@app.route("/advisor")
def advisor():


    total_expenses = sum(

        e["amount"]

        for e in expenses

    )


    remaining_balance = salary - total_expenses



    spending_percentage = 0


    if salary:

        spending_percentage = (

            total_expenses / salary

        ) * 100



    highest_expense = None


    if expenses:

        highest_expense = max(

            expenses,

            key=lambda x:x["amount"]

        )



    messages = []



    investment_total = 0



    for expense in expenses:


        if expense["category"] == "Investment 📈":

            investment_total += expense["amount"]




    if spending_percentage > 80:

        messages.append(

            "⚠️ Your spending is very high compared to income."

        )



    if highest_expense:


        if highest_expense["category"] == "Investment 📈":

            messages.append(

                "📈 Great! Your biggest allocation is towards investments."

            )

        else:

            messages.append(

                f"💸 Your highest spending is {highest_expense['category']}."

            )



    if investment_total > 0:


        messages.append(

            f"✅ You invested ₹{investment_total}. "
            "This improves your long term financial health."

        )

    else:


        messages.append(

            "💡 Consider starting SIPs or emergency savings."

        )




    health_score = 100


    if spending_percentage > 90:

        health_score = 40

    elif spending_percentage > 70:

        health_score = 65

    elif spending_percentage > 50:

        health_score = 80




    return render_template(

        "advisor.html",

        advisor_messages=messages,

        salary=salary,

        expenses=expenses,

        remaining_balance=remaining_balance,

        highest_expense=highest_expense,

        spending_percentage=spending_percentage,

        financial_health_score=health_score,

        total_investments=investment_total

    )




# =========================
# GOALS
# =========================


@app.route("/goals")
def goals():


    total_expenses = sum(

        e["amount"]

        for e in expenses

    )


    remaining_balance = salary - total_expenses



    months_needed = None



    if remaining_balance > 0 and goal_amount > 0:


        months_needed = (

            goal_amount / remaining_balance

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





# =========================
# BUDGET
# =========================

# =========================
# SMART BUDGET PAGE
# =========================

@app.route("/budget")
def budget():

    global salary
    global expenses


    total_expenses = sum(
        expense["amount"]
        for expense in expenses
    )


    remaining_balance = salary - total_expenses



    # =========================
    # 50/30/20 RULE
    # =========================

    needs_budget = salary * 0.50

    wants_budget = salary * 0.30

    savings_budget = salary * 0.20



    # =========================
    # CATEGORY ALLOCATION
    # =========================


    food_budget = salary * 0.15

    rent_budget = salary * 0.30

    entertainment_budget = salary * 0.05

    travel_budget = salary * 0.10

    shopping_budget = salary * 0.10



    # =========================
    # SMART CATEGORY TRACKING
    # =========================


    food_spending = 0

    rent_spending = 0

    entertainment_spending = 0

    investment_spending = 0



    for expense in expenses:


        category = expense["category"].lower()

        amount = expense["amount"]



        if "food" in category or "restaurant" in category:

            food_spending += amount



        elif "rent" in category:

            rent_spending += amount



        elif "movie" in category or "entertainment" in category:

            entertainment_spending += amount



        elif "investment" in category or "sip" in category:

            investment_spending += amount




    # =========================
    # ALERT SYSTEM
    # =========================


    budget_alerts = []



    if food_spending > food_budget:

        budget_alerts.append(
            "🍔 Food spending is above your recommended limit."
        )


    if rent_spending > rent_budget:

        budget_alerts.append(
            "🏠 Rent is taking a large portion of your income."
        )


    if investment_spending > 0:

        budget_alerts.append(
            "📈 Great job! You are building long-term wealth through investments."
        )


    if remaining_balance < salary*0.10:

        budget_alerts.append(
            "⚠️ Your remaining balance is low. Consider reducing unnecessary expenses."
        )


    if not budget_alerts:

        budget_alerts.append(
            "✅ Your budget allocation looks healthy."
        )



    return render_template(

        "budget.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,


        # 50/30/20

        needs_budget=needs_budget,

        wants_budget=wants_budget,

        savings_budget=savings_budget,


        # category budgets

        food_budget=food_budget,

        rent_budget=rent_budget,

        entertainment_budget=entertainment_budget,

        travel_budget=travel_budget,

        shopping_budget=shopping_budget,


        # actual spending

        food_spending=food_spending,

        rent_spending=rent_spending,

        entertainment_spending=entertainment_spending,

        investment_spending=investment_spending,


        budget_alerts=budget_alerts

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

    sub_category = request.form.get(
        "sub_category",
        "General"
    )


    amount = float(
        request.form["amount"]
    )


    expense = {

        "category": category,

        "sub_category": sub_category,

        "amount": amount
    }


    expenses.append(expense)


    return redirect("/dashboard")




# =========================
# DELETE
# =========================


@app.route("/delete/<int:index>")
def delete_expense(index):


    expenses.pop(index)


    return redirect("/dashboard")





# =========================
# EDIT
# =========================


@app.route("/edit/<int:index>")
def edit_expense(index):


    return render_template(

        "edit.html",

        expense=expenses[index],

        index=index

    )





# =========================
# UPDATE
# =========================


@app.route("/update/<int:index>", methods=["POST"])
def update_expense(index):


    merchant = request.form["category"]


    amount=float(

        request.form["amount"]

    )


    expenses[index]["merchant"]=merchant


    expenses[index]["category"]=categorize_expense(

        merchant

    )


    expenses[index]["amount"]=amount



    return redirect("/dashboard")





# =========================
# SAVE GOAL
# =========================


@app.route("/goal", methods=["POST"])
def save_goal():


    global goal_name

    global goal_amount


    goal_name=request.form["goal_name"]


    goal_amount=float(

        request.form["goal_amount"]

    )


    return redirect("/goals")




if __name__=="__main__":

    app.run(debug=True)
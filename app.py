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
            "swiggy",
            "restaurant",
            "cafe",
            "grocery",
            "supermarket",
            "food"
        ]

    },



    "Transport 🚗": {


        "subcategories":[
            "Cab",
            "Fuel",
            "Public Transport"
        ],


        "keywords":[

            "uber",
            "ola",
            "rapido",
            "petrol",
            "fuel",
            "metro",
            "bus"

        ]

    },



    "Rent 🏠": {


        "subcategories":[

            "House Rent"

        ],


        "keywords":[

            "rent",
            "house",
            "flat"

        ]

    },



    "Utilities 💡": {


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
            "wifi",
            "internet",
            "bill"

        ]

    },



    "Shopping 🛒": {


        "keywords":[

            "amazon",
            "flipkart",
            "myntra",
            "clothes",
            "shopping"

        ]

    },



    "Entertainment 🎬": {


        "keywords":[

            "netflix",
            "spotify",
            "movie",
            "cinema"

        ]

    },



    "Investment 📈": {


        "keywords":[

            "sip",
            "mutual",
            "stocks",
            "zerodha",
            "groww",
            "investment"

        ]

    }

}





def categorize_expense(text):


    text = text.lower()



    for category,data in CATEGORY_KEYWORDS.items():


        for word in data["keywords"]:


            if word in text:

                return category



    return "Other"




# =========================
# DASHBOARD
# =========================


@app.route("/dashboard")
def dashboard():


    global salary
    global expenses



    total_expenses = sum(
        e["amount"]
        for e in expenses
    )



    remaining_balance = salary-total_expenses




    category_budget={


        "Food 🍔":salary*0.15,

        "Transport 🚗":salary*0.10,

        "Rent 🏠":salary*0.30,

        "Shopping 🛒":salary*0.10,

        "Entertainment 🎬":salary*0.05,

        "Utilities 💡":salary*0.10,

        "Investment 📈":salary*0.20


    }





    category_spending={}



    for expense in expenses:


        category=expense["category"]


        category_spending[category]=category_spending.get(
            category,
            0
        ) + expense["amount"]





    budget_progress=[]



    for category,limit in category_budget.items():


        spent=category_spending.get(
            category,
            0
        )



        percentage=0


        if limit>0:

            percentage=(spent/limit)*100




        if percentage<60:

            status="Healthy"
            color="green"


        elif percentage<90:

            status="Near Limit"
            color="yellow"


        else:

            status="Overspent"
            color="red"




        budget_progress.append({


            "category":category,

            "spent":spent,

            "limit":limit,

            "percentage":round(
                percentage,
                1
            ),

            "status":status,

            "color":color

        })




    return render_template(

        "dashboard.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        budget_progress=budget_progress

    )

# =========================
# ANALYTICS
# =========================


@app.route("/analytics")
def analytics():


    total_expenses=sum(
        e["amount"]
        for e in expenses
    )


    remaining_balance=salary-total_expenses



    spending_percentage=0


    if salary>0:

        spending_percentage=(
            total_expenses/salary
        )*100



    highest_expense=None


    if expenses:

        highest_expense=max(
            expenses,
            key=lambda x:x["amount"]
        )



    if remaining_balance < 0:

        savings_message="You are overspending this month."

    elif remaining_balance > salary*0.3:

        savings_message="Excellent savings habit!"

    else:

        savings_message="Your finances are stable."



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
# GOALS
# =========================


@app.route("/goals")
def goals():


    total_expenses=sum(
        e["amount"]
        for e in expenses
    )


    remaining_balance=salary-total_expenses



    months_needed=None



    if remaining_balance>0 and goal_amount>0:


        months_needed=(
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






# =========================
# BUDGET
# =========================


@app.route("/budget")
def budget():


    total_expenses=sum(
        e["amount"]
        for e in expenses
    )



    remaining_balance=salary-total_expenses



    needs_budget=salary*0.50

    wants_budget=salary*0.30

    savings_budget=salary*0.20




    food_budget=salary*0.15

    rent_budget=salary*0.30

    entertainment_budget=salary*0.05

    travel_budget=salary*0.10

    shopping_budget=salary*0.10





    food_spending=0

    rent_spending=0

    entertainment_spending=0

    investment_spending=0



    for expense in expenses:


        category=expense["category"]


        amount=expense["amount"]



        if category=="Food 🍔":

            food_spending+=amount



        elif category=="Rent 🏠":

            rent_spending+=amount



        elif category=="Entertainment 🎬":

            entertainment_spending+=amount



        elif category=="Investment 📈":

            investment_spending+=amount






    budget_alerts=[]



    if food_spending>food_budget:

        budget_alerts.append(
            "🍔 Food spending is above limit."
        )



    if rent_spending>rent_budget:

        budget_alerts.append(
            "🏠 Rent is taking a large portion of income."
        )



    if investment_spending>0:

        budget_alerts.append(
            "📈 Great job! You are investing."
        )



    if remaining_balance < salary*0.10:

        budget_alerts.append(
            "⚠️ Low remaining balance."
        )



    if not budget_alerts:

        budget_alerts.append(
            "✅ Budget looks healthy."
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

# =========================
# SAVE SALARY
# =========================


@app.route("/salary", methods=["POST"])
def save_salary():

    global salary


    salary=float(
        request.form["salary"]
    )


    return redirect("/dashboard")





# =========================
# ADD EXPENSE
# =========================


@app.route("/add", methods=["POST"])
def add_expense():

    global expenses



    merchant=request.form["category"]


    amount=float(
        request.form["amount"]
    )


    category=categorize_expense(
        merchant
    )


    expense={


        "merchant":merchant,


        "category":category,


        "amount":amount

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


    merchant=request.form["category"]


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
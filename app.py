from flask import Flask, render_template, request, redirect
from models import db, User, Income, Expense, Goal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-to-a-random-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))



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

#forgot password
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        confirm = request.form["confirm_password"]

        if password != confirm:

            return "Passwords do not match."

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return "User not found."

        user.password = generate_password_hash(password)

        db.session.commit()

        return redirect("/login")

    return render_template(
        "forgot_password.html"
    )


#signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        confirm = request.form["confirm_password"]

        # Passwords must match
        if password != confirm:

            return "Passwords do not match."

        # Email already exists?
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return "Email already registered."

        hashed_password = generate_password_hash(password)

        new_user = User(

            name=name,

            email=email,

            password=hashed_password

        )

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

#login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect("/dashboard")

        return "Invalid email or password."

    return render_template("login.html")
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


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
@login_required
def dashboard():

    income = Income.query.filter_by(
        user_id=current_user.id
    ).first()

    salary = income.amount if income else 0

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_expenses = sum(
        expense.amount
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
            expense.category
        )

        if category in category_spending:

            category_spending[category] += expense.amount

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
@login_required
def analytics():

    # Current user's salary
    income = Income.query.filter_by(
        user_id=current_user.id
    ).first()

    salary = income.amount if income else 0

    # Current user's expenses
    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_expenses = sum(
        expense.amount
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
            key=lambda expense: expense.amount
        )

    if remaining_balance < 0:

        savings_message = "You are overspending this month."

    elif remaining_balance > salary * 0.30:

        savings_message = "Excellent savings habit!"

    else:

        savings_message = "Your finances are stable."

    chart_data = [
    {
        "category": expense.category,
        "amount": expense.amount
    }
    for expense in expenses
]

    return render_template(

        "analytics.html",

        salary=salary,

        expenses=expenses,

        total_expenses=total_expenses,

        remaining_balance=remaining_balance,

        highest_expense=highest_expense,

        spending_percentage=spending_percentage,

        savings_message=savings_message,

        chart_data = chart_data

    )

# ======================================
# GOALS
# ======================================
@app.route("/goals")
@login_required
def goals():

    # Salary
    income = Income.query.filter_by(
        user_id=current_user.id
    ).first()

    salary = income.amount if income else 0

    # Expenses
    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_expenses = sum(
        expense.amount
        for expense in expenses
    )

    remaining_balance = salary - total_expenses

    # Goal
    goal = Goal.query.filter_by(
        user_id=current_user.id
    ).first()

    goal_name = ""
    goal_amount = 0

    if goal:

        goal_name = goal.goal_name
        goal_amount = goal.goal_amount

    months_needed = None

    if remaining_balance > 0 and goal_amount > 0:

        months_needed = round(
            goal_amount / remaining_balance,
            1
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
@login_required
def budget():

    # Load the current user's salary
    income = Income.query.filter_by(
        user_id=current_user.id
    ).first()

    salary = income.amount if income else 0

    expenses = Expense.query.filter_by(
    user_id=current_user.id
    
    ).all()

    total_expenses = sum(
    expense.amount
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
            expense.category
        )

        amount = expense.amount

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
@login_required
def save_salary():

    amount = float(request.form["salary"])

    income = Income.query.filter_by(
        user_id=current_user.id
    ).first()

    if income:
        income.amount = amount
    else:
        income = Income(
            amount=amount,
            user_id=current_user.id
        )
        db.session.add(income)

    db.session.commit()

    return redirect("/dashboard")

# ======================================
# ADD EXPENSE
# ======================================

@app.route("/add", methods=["POST"])
@login_required
def add_expense():

    category = request.form["category"].strip()

    amount = float(request.form["amount"])

    expense = Expense(

        category=category,

        amount=amount,

        user_id=current_user.id

    )

    db.session.add(expense)

    db.session.commit()

    return redirect("/dashboard")


# ======================================
# DELETE EXPENSE
# ======================================

@app.route("/delete/<int:id>")
@login_required
def delete_expense(id):

    expense = Expense.query.filter_by(

        id=id,

        user_id=current_user.id

    ).first()

    if expense:

        db.session.delete(expense)

        db.session.commit()

    return redirect("/dashboard")

# ======================================
# EDIT EXPENSE
# ======================================

@app.route("/edit/<int:id>")
@login_required
def edit_expense(id):

    expense = Expense.query.filter_by(

        id=id,

        user_id=current_user.id

    ).first()

    if not expense:

        return redirect("/dashboard")

    return render_template(

        "edit.html",

        expense=expense

    )


# ======================================
# UPDATE EXPENSE
# ======================================

@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update_expense(id):

    expense = Expense.query.filter_by(

        id=id,

        user_id=current_user.id

    ).first()

    if not expense:

        return redirect("/dashboard")

    expense.category = request.form["category"].strip()

    expense.amount = float(
        request.form["amount"]
    )

    db.session.commit()

    return redirect("/dashboard")


# ======================================
# SAVE GOAL
# ======================================

@app.route("/goal", methods=["POST"])
@login_required
def save_goal():

    goal_name = request.form["goal_name"].strip()

    goal_amount = float(
        request.form["goal_amount"]
    )

    goal = Goal.query.filter_by(
        user_id=current_user.id
    ).first()

    if goal:

        goal.goal_name = goal_name
        goal.goal_amount = goal_amount

    else:

        goal = Goal(

            goal_name=goal_name,

            goal_amount=goal_amount,

            user_id=current_user.id

        )

        db.session.add(goal)

    db.session.commit()

    return redirect("/goals")

# ======================================
# RUN APP
# ======================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
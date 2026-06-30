import os
from services.portfolio_service import calculate_portfolio
from services.portfolio_analytics import create_portfolio_chart
from services.analytics_service import (
    get_dashboard_stats,
    get_prediction_charts
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from services.analytics_service import get_dashboard_stats
from werkzeug.security import check_password_hash
from functools import wraps
from database.db import create_user
import csv
from io import StringIO
from flask import Response
from services.prediction_service import predict_stock
from database.db import (
    initialize_database,
    save_prediction,
    fetch_predictions,
    fetch_all_predictions,
    clear_history,
    add_to_watchlist,
    get_watchlist,
    delete_from_watchlist,
    create_user,
    login_user,
    get_user_by_id,
    get_prediction_count,
    get_watchlist_count,
    update_user,
    update_password,
    update_profile_image,
    add_portfolio_stock,
    get_portfolio,
    delete_portfolio_stock
)
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ==========================================
# Upload Configuration
# ==========================================

UPLOAD_FOLDER = "static/uploads/profiles"

ALLOWED_EXTENSIONS = {

    "png",

    "jpg",

    "jpeg",

    "webp"

}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "stockvision_ai_secret_key"

# ==========================================
# GLOBAL USER CONTEXT
# ==========================================

@app.context_processor
def inject_user():

    if "user_id" in session:

        user = get_user_by_id(

            session["user_id"]

        )

    else:

        user = None

    return {

        "current_user": user

    }

# ==========================================
# LOGIN REQUIRED DECORATOR
# ==========================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".", 1)[1].lower()

        in ALLOWED_EXTENSIONS

    )

initialize_database()

@app.route("/")
@login_required
def home():

    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@login_required
def predict():

    symbol = request.form["symbol"]

    try:

        result = predict_stock(symbol)

        save_prediction(
        session["user_id"],
        result["symbol"],
        result["current_price"],
        result["prediction"],
        result["change_percent"],
        result["signal"]
    )

        return render_template(
            "index.html",
            **result
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=str(e)
        )

@app.route("/history")
@login_required
def history():
    rows = fetch_predictions(session["user_id"])
    return render_template(
        "history.html",
        rows=rows
    )

@app.route("/history/export")
@login_required
def export_history():

    rows = fetch_all_predictions(session["user_id"])

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Stock",
        "Current Price",
        "Predicted Price",
        "Change %",
        "Signal",
        "Time"
    ])

    writer.writerows(rows)

    output.seek(0)

    return Response(

        output,

        mimetype="text/csv",

        headers={

            "Content-Disposition":
            "attachment; filename=prediction_history.csv"

        }

    )

@app.route("/history/clear")
@login_required
def clear_prediction_history():

    clear_history(session["user_id"])

    return redirect("/history")

@app.route("/watchlist")
@login_required
def watchlist():

    rows = get_watchlist(session["user_id"])

    stocks = []

    for row in rows:

        try:

            result = predict_stock(row["symbol"])

            result["id"] = row["id"]

            result["added_on"] = row["added_on"]

            stocks.append(result)

        except Exception:

            pass

    return render_template(

        "watchlist.html",

        stocks=stocks

    )


@app.route("/watchlist/add/<symbol>")
@login_required
def add_watch(symbol):

    add_to_watchlist(session["user_id"], symbol)

    return redirect("/watchlist")


@app.route("/watchlist/delete/<int:id>")
@login_required
def delete_watch(id):

    delete_from_watchlist(session["user_id"], id)

    return redirect("/watchlist")

@app.route("/about")
@login_required
def about():

    return render_template(
        "about.html"
    )


@app.route("/metrics")
@login_required
def metrics():

    return render_template(
        "metrics.html"
    )

@app.route("/compare")
@login_required
def compare():

    return render_template(
        "compare.html"
    )

@app.route("/compare/result", methods=["POST"])
@login_required
def compare_result():

    symbols = request.form["symbols"]

    symbol_list = [

        symbol.strip().upper()

        for symbol in symbols.split(",")

        if symbol.strip()

    ]

    results = []

    for symbol in symbol_list:

        try:

            results.append(
                predict_stock(symbol)
            )

        except Exception:

            pass

    if results:

        best_stock = max(

            results,

            key=lambda x: x["confidence"]

        )

        highest_upside = max(

            results,

            key=lambda x: x["change_percent"]

        )

        lowest_risk = min(

            results,

            key=lambda x: x["volatility"]

        )

    else:

        best_stock = None

        highest_upside = None

        lowest_risk = None

    return render_template(

        "compare_result.html",

        results=results,

        best_stock=best_stock,

        highest_upside=highest_upside,

        lowest_risk=lowest_risk

    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        success = create_user(

            name,

            email,

            password

        )

        if success:

            return redirect("/login")

        return render_template(

            "register.html",

            error="Email already exists."

        )

    return render_template(

        "register.html"

    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = login_user(

            email,

            password

        )

        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            session["profile_image"] = user["profile_image"]

            return redirect("/")

        return render_template(

            "login.html",

            error="Invalid email or password."

        )

    return render_template(

        "login.html"
    )

# ==========================================
# USER PROFILE
# ==========================================

@app.route("/profile")
@login_required
def profile():

    user = get_user_by_id(session["user_id"])

    total_predictions = get_prediction_count(
        session["user_id"]
    )

    watchlist_count = get_watchlist_count(
        session["user_id"]
    )

    return render_template(

        "profile.html",

        user=user,

        total_predictions=total_predictions,

        watchlist_count=watchlist_count

    )

@app.route("/analytics")
@login_required
def analytics():

    stats = get_dashboard_stats(
        session["user_id"]
    )

    charts = get_prediction_charts(
        session["user_id"]
    )

    return render_template(

        "analytics.html",

        stats=stats,

        charts=charts

    )

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    user = get_user_by_id(session["user_id"])

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        success = update_user(

            session["user_id"],

            name,

            email

        )

        if success:

            session["user_name"] = name

            session["user_email"] = email

            user = get_user_by_id(session["user_id"])

            return render_template(

                "settings.html",

                user=user,

                success="Profile updated successfully."

            )

        return render_template(

            "settings.html",

            user=user,

            error="Email already exists."

        )

    return render_template(

        "settings.html",

        user=user

    )

@app.route("/upload-profile-photo", methods=["POST"])
@login_required
def upload_profile_photo():

    if "photo" not in request.files:

        return redirect("/settings")

    file = request.files["photo"]

    if file.filename == "":

        return redirect("/settings")

    if file and allowed_file(file.filename):

        extension = file.filename.rsplit(".", 1)[1].lower()

        filename = f"user_{session['user_id']}.{extension}"

        filepath = os.path.join(

            app.config["UPLOAD_FOLDER"],

            filename

        )

        file.save(filepath)

        update_profile_image(

            session["user_id"],

            filename

        )

        session["profile_image"] = filename

    return redirect("/settings")

@app.route("/change-password", methods=["POST"])
@login_required
def change_password():

    current_password = request.form["current_password"]

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]

    user = get_user_by_id(session["user_id"])

    if not check_password_hash(

        user["password"],

        current_password

    ):

        return render_template(

            "settings.html",

            user=user,

            error="Current password is incorrect."

        )

    if new_password != confirm_password:

        return render_template(

            "settings.html",

            user=user,

            error="Passwords do not match."

        )

    import re

    if len(new_password) < 8:

        return render_template(

            "settings.html",

            user=user,

            error="Password must contain at least 8 characters."

        )

    if not re.search(r"[A-Z]", new_password):

        return render_template(

            "settings.html",

            user=user,

            error="Password needs one uppercase letter."

        )

    if not re.search(r"[0-9]", new_password):

        return render_template(

            "settings.html",

            user=user,

            error="Password needs one digit."

    )

        return render_template(

            "settings.html",

            user=user,

            error="Password must be at least 6 characters."

        )

    update_password(

        session["user_id"],

        new_password

    )

    return render_template(

        "settings.html",

        user=user,

        success="Password updated successfully."

    )

@app.route("/portfolio")
@login_required
def portfolio():

    rows = get_portfolio(session["user_id"])

    rows, summary = calculate_portfolio(rows)

    portfolio_chart = create_portfolio_chart(rows)

    return render_template(

        "portfolio.html",

        rows=rows,

        summary=summary,

        portfolio_chart=portfolio_chart

    )


@app.route("/portfolio/add", methods=["POST"])
@login_required
def add_portfolio():

    symbol = request.form["symbol"]

    quantity = int(

        request.form["quantity"]

    )

    buy_price = float(

        request.form["buy_price"]

    )

    add_portfolio_stock(

        session["user_id"],

        symbol,

        quantity,

        buy_price

    )

    return redirect("/portfolio")


@app.route("/portfolio/delete/<int:id>")
@login_required
def delete_portfolio(id):

    delete_portfolio_stock(

        session["user_id"],

        id

    )

    return redirect("/portfolio")

@app.route("/logout")
@login_required
def logout():

    session.clear()

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
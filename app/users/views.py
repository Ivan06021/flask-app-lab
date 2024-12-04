from datetime import timedelta
from flask import (
    flash,
    make_response,
    render_template,
    request,
    redirect,
    session,
    url_for,
)
from . import user_bp


@user_bp.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age", 0, int)
    return render_template("users/hi.html", name=name, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greeting", age=45, name="administrator", external=True)
    print(to_url)
    return redirect(to_url)


@user_bp.route("/profile")
def get_profile():
    if "username" in session:
        username = session["username"]
        return render_template("users/profile.html", username=username)
    flash("You need to login", "danger")
    return redirect(url_for("users.login"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correct_username = "admin"
        correct_password = "admin"
        username = request.form.get("username")
        password = request.form.get("password")
        if username == correct_username and password == correct_password:
            session["username"] = username
            flash("You are successfully logged in", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("users.login"))
    if "username" in session:
        flash("You are already logged in", "info")
        return redirect(url_for("users.get_profile"))
    return render_template("users/login.html")


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("age", None)
    return redirect(url_for("users.get_profile"))


@user_bp.route("/set_cookie")
def set_cookie():
    response = make_response("Кука установлена")
    response.set_cookie(
        "username", "student", max_age=timedelta(seconds=60).total_seconds()
    )
    response.set_cookie("color", "black", max_age=timedelta(seconds=60).total_seconds())
    return response


@user_bp.route("/get_cookie")
def get_cookie():
    username = request.cookies.get("username")
    return f"Користувач: {username}"


@user_bp.route("/delete_cookie")
def delete_cookie():
    response = make_response("Кука видалена")
    response.set_cookie("username", "", expires=0)
    return response

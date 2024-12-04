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
        return render_template(
            "users/profile.html", username=username, cookies=request.cookies
        )
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
    flash("You are successfully logged out", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/set_cookie", methods=["GET", "POST"])
def set_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age", 60, int)
    if not key or not value or not max_age:
        flash("Заповніть всі поля", "danger")
        return redirect(url_for("users.get_profile"))
    flash(f"Кука {key} зі значенням {value} встановлена", "success")

    response = make_response(redirect(url_for("users.get_profile")))
    response.set_cookie(key, value, max_age=max_age)
    return response


@user_bp.route("/get_cookie", methods=["GET", "POST"])
def get_cookie():
    username = request.cookies.get("username")
    return f"Користувач: {username}"


@user_bp.route("/delete_cookie", methods=["GET", "POST"])
def delete_cookie():
    key = request.form.get("key")
    flash(f"Кука {key} видалена", "info")
    response = make_response(redirect(url_for("users.get_profile")))
    response.set_cookie(key, "", expires=0)
    return response


@user_bp.route("/delete_all_cookies", methods=["GET", "POST"])
def delete_all_cookies():
    flash("All cookies are deleted", "info")
    response = make_response(redirect(url_for("users.get_profile")))
    for key in request.cookies:
        response.set_cookie(key, "", expires=0)
    return response

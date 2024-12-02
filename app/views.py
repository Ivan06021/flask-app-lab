from flask import render_template, request, redirect, url_for, abort
from . import app


@app.route("/")
def main():
    return render_template("hello.html")


@app.route("/homepage")
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return render_template("home.html", agent=agent)


@app.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age", 0, int)
    return render_template("hi.html", name=name, age=age)


@app.route("/admin")
def admin():
    to_url = url_for("greeting", name="administrator", age=30, _external=True)
    print(to_url)
    return redirect(to_url)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Моє резюме")
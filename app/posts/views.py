import os
from flask import json, render_template, abort, redirect, flash, session, url_for
from . import post_bp
from .forms import PostForm

DB = "posts.json"


def load_posts():
    if not os.path.exists(DB):
        return []
    with open(DB, "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts):
    with open(DB, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


@post_bp.route("/")
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>")
def get_post(id):
    posts = load_posts()
    if id > len(posts) or id <= 0:  # Перевіряємо, чи існує пост
        abort(404)
    post = posts[id - 1]
    return render_template("detail-post.html", post=post)


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data.strftime("%Y-%m-%d"),
            "category": form.category.data,
            "author": session.get("username", "Anonymous"),
        }
        posts.append(new_post)
        save_posts(posts)
        flash("Post added successfully", "success")
        return redirect(url_for("posts.add_post"))
    return render_template("add_post.html", form=form)

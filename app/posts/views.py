from flask import render_template, redirect, flash, session, url_for
from . import post_bp
from .forms import PostForm
from app.posts.models import Post
from app import db


@post_bp.route("/")
def get_posts():
    posts = Post.query.order_by(Post.posted.asc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>")
def get_post(id):
    post = Post.query.get(id)
    return render_template("detail-post.html", post=post)


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,
            category=form.category.data,
            author=session.get("username", "Anonymous"),
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.add_post"))
    return render_template("add_post.html", form=form)


@post_bp.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for(".get_posts"))
    return render_template("edit-post.html", form=form, post=post)


@post_bp.route("/delete_post/<int:id>", methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully", "success")
    return redirect(url_for(".get_posts"))

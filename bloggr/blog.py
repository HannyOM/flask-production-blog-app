from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from .models import Post
from flask_login import current_user, login_required
from . import db
from datetime import date


# Define the blueprint
bp = Blueprint("blog",          # Names the blueprint. 
               __name__)            # Lets the blueprint know where it is defined.


# INDEX VIEW
@bp.route("/")
def index():
    all_posts = Post.query.all()
    return render_template("blog/index.html", all_posts=all_posts, user=current_user)


# NEW POST VIEW
@bp.route("/new", methods=["GET"])
@login_required
def new():
    return render_template("blog/new.html")


# ADD POST VIEW
@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":            # Gets the user input.
        title = request.form.get("post_title")
        content = request.form.get("post_content")
        error = None
        
        if not title:           # Ensures the user has inputted something.
            error = "Title is required."
        elif not content:
            error = "Content is required."
        
        if error is not None:
            error_msg = flash(error)
            return render_template("blog/new.html", error_msg=error_msg)
        else:
            new_content = Post(title=title, content=content,author_id=current_user.id, date=date.today()) #type: ignore            # Updates the database with the user's input.
            db.session.add(new_content)
            db.session.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/new.html")


# EDIT POST VIEW
@bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit(post_id):
    editing_post = db.get_or_404(Post, post_id)
    if editing_post.author_id != current_user.id: # type: ignore
        abort(403)
    return render_template("blog/edit.html", editing_post=editing_post)


# SAVE POST VIEW
@bp.route("/save/<int:post_id>", methods=["POST"])
@login_required
def save(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    if request.method == "POST":
        new_title = request.form.get("new_post_title")
        new_content = request.form.get("new_post_content")
        error = None

        if not new_title:
            error = "Title is required."
        elif not new_content:
            error = "Content is required."

        if error is not None:
            error_msg = flash(error)
            return render_template("blog/edit.html", editing_post=editing_post, error_msg=error_msg) # type: ignore
        else:
            editing_post.title = new_title # type: ignore
            editing_post.content = new_content # type: ignore
            db.session.commit()
    return redirect(url_for("blog.index"))


# DELETE POST VIEW
@bp.route("/delete/<int:post_id>", methods=["GET"])
@login_required
def delete(post_id):
    deleting_post = db.get_or_404(Post, post_id)
    if deleting_post.author_id != current_user.id: # type: ignore
        abort(403)
    else:    
        db.session.delete(deleting_post)
        db.session.commit()
    return redirect(url_for("blog.index"))
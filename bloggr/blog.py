from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Post
from flask_login import current_user, login_required
from . import db
from datetime import date


# Define the blueprint
bp = Blueprint("blog",          # Names the blueprint. 
               __name__)            # Lets the blueprint know where it is defined.

# INDEX ROUTE
@bp.route("/")
def index():
    all_posts = Post.query.all()
    return render_template("blog/index.html", all_posts=all_posts, user=current_user)

# NEW POST ROUTE
@bp.route("/new", methods=["GET"])
@login_required
def new():
    return render_template("blog/new.html")

# ADD POST ROUTE
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
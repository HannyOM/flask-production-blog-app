from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from .models import Post
from flask_security.decorators import auth_required, roles_accepted
from flask_login import current_user
from . import db
from datetime import date


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    all_posts = Post.query.filter_by(is_published=True).all()
    return render_template("blog/index.html", all_posts=all_posts, user=current_user)


@bp.route("/post/<int:post_id>")
def post(post_id):
    post = db.get_or_404(Post, post_id)
    if not post.is_published and (not current_user.is_authenticated or post.author_id != current_user.id):
        abort(404)
    return render_template("blog/post.html", post=post, user=current_user)


@bp.route("/articles")
def articles():
    all_posts = Post.query.filter_by(is_published=True).all()
    return render_template("blog/articles.html", all_posts=all_posts, user=current_user)


@bp.route("/search")
def search():
    query = request.args.get("q", "")
    if query:
        all_posts = Post.query.filter(
            Post.is_published == True,
            (Post.title.ilike(f"%{query}%")) | (Post.content.ilike(f"%{query}%"))
        ).all()
    else:
        all_posts = []
    return render_template("blog/search.html", all_posts=all_posts, query=query, user=current_user)


@bp.route("/new", methods=["GET"])
@auth_required()
@roles_accepted("admin", "editor")
def new():
    return render_template("blog/new.html")


@bp.route("/add", methods=["GET", "POST"])
@auth_required()
def add():
    if request.method == "POST":
        title = request.form.get("post_title")
        content = request.form.get("post_content")
        publish_now = request.form.get("publish_now") == "on"
        error = None
        
        if not title:
            error = "Title is required."
        elif not content:
            error = "Content is required."
        
        if error is not None:
            flash(error)
            return render_template("blog/new.html")
        else:
            new_content = Post(
                title=title,
                content=content,
                author_id=current_user.id,
                date=date.today(),
                is_published=publish_now
            )
            db.session.add(new_content)
            db.session.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/new.html")


@bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
@auth_required()
def edit(post_id):
    editing_post = db.get_or_404(Post, post_id)
    if editing_post.author_id != current_user.id:
        abort(403)
    return render_template("blog/edit.html", editing_post=editing_post)


@bp.route("/save/<int:post_id>", methods=["POST"])
@auth_required()
def save(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    if editing_post.author_id != current_user.id:
        abort(403)
    if request.method == "POST":
        new_title = request.form.get("new_post_title")
        new_content = request.form.get("new_post_content")
        publish_now = request.form.get("publish_now") == "on"
        error = None

        if not new_title:
            error = "Title is required."
        elif not new_content:
            error = "Content is required."

        if error is not None:
            flash(error)
            return render_template("blog/edit.html", editing_post=editing_post)
        else:
            editing_post.title = new_title
            editing_post.content = new_content
            editing_post.is_published = publish_now
            db.session.commit()
    return redirect(url_for("blog.index"))


@bp.route("/delete/<int:post_id>", methods=["GET"])
@auth_required()
def delete(post_id):
    deleting_post = db.get_or_404(Post, post_id)
    if deleting_post.author_id != current_user.id:
        abort(403)
    else:    
        db.session.delete(deleting_post)
        db.session.commit()
    return redirect(url_for("blog.index"))


@bp.route("/profile/<username>")
def profile(username):
    from .models import User
    profile_user = User.query.filter_by(username=username).first_or_404()
    published_posts = Post.query.filter_by(author_id=profile_user.id, is_published=True).all()
    is_owner = current_user.is_authenticated and current_user.id == profile_user.id
    if is_owner:
        draft_posts = Post.query.filter_by(author_id=profile_user.id, is_published=False).all()
    else:
        draft_posts = []
    return render_template("blog/profile.html", profile_user=profile_user, posts=published_posts, drafts=draft_posts, is_owner=is_owner)


@bp.route("/profile/edit", methods=["GET", "POST"])
@auth_required()
def edit_profile():
    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")
        error = None

        if not new_username:
            error = "Username is required."
        elif not new_email:
            error = "Email is required."

        if error is not None:
            flash(error)
            return render_template("blog/edit_profile.html")

        current_user.username = new_username
        current_user.email = new_email
        db.session.commit()
        flash("Profile updated successfully.")
        return redirect(url_for("blog.profile", username=current_user.username))

    return render_template("blog/edit_profile.html")


@bp.route("/api/user/<int:user_id>")
def get_user(user_id):
    from .models import User
    user = db.get_or_404(User, user_id)
    post_count = Post.query.filter_by(author_id=user.id).count()
    return jsonify({
        "username": user.username,
        "joined": user.confirmed_at.strftime("%B %d, %Y") if user.confirmed_at else "Unknown",
        "roles": [role.name for role in user.roles],
        "post_count": post_count
    })

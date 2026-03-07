import pytest
from bloggr.models import Post
from datetime import date


# Test to see if the index page works.
def test_index(client, create_user, auth):
    response = client.get("/")
    assert b"New Post" in response.data

    auth.login()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


# Test to see if the app sends the unauthenticated user to the login page.
@pytest.mark.parametrize(("path", "method"), (("/new", "GET"), 
                                              ("/add", "POST"), 
                                              ("/edit/2", "GET"), 
                                              ("/save/2", "POST"), 
                                              ("/delete/2", "GET")))
def test_login_required(client, path, method):
    if method == "GET":
        response = client.get(path)
    else:
        response = client.post(path)
    assert response.headers["Location"].startswith("/login")


# Test to see if only the author of a post can edit it.
def test_author_required(app, db, create_user, create_user2, auth, client):         # Tests that the author_id is required to determine who has permission to edit or delete a post. 
    with app.app_context():
        username, password, user, email, confirmed_at, fs_uniquifier = create_user          # Creates User1.
        username2, password2, user2, email2, confirmed_at2, fs_uniquifier2 = create_user2          # Creates User2.

        post = Post(            # Creates a post from User1
                title = "User1 Blog Post", # type:ignore
                content = "This is actually his first blog post.", # type:ignore
                author_id = user.id, # type:ignore
                date = date.today() # type:ignore
            )
        db.session.add(post)
        db.session.commit()
        retrieved_post = Post.query.filter_by(id=1).first()
        retrieved_post.author_id = user2.id # type: ignore             # Changes the author_id of User1's post(User1's id) to User2's id.
        db.session.commit()

    auth.login()            # Logs in User1
    assert client.get("/edit/1").status_code == 302        # Asserts that if User1 tries to edit the post(whose author_id was reassigned User2's id), User1 will be redirected.
    assert client.get("/delete/1").status_code == 302       # Asserts that if User1 tries to delete the post(whose author_id was reassigned User2's id), User1 will be redirected.


# To see if the path exists.
@pytest.mark.parametrize(("path"), (("/edit/2"),            # Tests that a path must exist to be accessed.
                                    ("/delete/2")))
def test_exists_required(client, create_user, auth, path):          
    auth.login()
    response = client.get(path)
    assert response.status_code == 302          # Asserts that if the path does not exist, a 404 status code is returned.


# Test to see if adding post works.
def test_add_post(client, create_user, auth, app):
    auth.login()
    response = client.get("/new")
    assert response.status_code == 200

    client.post("/add", data={"post_title" : "The Post title",
                              "post_content" : "The Post content"})
    with app.app_context():
        count = Post.query.count()
        assert count == 1


# Test to see if editing post works.
def test_edit_post(client, create_user, auth, app, db):
    auth.login()
    client.post("/add", data={"post_title" : "The post title",
                              "post_content" : "The post content"})
    response = client.get("/edit/1")
    assert response.status_code == 200

    client.post("/save/1", data={"new_post_title" : "The new post title",
                                 "new_post_content" : "The new post content"})
    with app.app_context():
        edited_post = db.get_or_404(Post, 1)
        assert edited_post.title == "The new post title"


# Test to see if a new post is properly validated before it is added.
@pytest.mark.parametrize(("title", "content", "message"),(("", "", b"Title is required."),
                                                          ("Test post title", "", b"Content is required.")))
def test_add_post_validate(client, create_user, auth, title, content, message):
    auth.login()
    response = client.post("/add", data={"post_title" : title,
                                         "post_content" : content})
    assert message in response.data
    print(response)


# Test to see if a post is properly validated before it is edited.
@pytest.mark.parametrize(("new_title", "new_content", "message"),(("", "", b"Title is required."),
                                                          ("New test post title", "", b"Content is required.")))
def test_edit_post_validate(client, create_user, auth, new_title, new_content, message):
    auth.login()
    client.post("/add", data={"post_title" : "The post title",
                              "post_content" : "The post content"})
    response = client.post("/save/1", data={"new_post_title" : new_title,
                                            "new_post_content" : new_content})
    assert message in response.data
    print(response)


# Test to see if deleting post works.
def test_delete(client, create_user, auth, app):
    auth.login()
    print(auth.login().data)
    client.post("/add", data={"post_title" : "The post title",
                              "post_content" : "The post content"})
    with app.app_context():
        count = Post.query.count()
        assert count == 1
    
    client.get("/delete/1")
    with app.app_context():
        count = Post.query.count()
        assert count == 0
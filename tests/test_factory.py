from bloggr import create_app

def test_config():          # Tests that the app factory sets default config and accepts overrides.
    app = create_app()
    assert app.config["TESTING"] is False

    app = create_app({"TESTING" : True})
    assert app.config["TESTING"] is True


def test_index_route(client):           # Tests that the index route from the blog blueprint loads successfully.
    response = client.get("/")
    assert response.status_code == 200
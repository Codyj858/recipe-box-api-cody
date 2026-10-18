from app import create_app

app = create_app("testing")

with app.test_client() as client:
    # 1) Register
    resp = client.post("/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass"
    })
    print("register:", resp.status_code, resp.json)

    # 2) Login
    resp = client.post("/login", json={
        "username": "testuser2",
        "password": "testpass"
    })
    print("login:", resp.status_code)
    token = resp.json["token"]

    # 3) List recipes
    resp = client.get("/recipes", headers={
        "Authorization": f"Bearer {token}"
    })
    print("recipes:", resp.status_code, resp.json)
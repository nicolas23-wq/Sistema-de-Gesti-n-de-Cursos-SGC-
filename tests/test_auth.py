def test_login_exitoso(client):
    resp = client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    assert resp.status_code == 302
    assert "/admin/" in resp.headers["Location"]


def test_login_credenciales_invalidas(client):
    resp = client.post("/login", data={"email": "admin@test.com", "password": "incorrecta"})
    assert resp.status_code == 200
    assert b"Credenciales invalidas" in resp.data


def test_logout(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Session cerrada" in resp.data or b"Sesion cerrada" in resp.data


def test_ruta_protegida_redirige_a_login(client):
    resp = client.get("/admin/")
    assert resp.status_code in (302, 401)
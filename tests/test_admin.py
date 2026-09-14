def test_admin_crea_curso(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.post(
        "/admin/cursos/crear",
        data={"nombre": "Fisica I", "descripcion": "Mecanica clasica", "docente_id": 2},
    )
    assert resp.status_code == 302
    resp = client.get("/admin/cursos")
    assert b"Fisica I" in resp.data


def test_admin_lista_cursos(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.get("/admin/cursos")
    assert resp.status_code == 200
    assert b"Curso Test" in resp.data


def test_admin_inscribe_estudiante(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.post(
        "/admin/inscribir",
        data={"curso_id": 1, "estudiante_id": 3},
    )
    assert resp.status_code == 302
    resp = client.get("/admin/", follow_redirects=True)
    assert resp.status_code == 200


def test_admin_no_accede_como_estudiante(client):
    client.post("/login", data={"email": "estudiante@test.com", "password": "estudiante123"})
    resp = client.get("/admin/")
    assert resp.status_code == 403


def test_admin_crea_docente(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.post(
        "/admin/usuarios/crear",
        data={"nombre": "Docente Nuevo", "email": "docentenuevo@test.com", "password": "clave123", "rol": "docente"},
    )
    assert resp.status_code == 302
    resp = client.get("/admin/usuarios")
    assert b"Docente Nuevo" in resp.data


def test_admin_crea_estudiante(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    client.post(
        "/admin/usuarios/crear",
        data={"nombre": "Estudiante Nuevo", "email": "estudianuevo@test.com", "password": "clave123", "rol": "estudiante"},
    )
    resp = client.get("/admin/usuarios")
    assert b"Estudiante Nuevo" in resp.data


def test_admin_no_crea_usuario_email_duplicado(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    resp = client.post(
        "/admin/usuarios/crear",
        data={"nombre": "Duplicado", "email": "docente@test.com", "password": "clave123", "rol": "docente"},
        follow_redirects=True,
    )
    assert b"Ya existe un usuario" in resp.data


def test_usuario_recien_creado_puede_iniciar_sesion(client):
    client.post("/login", data={"email": "admin@test.com", "password": "admin123"})
    client.post(
        "/admin/usuarios/crear",
        data={"nombre": "Ana Estudiante", "email": "ana@test.com", "password": "clave123", "rol": "estudiante"},
    )
    resp = client.post("/login", data={"email": "ana@test.com", "password": "clave123"})
    assert resp.status_code == 302
    assert "/estudiante/" in resp.headers["Location"]
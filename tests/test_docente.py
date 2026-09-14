def test_docente_ve_sus_cursos(client):
    client.post("/login", data={"email": "docente@test.com", "password": "docente123"})
    resp = client.get("/docente/mis-cursos")
    assert resp.status_code == 200
    assert b"Curso Test" in resp.data


def test_docente_registra_calificacion(client):
    client.post("/login", data={"email": "docente@test.com", "password": "docente123"})
    resp = client.post(
        "/docente/calificar",
        data={"curso_id": 1, "estudiante_id": 3, "nota": 18.5},
    )
    assert resp.status_code == 302


def test_docente_no_accede_a_admin(client):
    client.post("/login", data={"email": "docente@test.com", "password": "docente123"})
    resp = client.get("/admin/cursos")
    assert resp.status_code == 403
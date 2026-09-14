def test_estudiante_ve_sus_cursos(client):
    client.post("/login", data={"email": "estudiante@test.com", "password": "estudiante123"})
    resp = client.get("/estudiante/mis-cursos")
    assert resp.status_code == 200
    assert b"Curso Test" in resp.data


def test_estudiante_ve_sus_calificaciones(client):
    client.post("/login", data={"email": "estudiante@test.com", "password": "estudiante123"})
    resp = client.get("/estudiante/mis-calificaciones")
    assert resp.status_code == 200
    assert b"15.0" in resp.data


def test_estudiante_no_accede_a_docente(client):
    client.post("/login", data={"email": "estudiante@test.com", "password": "estudiante123"})
    resp = client.get("/docente/calificar")
    assert resp.status_code == 403
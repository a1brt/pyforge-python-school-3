from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.routers.molecules import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# def test_substructure_search():
#     smile = "CCCC"

#     response = client.get("/molecules/search?smile=" + smile)
#     assert response.status_code == 200
#     assert response.json() == []

#     response = client.post("/molecules", json={"smile": smile})
#     assert response.status_code == 201
#     assert response.json()["smile"] == smile
#     smile_id = response.json()["id"]

#     response = client.get("/molecules/search?smile=" + smile)
#     assert response.status_code == 200
#     assert [s for s in response.json() if s['id'] == smile_id]


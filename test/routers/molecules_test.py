from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.routers.molecules import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

mock_molecules = [{"smile": "COO", "id": 124}, {"smile": "COC", "id": 432}]


def test_get_all_molecules(mocker):
    mocker.patch("src.routers.molecules.get_all", return_value=mock_molecules)
    response = client.get("/molecules")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(mock_molecules)

def test_search_molecules_valid_substructure(mocker):
    mock_db_call = mocker.patch(
        "src.routers.molecules.get_filtered", return_value=mock_molecules
    )
    response = client.get("/molecules/search?smile=CCO")
    print(response.json())
    assert response.status_code == 200

    data = response.json()
    assert len(data) == len(mock_molecules)
    mock_db_call.assert_called_with("CCO")
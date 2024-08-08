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


def test_valid_substructure_smile(mocker):
    mock_db_call = mocker.patch(
        "src.routers.molecules.get_filtered", return_value=mock_molecules
    )
    response = client.get("/molecules/search?smile=CCO")
    assert response.status_code == 200
    mock_db_call.assert_called_with("CCO")


def test_invalid_substructure_smile_string():
    response = client.get("/molecules/search?smile=invalid_smile")
    assert response.status_code == 422
    assert response.json()["detail"] == "'invalid_smile' is not a valid SMILES string."


def test_empty_substructure_smile():
    response = client.get("/molecules/search?smile=")
    assert response.status_code == 422
    assert response.json()["detail"] == "SMILES is not specified."


def test_substructure_search_without_smile_query_parameter():
    response = client.get("/molecules/search")
    assert response.status_code == 422
    assert response.json()["detail"] == "SMILES is not specified."

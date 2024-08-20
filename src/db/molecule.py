from random import randint

from src.utils.chem import substructure_search, valid_smile
from src.models.molecule import RequestMolecule

molecules_table = [
    {"smile": "COO", "id": 124},
    {"smile": "COC", "id": 1324},
    {"smile": "CC", "id": 24},
]


def find_by_id(id: int):
    for m in molecules_table:
        if m["id"] == id:
            return m
    return None


def find_index_by_id(id: int):
    for i, m in enumerate(molecules_table):
        if m["id"] == id:
            return i
    return -1


def delete_by_id(id: int):
    molecule = find_by_id(id)
    if molecule:
        molecules_table.remove(molecule)
        return True
    else:
        return False


def get_all():
    return molecules_table


def get_filtered(substructre: str):
    return substructure_search(molecules_table, substructre)


def create(new_molecule: RequestMolecule):
    molecule = new_molecule.model_dump()
    molecule["id"] = randint(1, 10000)  # not perfect but works for now
    molecules_table.append(molecule)
    return molecule


def update_by_id(id: int, new_molecule: RequestMolecule):
    index = find_index_by_id(id)

    if index == -1:
        return None

    molecule = new_molecule.model_dump()
    molecule["id"] = id
    molecules_table[index] = molecule
    return molecule


def create_in_bulk(smiles: list[str]):
    success = failed = 0
    created_smile_ids = []
    rejected_smiles = []

    for smile in smiles:
        if not valid_smile(smile):
            rejected_smiles.append(smile)
            failed += 1
        else:
            created_smile_ids.append(create(RequestMolecule(smile=smile))["id"])
            success += 1

    result = {
        "success": success,
        "failed": failed,
        "created_smile_ids": created_smile_ids,
        "rejected_smiles": rejected_smiles,
    }
    return result

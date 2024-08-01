from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile

from src.utils.parser import parse_text_file
from src.db.molecule import (
    get_filtered,
    get_all,
    find_by_id,
    create,
    create_in_bulk,
    update_by_id,
    delete_by_id,
)
from src.models.molecule import RequestMolecule, ResponseMolecule, UploadResponse
from src.utils.chem import valid_smile

router = APIRouter()


def valid_smile_string(
    smile: str = Query(
        ...,
        description="A SMILES string representation of a molecule",
        example="CCO",
    )
):

    if not valid_smile(smile):
        raise HTTPException(
            status_code=422, detail=f"'{smile}' is not a valid SMILES string."
        )

    return smile


@router.get(
    "",
    summary="Get all molecules",
    description="Get all molecules from db",
)
async def get_all_molecules() -> list[ResponseMolecule]:
    molecules = get_all()
    return [ResponseMolecule.model_validate(m) for m in molecules]


@router.get(
    "/search",
    summary="Get molecules by substructre",
    description="Get all molecules that contain the specified substructure",
)
async def search_molecules_by_substructure(
    substructre: str = Depends(valid_smile_string),
) -> list[ResponseMolecule]:
    filtered_molecules = get_filtered(substructre)
    return [ResponseMolecule.model_validate(m) for m in filtered_molecules]


@router.get(
    "/{molecule_id}",
    summary="Get molecule by id",
    description="Get the molecule with the specifed id",
)
async def get_molecule_by_id(molecule_id: int) -> ResponseMolecule:
    molecule = find_by_id(molecule_id)
    if not molecule:
        raise HTTPException(
            status_code=404, detail=f"Molecule not found by id: {molecule_id}"
        )
    return ResponseMolecule.model_validate(molecule)


@router.post(
    "",
    status_code=201,
    summary="Create a molecule",
    description="Create a molecule with specified SMILE",
)
async def create_molecule(request: RequestMolecule) -> ResponseMolecule:
    created_molecule = create(request)
    return ResponseMolecule.model_validate(created_molecule)


@router.post(
    "/upload",
    status_code=201,
    summary="Uploaded molecule from a file",
    description="""Upload a text file with SMILE's seperated
                   by commas to save them""",
)
async def upload_molecules(file: UploadFile) -> UploadResponse:
    file_conetnt = await parse_text_file(file)
    result = create_in_bulk(file_conetnt)

    return UploadResponse.model_validate(result)


@router.put(
    "/{molecule_id}",
    summary="Update a molecule",
    description="""Replace the molecule with specifed id with a new one
                that has the same id but new SMILE""",
)
async def update_molecule_by_id(
    molecule_id: int, request: RequestMolecule
) -> ResponseMolecule:
    updated_molecule = update_by_id(molecule_id, request)
    if not updated_molecule:
        raise HTTPException(
            status_code=404, detail=f"Molecule not found by id: {molecule_id}"
        )
    return ResponseMolecule.model_validate(updated_molecule)


@router.delete(
    "/{molecule_id}",
    status_code=204,
    summary="Delete a molecule",
    description="Delete the moleclue with the specified id",
)
async def delete_molecule_by_id(molecule_id: int):
    deleted = delete_by_id(molecule_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail=f"Molecule not found by id: {molecule_id}"
        )

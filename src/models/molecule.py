from pydantic import BaseModel, ValidationInfo, Field, field_validator

from src.utils.chem import valid_smile


class BaseMolecule(BaseModel):
    smile: str = Field(example="COO")

    @field_validator("smile")
    def check_valid_smile(cls, v: str, info: ValidationInfo):
        if not valid_smile(v):
            raise ValueError(f"'{v}' is not a valid SMILES string.")
        return v


class RequestMolecule(BaseMolecule):
    pass


class ResponseMolecule(BaseMolecule):
    id: int = Field(example=1324)


class UploadResponse(BaseModel):
    failed: int = Field(example=2)
    success: int = Field(example=3)
    rejected_smiles: list[str] = Field(examples=[["not-a-smile", "CC.O"]])
    created_smile_ids: list[int] = Field(examples=[[1324, 2246, 7894]])

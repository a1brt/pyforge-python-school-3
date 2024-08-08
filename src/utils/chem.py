from rdkit import Chem


def substructure_search(mols, mol):
    chem_mol = Chem.MolFromSmiles(mol)
    return [
        m for m in mols if Chem.MolFromSmiles(m["smile"]).HasSubstructMatch(chem_mol)
    ]


def valid_smile(s: str):
    if not isinstance(s, str):
        return False

    mol = Chem.MolFromSmiles(s)
    if mol is None:
        return False
    return True


if __name__ == "__main__":
    pass

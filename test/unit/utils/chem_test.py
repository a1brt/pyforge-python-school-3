import pytest
from src.utils.chem import substructure_search, valid_smile


mols = [
    {"smile": "CCO"},
    {"smile": "C1CCCCC1"},
    {"smile": "CCN"},
    {"smile": "CCOCC"},
]


@pytest.mark.parametrize(
    "smile, expected",
    [
        ("CCO", True),
        ("C1CCCCC1", True),
        ("nothing", False),
        ("C1CCC3000CC1", False),
        (1, False),
        (None, False),
    ],
)
def test_valid_smile(smile, expected):
    assert (
        valid_smile(smile) == expected
    ), f"{smile} is expected to be {'valid' if expected else 'invalid'} SMILES"


@pytest.mark.parametrize(
    "query, expected",
    [
        ("C1CCCCC1", [{"smile": "C1CCCCC1"}]),
        ("CCO", [{"smile": "CCO"}, {"smile": "CCOCC"}]),
        ("CNC", []),
    ],
)
def test_substructure_search(query, expected):
    result = substructure_search(mols, query)
    assert result == expected, f"Expected {expected}, but got {result}"

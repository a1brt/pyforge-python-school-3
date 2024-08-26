from sqlalchemy.orm import Mapped
from src.db.database import Base, str_uniq, int_pk


class Molecule(Base):
    id: Mapped[int_pk]
    smile: Mapped[str_uniq]

    def to_dict(self):
        return {
            "id": self.id,
            "smile": self.smile,
        }

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"smile={self.smiles!r})"
        )

    def __repr__(self):
        return str(self)

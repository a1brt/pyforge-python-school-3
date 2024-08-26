from sqlalchemy import delete
from sqlalchemy.future import select
from src.models.db_models import Molecule
from src.db.database import async_session_maker
from src.dao.base import BaseDAO


class MoleculeDAO(BaseDAO):
    model = Molecule

    @classmethod
    async def find_all_molecules(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            molecules = await session.execute(query)
            return molecules.scalars().all()

    @classmethod
    async def find_full_data(cls, molecule_id):
        async with async_session_maker() as session:
            # Query to get molecule info
            query = select(cls.model).filter_by(id=molecule_id)
            result = await session.execute(query)
            molecule_info = result.scalar_one_or_none()

            # If Molecule is not found, return None
            if not molecule_info:
                return None

            molecule_data = molecule_info.to_dict()
            return molecule_data

    @classmethod
    async def add_molecule(cls, **molecule_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_molecule = cls.model(**molecule_data)
                session.add(new_molecule)
                await session.flush()
                new_molecule_id = new_molecule.id
                await session.commit()
                return new_molecule_id

    @classmethod
    async def delete_molecule_by_id(cls, molecule_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=molecule_id)
                result = await session.execute(query)
                molecule_to_delete = result.scalar_one_or_none()

                if not molecule_to_delete:
                    return None

                # Delete the molecule
                await session.execute(delete(cls.model).filter_by(id=molecule_id))

                await session.commit()
                return molecule_id

from openai.types.beta.realtime import Session

from app.repositories.character_repo import CharacterRepository
from app.schemas.character import CharacterCreate


class CharacterService:
    def __init__(self, repo: CharacterRepository):
        self.repo = repo

    def create_character(self, db: Session, data: CharacterCreate):
        return self.repo.create_character(
            db,
            data
        )

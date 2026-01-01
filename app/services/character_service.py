from openai.types.beta.realtime import Session

from app.persona.builder import PersonaBuilder
from app.repositories.character_repo import CharacterRepository
from app.schemas.character import CharacterCreate


class CharacterService:
    def __init__(self, repo: CharacterRepository):
        self.repo = repo

    def create_character(self, db: Session, data: CharacterCreate):
        persona = PersonaBuilder.apply_tags(data.tags)
        return self.repo.create_character(
            db,
            name=data.name,
            avatar=data.avatar,
            description=data.description,
            worldview=data.worldview,
            persona=persona

        )

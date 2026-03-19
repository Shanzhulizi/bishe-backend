from app.repositories.conversation_repo import ConversationRepository


class ConversationService:
    def __init__(self, db):
        self.db = db
        self.conv_repo = ConversationRepository(db)

    async def get_conv(self, user_id, character_id):
        conv = await self.conv_repo.get_active(user_id=user_id, character_id=character_id)
        return conv

    async def create_conv(self, user_id, character_id):
        conv = await self.conv_repo.create(user_id=user_id, character_id=character_id)
        return conv

from sqlalchemy import Column, BigInteger, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base  # declarative_base

class Character(Base):
    __tablename__ = "character"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    worldview = Column(Text, nullable=True)
    speech_style = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联角色配置
    config = relationship(
        "CharacterConfigs",
        uselist=False,
        back_populates="character",
        cascade="all, delete-orphan"
    )

from datetime import datetime
from sqlalchemy import UUID, Boolean, Column, DateTime, Integer, String, Text
from database import Base


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    email = Column(String(64), default=None)
    password = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, default=datetime.now)
    token = Column(Text, nullable=False)
    is_verified = Column(Boolean, default=False)

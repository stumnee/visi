from sqlalchemy import Column, Integer, String, DateTime, JSON

from api.core.database import Base


class Event(Base):
    """Event model for database.

    Attributes:
        id: Unique identifier
        name: Event name
        value: Event Value
        createdAt: Timestamp
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    value = Column(JSON, nullable=True)
    createdAt = Column(DateTime)

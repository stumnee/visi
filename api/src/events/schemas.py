from pydantic import BaseModel, ConfigDict, Field, Json


class EventBase(BaseModel):
    """Base schema for Event data.

    Attributes:
        name: Event name
        value: Event JSON Value
    """

    name: str = Field(..., min_length=1, max_length=100, description="Event name")
    value: dict = Field({}, description="Event value")


class EventCreate(EventBase):
    """Schema for creating a new event."""


class EventUpdate(BaseModel):
    """Schema for updating an existing event.

    All fields are optional since updates might be partial.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    powers: str | None = None


class EventResponse(EventBase):
    """Schema for event responses.

    Includes all base fields plus the id.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int

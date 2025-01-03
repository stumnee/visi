from api.src.events.repository import EventRepository
from api.src.events.schemas import EventCreate, EventResponse, EventUpdate


class EventService:
    """Service layer for event operations."""

    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def create_event(self, event_data: EventCreate) -> EventResponse:
        """Create a new event.

        Args:
            event_data: Event creation data

        Returns:
            EventResponse: Created event data
        """
        event = await self.repository.create(event_data)
        return EventResponse.model_validate(event)

    async def get_event(self, event_id: int) -> EventResponse:
        """Get event by ID.

        Args:
            event_id: Event ID

        Returns:
            EventResponse: Event data
        """
        event = await self.repository.get_by_id(event_id)
        return EventResponse.model_validate(event)

    async def get_all_events(self) -> list[EventResponse]:
        """Get all events.

        Returns:
            List[EventResponse]: List of all events
        """
        events = await self.repository.get_all()
        return [EventResponse.model_validate(event) for event in events]

    async def update_event(self, event_id: int, event_data: EventUpdate) -> EventResponse:
        """Update event by ID.

        Args:
            event_id: Event ID
            event_data: Event update data

        Returns:
            EventResponse: Updated event data
        """
        event = await self.repository.update(event_id, event_data)
        return EventResponse.model_validate(event)

    async def delete_event(self, event_id: int) -> None:
        """Delete event by ID.

        Args:
            event_id: Event ID
        """
        await self.repository.delete(event_id)

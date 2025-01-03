from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.exceptions import AlreadyExistsException, NotFoundException
from api.src.events.models import Event
from api.src.events.schemas import EventCreate, EventUpdate


class EventRepository:
    """Repository for handling event database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_data: EventCreate) -> Event:
        """Create a new event.

        Args:
            event_data: Event creation data

        Returns:
            Event: Created event

        Raises:
            AlreadyExistsException: If event with same alias already exists
        """
        event = Event(**event_data.model_dump())
        try:
            self.session.add(event)
            await self.session.commit()
            await self.session.refresh(event)
            return event
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsException(
                f"Event with alias {event_data.alias} already exists"
            )

    async def get_by_id(self, event_id: int) -> Event:
        """Get event by ID.

        Args:
            event_id: Event ID

        Returns:
            Event: Found event

        Raises:
            NotFoundException: If event not found
        """
        query = select(Event).where(Event.id == event_id)
        result = await self.session.execute(query)
        event = result.scalar_one_or_none()

        if not event:
            raise NotFoundException(f"Event with id {event_id} not found")
        return event

    async def get_all(self) -> list[Event]:
        """Get all events.

        Returns:
            List[Event]: List of all events
        """
        query = select(Event)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, event_id: int, event_data: EventUpdate) -> Event:
        """Update event by ID.

        Args:
            event_id: Event ID
            event_data: Event update data

        Returns:
            Event: Updated event

        Raises:
            NotFoundException: If event not found
        """
        update_data = event_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields to update")

        query = update(Event).where(Event.id == event_id).values(**update_data)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Event with id {event_id} not found")

        await self.session.commit()
        return await self.get_by_id(event_id)

    async def delete(self, event_id: int) -> None:
        """Delete event by ID.

        Args:
            event_id: Event ID

        Raises:
            NotFoundException: If event not found
        """
        query = delete(Event).where(Event.id == event_id)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Event with id {event_id} not found")

        await self.session.commit()

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.logging import get_logger
from api.core.security import get_current_user
from api.src.events.repository import EventRepository
from api.src.events.schemas import EventCreate, EventResponse, EventUpdate
from api.src.events.service import EventService
from api.src.users.models import User

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


def get_event_service(session: AsyncSession = Depends(get_session)) -> EventService:
    """Dependency for getting event service instance."""
    repository = EventRepository(session)
    return EventService(repository)


@router.get("/", response_model=list[EventResponse])
async def get_all_events(
    service: EventService = Depends(get_event_service),
    current_user: User = Depends(get_current_user),
) -> list[EventResponse]:
    """Get all events."""
    logger.debug("Fetching all events")
    try:
        events = await service.get_all_events()
        logger.info(f"Retrieved {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Failed to fetch events: {str(e)}")
        raise


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    service: EventService = Depends(get_event_service),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """Get event by ID."""
    logger.debug(f"Fetching event {event_id}")
    try:
        event = await service.get_event(event_id)
        logger.info(f"Retrieved event {event_id}")
        return event
    except Exception as e:
        logger.error(f"Failed to fetch event {event_id}: {str(e)}")
        raise


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    service: EventService = Depends(get_event_service),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """Create a new event."""
    logger.debug("Creating new event")
    try:
        event = await service.create_event(event_data)
        logger.info(f"Created event {event.id}")
        return event
    except Exception as e:
        logger.error(f"Failed to create event: {str(e)}")
        raise


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    service: EventService = Depends(get_event_service),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """Update event by ID."""
    logger.debug(f"Updating event {event_id}")
    try:
        event = await service.update_event(event_id, event_data)
        logger.info(f"Updated event {event_id}")
        return event
    except Exception as e:
        logger.error(f"Failed to update event {event_id}: {str(e)}")
        raise


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    service: EventService = Depends(get_event_service),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete event by ID."""
    logger.debug(f"Deleting event {event_id}")
    try:
        await service.delete_event(event_id)
        logger.info(f"Deleted event {event_id}")
    except Exception as e:
        logger.error(f"Failed to delete event {event_id}: {str(e)}")
        raise

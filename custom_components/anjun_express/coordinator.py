"""DataUpdateCoordinator for Anjun Express."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.persistent_notification import async_create
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AnjunExpressApiClientError
from .const import CONF_PACKAGE_NAME, CONF_TRACKING_NUMBER

if TYPE_CHECKING:
    from .data import AnjunExpressConfigEntry


class AnjunExpressDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: AnjunExpressConfigEntry
    _previous_data: dict[str, Any] | None = None

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            new_data = await (
                self.config_entry.runtime_data.client.async_get_tracking_data()
            )
        except AnjunExpressApiClientError as exception:
            raise UpdateFailed(exception) from exception
        else:
            # Check for updates and create notifications
            await self._check_for_updates(new_data)

            # Store current data as previous for next comparison
            self._previous_data = new_data.copy() if new_data else None

            return new_data

    async def _check_for_updates(self, new_data: dict[str, Any]) -> None:
        """Check for updates and create persistent notifications."""
        if not new_data or not self._previous_data:
            return

        # Get shipping events from both old and new data
        old_events = self._previous_data.get("shippingCompany", [])
        new_events = new_data.get("shippingCompany", [])

        if not new_events:
            return

        # Check if there are new events (more events than before)
        if len(new_events) > len(old_events):
            latest_event = new_events[0]  # First event is the latest

            package_name = self.config_entry.data[CONF_PACKAGE_NAME]
            tracking_number = self.config_entry.data[CONF_TRACKING_NUMBER]

            # Create persistent notification
            await self._create_update_notification(
                package_name=package_name,
                tracking_number=tracking_number,
                status=latest_event.get("status", "Unknown status"),
                location=latest_event.get("address", "Unknown location"),
                date=latest_event.get("date", ""),
            )

    async def _create_update_notification(
        self,
        package_name: str,
        tracking_number: str,
        status: str,
        location: str,
        date: str,
    ) -> None:
        """Create a persistent notification for package updates."""
        # Create notification ID following similar pattern
        clean_package_name = package_name.lower().replace(" ", "_")
        clean_tracking = tracking_number.lower()
        notification_id = f"anjun_{clean_package_name}_{clean_tracking}_update"

        title = f"📦 Package Update: {package_name}"

        message = f"""**Status:** {status}
**Location:** {location}
**Tracking:** {tracking_number}
**Updated:** {date}

Your package has a new tracking update!"""

        async_create(
            hass=self.hass,
            message=message,
            title=title,
            notification_id=notification_id,
        )

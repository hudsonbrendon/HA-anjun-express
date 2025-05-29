"""DataUpdateCoordinator for Anjun Express."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AnjunExpressApiClientError

if TYPE_CHECKING:
    from .data import AnjunExpressConfigEntry


class AnjunExpressDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: AnjunExpressConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_tracking_data()
        except AnjunExpressApiClientError as exception:
            raise UpdateFailed(exception) from exception

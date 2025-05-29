"""
Custom integration to integrate Anjun Express with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom/anjun-express
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import AnjunExpressApiClient
from .const import (
    CONF_TRACKING_NUMBER,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    LOGGER,
)
from .coordinator import AnjunExpressDataUpdateCoordinator
from .data import AnjunExpressData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import AnjunExpressConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AnjunExpressConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = AnjunExpressDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=DEFAULT_UPDATE_INTERVAL),
    )
    entry.runtime_data = AnjunExpressData(
        client=AnjunExpressApiClient(
            tracking_number=entry.data[CONF_TRACKING_NUMBER],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AnjunExpressConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: AnjunExpressConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

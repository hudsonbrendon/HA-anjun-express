"""AnjunExpressEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    CONF_PACKAGE_NAME,
    CONF_TRACKING_NUMBER,
)
from .coordinator import AnjunExpressDataUpdateCoordinator


class AnjunExpressEntity(CoordinatorEntity[AnjunExpressDataUpdateCoordinator]):
    """AnjunExpressEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: AnjunExpressDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

        # Get package info for naming
        package_name = coordinator.config_entry.data[CONF_PACKAGE_NAME]
        tracking_number = coordinator.config_entry.data[CONF_TRACKING_NUMBER]

        # Create device name following pattern
        device_name = f"Anjun {package_name} ({tracking_number})"

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=device_name,
            manufacturer="Anjun Express",
            model=f"Package Tracking - {tracking_number}",
        )

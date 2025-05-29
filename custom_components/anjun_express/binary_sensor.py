"""Binary sensor platform for Anjun Express."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import AnjunExpressEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AnjunExpressDataUpdateCoordinator
    from .data import AnjunExpressConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="delivered",
        name="Delivered",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:package-check",
    ),
)

# Status messages that indicate delivery
DELIVERY_STATUSES = [
    "entregue",
    "delivered",
    "objeto entregue",
    "entrega realizada",
    "package delivered",
]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AnjunExpressConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        AnjunExpressBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AnjunExpressBinarySensor(AnjunExpressEntity, BinarySensorEntity):
    """Anjun Express binary_sensor class."""

    def __init__(
        self,
        coordinator: AnjunExpressDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the package is delivered."""
        if not self.coordinator.data or "shippingCompany" not in self.coordinator.data:
            return False

        shipping_events = self.coordinator.data.get("shippingCompany", [])
        if not shipping_events:
            return False

        # Check if any event indicates delivery
        for event in shipping_events:
            status = event.get("status", "").lower()
            if any(delivery_status in status for delivery_status in DELIVERY_STATUSES):
                return True

        return False

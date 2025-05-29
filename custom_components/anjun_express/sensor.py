"""Sensor platform for Anjun Express."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import EntityCategory

from .entity import AnjunExpressEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AnjunExpressDataUpdateCoordinator
    from .data import AnjunExpressConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="current_status",
        name="Current Status",
        icon="mdi:package-variant",
    ),
    SensorEntityDescription(
        key="current_location",
        name="Current Location",
        icon="mdi:map-marker",
    ),
    SensorEntityDescription(
        key="last_update",
        name="Last Update",
        icon="mdi:clock",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="tracking_events",
        name="Tracking Events",
        icon="mdi:format-list-bulleted",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AnjunExpressConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        AnjunExpressSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AnjunExpressSensor(AnjunExpressEntity, SensorEntity):
    """Anjun Express Sensor class."""

    def __init__(
        self,
        coordinator: AnjunExpressDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def native_value(self) -> str | datetime | None:
        """Return the native value of the sensor."""
        if not self.coordinator.data or "shippingCompany" not in self.coordinator.data:
            return None

        shipping_events = self.coordinator.data.get("shippingCompany", [])
        if not shipping_events:
            return None

        latest_event = shipping_events[0]  # First event is the latest

        value_map = {
            "current_status": latest_event.get("status"),
            "current_location": latest_event.get("address"),
            "tracking_events": len(shipping_events),
        }

        if self.entity_description.key in value_map:
            return value_map[self.entity_description.key]

        if self.entity_description.key == "last_update":
            date_str = latest_event.get("date")
            if date_str:
                try:
                    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except ValueError:
                    return None

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes."""
        if not self.coordinator.data:
            return None

        attributes = {}

        if self.entity_description.key == "tracking_events":
            events = self.coordinator.data.get("shippingCompany", [])
            attributes["events"] = [
                {
                    "date": event.get("date"),
                    "status": event.get("status"),
                    "location": event.get("address"),
                    "remark": event.get("remark"),
                }
                for event in events
            ]

        # Add collection order info if available
        collect_order = self.coordinator.data.get("clCollectOrder", {})
        if collect_order and any(collect_order.values()):
            attributes["collection_info"] = collect_order

        return attributes if attributes else None

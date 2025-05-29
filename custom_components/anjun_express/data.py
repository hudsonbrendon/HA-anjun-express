"""Custom types for Anjun Express."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import AnjunExpressApiClient
    from .coordinator import AnjunExpressDataUpdateCoordinator


type AnjunExpressConfigEntry = ConfigEntry[AnjunExpressData]


@dataclass
class AnjunExpressData:
    """Data for the Anjun Express integration."""

    client: AnjunExpressApiClient
    coordinator: AnjunExpressDataUpdateCoordinator
    integration: Integration

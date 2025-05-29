"""Adds config flow for Anjun Express."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    AnjunExpressApiClient,
    AnjunExpressApiClientCommunicationError,
    AnjunExpressApiClientError,
    AnjunExpressApiClientTrackingNotFoundError,
)
from .const import CONF_PACKAGE_NAME, CONF_TRACKING_NUMBER, DOMAIN, LOGGER


class AnjunExpressFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Anjun Express."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_tracking_number(
                    tracking_number=user_input[CONF_TRACKING_NUMBER],
                )
            except AnjunExpressApiClientTrackingNotFoundError:
                LOGGER.warning("Tracking number not found")
                _errors["base"] = "tracking_not_found"
            except AnjunExpressApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except AnjunExpressApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    unique_id=user_input[CONF_TRACKING_NUMBER].upper()
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_PACKAGE_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_TRACKING_NUMBER,
                        default=(user_input or {}).get(
                            CONF_TRACKING_NUMBER, vol.UNDEFINED
                        ),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_PACKAGE_NAME,
                        default=(user_input or {}).get(
                            CONF_PACKAGE_NAME, vol.UNDEFINED
                        ),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_tracking_number(self, tracking_number: str) -> None:
        """Validate tracking number."""
        client = AnjunExpressApiClient(
            tracking_number=tracking_number,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_tracking_data()

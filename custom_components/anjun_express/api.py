"""Anjun Express API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import API_BASE_URL, API_TRACKING_ENDPOINT

# HTTP status codes
HTTP_NOT_FOUND = 404


class AnjunExpressApiClientError(Exception):
    """Exception to indicate a general API error."""


class AnjunExpressApiClientCommunicationError(AnjunExpressApiClientError):
    """Exception to indicate a communication error."""


class AnjunExpressApiClientTrackingNotFoundError(AnjunExpressApiClientError):
    """Exception to indicate tracking number not found."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status == HTTP_NOT_FOUND:
        msg = "Tracking number not found"
        raise AnjunExpressApiClientTrackingNotFoundError(msg)
    response.raise_for_status()


class AnjunExpressApiClient:
    """Anjun Express API Client."""

    def __init__(
        self,
        tracking_number: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API Client."""
        self._tracking_number = tracking_number
        self._session = session

    async def async_get_tracking_data(self) -> dict[str, Any]:
        """Get tracking data from the API."""
        return await self._api_wrapper(
            method="get",
            url=f"{API_BASE_URL}{API_TRACKING_ENDPOINT}",
            params={"trackingNumber": self._tracking_number},
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "dnt": "1",
                "origin": "https://anjunexpress.com.br",
                "priority": "u=1, i",
                "referer": "https://anjunexpress.com.br/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 "
                    "Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
                ),
            },
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AnjunExpressApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AnjunExpressApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AnjunExpressApiClientError(msg) from exception

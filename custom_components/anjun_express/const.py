"""Constants for Anjun Express."""

import re
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "anjun_express"
ATTRIBUTION = "Data provided by Anjun Express"

# Configuration constants
CONF_TRACKING_NUMBER = "tracking_number"
CONF_PACKAGE_NAME = "package_name"

# API constants
API_BASE_URL = "https://website-trackings.anjunexpress.com.br"
API_TRACKING_ENDPOINT = "/tracking/get-tracking"

# Update interval
DEFAULT_UPDATE_INTERVAL = 30  # minutes


def create_entity_id(
    tracking_number: str, sensor_type: str
) -> str:
    """
    Create standardized entity ID.

    Following pattern: anjun_nome_do_pacote_codigo_do_pacote_sensor_type.
    """

    # Clean tracking number: remove special chars, convert to lowercase
    clean_tracking_number = re.sub(r"[^a-zA-Z0-9]", "", tracking_number.lower())

    # Create entity ID
    return f"anjun_{clean_tracking_number}_{sensor_type}"

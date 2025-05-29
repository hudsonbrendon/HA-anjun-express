"""Constants for Anjun Express."""

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

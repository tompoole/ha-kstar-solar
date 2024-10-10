"""KStar Integration Data Coordinator."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import KStarClient

_LOGGER = logging.getLogger(__name__)


class KstarInverterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Inverter API."""

    def __init__(self, hass: HomeAssistant, api: KStarClient, name: str) -> None:
        """Initialize the data updater."""

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=name,
            update_interval=timedelta(seconds=60),
        )

        self.api = api

    async def _async_update_data(self):
        """Fetch the data from the inverter."""
        try:
            return self.api.get_latest_data()
        except TimeoutError as err:
            raise UpdateFailed("Error communicating with Solar Inverter") from err

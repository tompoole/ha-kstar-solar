"""The KStar Solar Inverter integration."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant

from .client import KStarClient
from .coordinator import KstarInverterDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]


@dataclass
class KStarConfigData:
    """Data for KStar Solar Inverter config."""

    coordinator: KstarInverterDataUpdateCoordinator


type KStarConfigEntry = ConfigEntry[KStarConfigData]


async def async_setup_entry(hass: HomeAssistant, entry: KStarConfigEntry) -> bool:
    """Set up KStar Solar Inverter from a config entry."""

    hostAddress = entry.data[CONF_HOST]
    api = KStarClient(hostAddress)
    coordinator = KstarInverterDataUpdateCoordinator(hass, api, hostAddress)
    entry.runtime_data = KStarConfigData(coordinator=coordinator)

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

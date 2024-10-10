"""KSTAR Sensor Platform."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KStarConfigEntry
from .const import DOMAIN
from .coordinator import KstarInverterDataUpdateCoordinator

__LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class KStarSensorDescription(SensorEntityDescription):
    """Class describing KStar Solar Inverter sensor entities."""

    value_fn: Callable[[dict[str, Any]], str | int | float | None]


entityDescriptions = [
    KStarSensorDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        name="Temperature",
        value_fn=lambda data: data["stats"]["temperature"],
    ),
    KStarSensorDescription(
        key="energy_today",
        name="Energy Today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data["stats"]["energy_today"],
    ),
    KStarSensorDescription(
        key="energy_total",
        name="Energy Total",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda data: data["stats"]["energy_total"],
    ),
    KStarSensorDescription(
        key="pv_power",
        name="PV Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        value_fn=lambda data: data["pv"]["power"],
    ),
    KStarSensorDescription(
        key="grid_power",
        name="Grid Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        value_fn=lambda data: data["grid"]["power"],
    ),
    KStarSensorDescription(
        key="load_power",
        name="Load Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        value_fn=lambda data: data["load"]["power"],
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KStarConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the KSTAR sensor platform."""

    __LOGGER.info("Creating KSTAR sensors")

    coordinator = entry.runtime_data.coordinator

    entities: list[KStarSensor] = [
        KStarSensor(coordinator, description) for description in entityDescriptions
    ]

    async_add_entities(entities, True)


class KStarSensor(CoordinatorEntity[KstarInverterDataUpdateCoordinator], SensorEntity):
    """Implementation of the base."""

    def __init__(
        self,
        coordinator: KstarInverterDataUpdateCoordinator,
        description: KStarSensorDescription,
    ) -> None:
        """Initialize the Kstar Entity."""
        super().__init__(coordinator=coordinator)

        self.entity_description = description
        self.entity_id = f"{DOMAIN}.solar_inverter_{description.key}"
        self._attr_unique_id = (f"solar_inverter_{description.key}").lower()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from Coordinator."""
        self._attr_native_value = self.entity_description.value_fn(
            self.coordinator.data
        )
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Define the device based on name."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.name)},
            manufacturer="KStar",
            model="Solar Inverter",
            name=self.coordinator.name,
        )

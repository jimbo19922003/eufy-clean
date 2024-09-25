# vacuum.py

import logging

from homeassistant.components.vacuum import (
    SUPPORT_BATTERY,
    SUPPORT_CLEAN_SPOT,
    SUPPORT_PAUSE,
    SUPPORT_RETURN_HOME,
    SUPPORT_START,
    SUPPORT_STATUS,
    SUPPORT_STOP,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_IDLE,
    STATE_PAUSED,
    STATE_RETURNING,
    VacuumEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Eufy Clean vacuums."""
    client = hass.data[DOMAIN][entry.entry_id]

    devices = await client.getAllDevices()

    entities = []
    for device_info in devices:
        device_id = device_info["deviceId"]
        nickname = device_info["nickName"]
        device = await client.initDevice({"deviceId": device_id})
        entity = EufyVacuum(device, nickname)
        entities.append(entity)

    async_add_entities(entities, update_before_add=True)

class EufyVacuum(VacuumEntity):
    """Representation of a Eufy Clean vacuum."""

    def __init__(self, device, name):
        """Initialize the vacuum."""
        self._device = device
        self._name = name
        self._status = None
        self._battery = None

    @property
    def name(self):
        """Return the name of the vacuum."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._device.device.get("deviceId")

    @property
    def supported_features(self):
        """Flag supported features."""
        return (
            SUPPORT_START
            | SUPPORT_STOP
            | SUPPORT_PAUSE
            | SUPPORT_RETURN_HOME
            | SUPPORT_BATTERY
            | SUPPORT_STATUS
        )

    @property
    def state(self):
        """Return the state of the vacuum."""
        status_mapping = {
            "RUNNING": STATE_CLEANING,
            "CHARGING": STATE_DOCKED,
            "PAUSED": STATE_PAUSED,
            "RETURNING": STATE_RETURNING,
            "IDLE": STATE_IDLE,
            # Add other status mappings as needed
        }
        return status_mapping.get(self._status, STATE_IDLE)

    @property
    def battery_level(self):
        """Return the battery level of the vacuum."""
        return self._battery

    async def async_update(self):
        """Fetch the latest state."""
        await self._device.connect()
        status = await self._device.get_status()
        self._status = status.get("state")
        self._battery = status.get("battery")

    async def async_start(self):
        """Start cleaning."""
        await self._device.start()
        await self.async_update()

    async def async_stop(self, **kwargs):
        """Stop cleaning."""
        await self._device.stop()
        await self.async_update()

    async def async_pause(self):
        """Pause cleaning."""
        await self._device.pause()
        await self.async_update()

    async def async_return_to_base(self, **kwargs):
        """Return to base."""
        await self._device.goHome()
        await self.async_update()

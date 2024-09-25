# __init__.py

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Eufy Clean integration."""
    # We don't support YAML configuration
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Eufy Clean from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    email = entry.data.get("email")
    password = entry.data.get("password")

    # Import the SDK
    from .eufyclean.eufy_clean import EufyClean

    # Initialize the client
    client = EufyClean(email, password)
    await client.init()

    hass.data[DOMAIN][entry.entry_id] = client

    # Forward entry setup to platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Unload platforms
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    # Remove data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "eufy_clean"

PLATFORMS = ["vacuum"]  # Or other platforms you'll implement

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eufy Clean from a config entry."""

    hass.data[DOMAIN][entry.entry_id] = entry.data  # Store the config data

    for platform in PLATFORMS:
        hass.async_create_task(hass.config_entries.async_setup_platform(entry, platform))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

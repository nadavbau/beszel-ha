import asyncio
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_URL, CONF_USERNAME, CONF_PASSWORD, UPDATE_INTERVAL, LOGGER
from .api import BeszelApiClient

PLATFORMS = ["sensor", "binary_sensor"]

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})

    url = entry.data[CONF_URL]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    client = BeszelApiClient(url, username, password)
    client.login()

    async def async_update_data():
        try:
            return await hass.async_add_executor_job(client.get_systems)
        except Exception as err:
            raise UpdateFailed(f"Error fetching systems: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name="Beszel API",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

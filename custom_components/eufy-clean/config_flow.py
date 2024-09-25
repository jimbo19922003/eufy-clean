# config_flow.py

import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

class EufyCleanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eufy Clean."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            # Validate the credentials
            if await self._test_credentials(email, password):
                # Create entry
                return self.async_create_entry(
                    title=email,
                    data={
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,
                    },
                )
            else:
                errors["base"] = "invalid_auth"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def _test_credentials(self, email, password):
        """Return true if credentials are valid."""
        try:
            from .eufyclean.eufy_clean import EufyClean
            client = EufyClean(email, password)
            await client.init()
            return True
        except Exception as ex:
            _LOGGER.error("Authentication failed: %s", ex)
            return False

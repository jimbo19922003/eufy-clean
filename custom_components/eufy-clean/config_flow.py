import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

DOMAIN = "eufy_clean"

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

class EufyCleanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Validate credentials (you'll need to implement this)
            # ...

            return self.async_create_entry(title="Eufy Clean", data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

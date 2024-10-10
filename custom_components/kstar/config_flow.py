"""Config flow for KSTAR inverter."""

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST

from .const import DOMAIN


class KStarInverterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Return the config steps."""
        if user_input is not None:
            host = user_input[CONF_HOST]
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=host, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({vol.Required("host"): str})
        )

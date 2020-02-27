"""
Lutron RadioRA Classic support for Home Assistant
See https://github.com/rsnodgrass/hass-radiora-classic
"""
import logging

from pyradiora_classic import get_async_radiora_controller

import voluptuous as vol

from homeassistant.const import CONF_HOST
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

LOG = logging.getLogger(__name__)

RADIORA_CLASSIC = "radiora_classic"

DOMAIN = "radiora_classic"

CONF_PORT = 'port'
CONF_DIMMERS = 'dimmers'
CONF_SWITCHES = 'switches'

# FIXME: allow multiple bridges?
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PORT): cv.string,
                vol.Optional(CONF_SWITCHES): cv.string,
                vol.Optional(CONF_DIMMERS): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

RADIORA_CLASSIC_COMPONENTS = [ "light" ]

async def async_setup(hass, base_config):
    """Set up the Lutron component."""

    tty = base_config.get(DOMAIN)

    radiora = get_async_radiora_controller(tty, hass.loop)
    if not radiora:
        LOG.error("Unable to connect to RadioRA Classic Smart Bridge at %s", tty)
        return False

    hass.data[RADIORA_CLASSIC] = radiora

#    for component in LUTRON_CASETA_COMPONENTS:
#        hass.async_create_task(
#            discovery.async_load_platform(hass, component, DOMAIN, {}, config)
#        )

    return True

class RadioRAClassicDevice(Entity):
    """Common base class for all Lutron RadioRA Classic devices."""

    def __init__(self, device, radiora):
        """Set up the base class.

        [:param]device the device metadata
        [:param]radiora the RadioRA controller
        """
        self._device = device
        self._radiora = radiora
        self._zone = 1
        self._system = 1

    async def async_added_to_hass(self):
        """Register callbacks."""
    #    self._radiora.add_subscriber(
    #        self.device_id, self.async_schedule_update_ha_state
    #    )
        return

    @property
    def device_id(self):
        """Return the device ID used for calling pylutron_caseta."""
        return self._device["device_id"]

    @property
    def name(self):
        """Return the name of the device."""
        return self._device["name"]

    @property
    def serial(self):
        """Return the serial number of the device."""
        return self._device["serial"]

    @property
    def unique_id(self):
        """Return the unique ID of the device (serial)."""
        return str(self.serial)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        return attr

    @property
    def should_poll(self):
        """No polling needed."""
        return False

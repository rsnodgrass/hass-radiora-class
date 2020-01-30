"""
Lutron RadioRA Classic support for Home Assistant
See https://github.com/rsnodgrass/hass-radiora-classic
"""
import logging

#from pylutron_caseta.smartbridge import Smartbridge
import voluptuous as vol

from homeassistant.const import CONF_HOST
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

LOG = logging.getLogger(__name__)

RADIORA_CLASSIC_SMARTBRIDGE = "radiora_classic_bridge"

DOMAIN = "lutron_radiora_classic"

# FIXME: allow multiple bridges?
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

RADIORA_CLASSIC_COMPONENTS = ["light", "switch"]

async def async_setup(hass, base_config):
    """Set up the Lutron component."""

    config = base_config.get(DOMAIN)
    keyfile = hass.config.path(config[CONF_KEYFILE])
    hostname=config[CONF_HOST],

    hass.data[RADIORA_CLASSIC_SMARTBRIDGE] = bridge
    await bridge.connect()
    if not hass.data[RADIORA_CLASSIC_SMARTBRIDGE].is_connected():
        LOG.error(
            "Unable to connect to RadioRA Classic Smart Bridge at %s", config[CONF_HOST]
        )
        return False

    LOG.info("Connected to RadioRA Classic Smart Bridge at %s", config[CONF_HOST])

    for component in LUTRON_CASETA_COMPONENTS:
        hass.async_create_task(
            discovery.async_load_platform(hass, component, DOMAIN, {}, config)
        )

    return True

class RadioRAClassicDevice(Entity):
    """Common base class for all Lutron RadioRA Classic devices."""

    def __init__(self, device, bridge):
        """Set up the base class.

        [:param]device the device metadata
        [:param]bridge the smartbridge object
        """
        self._device = device
        self._smartbridge = bridge

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._smartbridge.add_subscriber(
            self.device_id, self.async_schedule_update_ha_state
        )

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
        attr = {"Device ID": self.device_id, "Zone ID": self._device["zone"]}
        return attr

    @property
    def should_poll(self):
        """No polling needed."""
        return False

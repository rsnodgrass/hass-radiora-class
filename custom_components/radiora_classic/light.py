"""Support for Lutron RadioRA Classic lights."""
import logging

from homeassistant.components.light import (
    DOMAIN,
    SUPPORT_BRIGHTNESS,
    Light,
)
from homeassistant.components.lutron.light import to_hass_level, to_lutron_level

from . import LUTRON_RADIORA_CLASSIC, RadioRAClassicDevice

LOG = logging.getLogger(__name__)

DEFAULT_BRIGHTNESS = 100

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Lutron RadioRA Classic lights."""
    radiora = hass.data[LUTRON_RADIORA_CLASSICE]

    devices = []
#    for light_device in light_devices:
#        zone = 1
#        devices.append(LutronCasetaLight(light_device, radiora, zone))
    async_add_entities(devices, True)

class RadioRAClassicLight(RadioRAClassicDevice, Light):
    """Representation of a Lutron RadioRA Classic light."""

    def __init__(self, device, radiora, zone):
        super().__init__(device, radior, zone)
        self._brightness = DEFAULT_BRIGHTNESS

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness # we cannot GET the brightness of the light...only return what we know

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        self._radiora.turn_on(self._zone)

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        self._radiora.turn_off(self._zone)

    @property
    def is_on(self):
        """Return true if device is on."""
        self._radiora.is_zone_on(self._zone)

    async def async_update(self):
        """Call when forcing a refresh of the device."""

        # we only need ONE of the light switches to update to get data for ALL the zones
        if self._zone == 1:  # FIXME: this should be done on an object we know always exist, the first dimmer COULD have not been configured
            self._radiora.update()
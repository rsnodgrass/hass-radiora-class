"""Support for Lutron RadioRA Classic lights."""
import logging

from homeassistant.components.light import (
    DOMAIN,
    SUPPORT_BRIGHTNESS,
    ATTR_BRIGHTNESS,
    Light,
)
from homeassistant.components.lutron.light import to_hass_level, to_lutron_level

from . import RADIORA_CLASSIC, RadioRAClassicDevice

LOG = logging.getLogger(__name__)

DEFAULT_BRIGHTNESS = 100

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Lutron RadioRA Classic lights."""
    radiora = hass.data[RADIORA_CLASSIC]

    devices = []
    for zone in range(1, 31):  # FIXME: allow override to specify names AND which zones to include
        name = f"RadioRA Zone {self._zone}"
        devices.append(RadioRAClassicLight(radiora, zone, name))

    async_add_entities(devices)

class RadioRAClassicLight(RadioRAClassicDevice, Light):
    """Representation of a Lutron RadioRA Classic light."""

    def __init__(self, radiora, zone, name):
        super().__init__(radiora, zone, name)
        self._brightness = DEFAULT_BRIGHTNESS

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def brightness(self):
        """Return the brightness of the light."""
        if self.is_on():
            # RadioRA doesn't support GETTING current dimmer level; return last set value (or 100 if never set)
            return to_hass_level(self._brightness)
        else:
            return 0

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        self._radiora.turn_on(self._zone)

        if ATTR_BRIGHTNESS in kwargs:
            hass_brightness = int((kwargs[ATTR_BRIGHTNESS] / 255.0) * 200.0)
            lutron_brightness = to_lutron_level( hass_brightness )
            await self._radiora.set_dimmer_level(self._zone, lutron_brightness)
            self._brightness = lutron_brightness
            return

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self._radiora.turn_off(self._zone)

    @property
    def is_on(self):
        """Return true if device is on."""
        await self._radiora.is_zone_on(self._zone)

    async def async_update(self):
        """Call when forcing a refresh of the device."""

        # we only need ONE of the light switches to update to get data for ALL the zones
        if self._zone == 1:  # FIXME: this should be done on an object we know always exist, the first dimmer COULD have not been configured
            await self._radiora.update()
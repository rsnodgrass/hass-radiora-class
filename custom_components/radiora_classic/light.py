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
    devices.append(RadioRAClassicBridge(radiora, "RadioRA Bridge"))

    for zone in range(1, 31):  # FIXME: allow override to specify names AND which zones to include
        name = f"RadioRA Zone {zone}"
        devices.append(RadioRAClassicLight(radiora, zone, name))

    async_add_entities(devices)

class RadioRAClassicLight(RadioRAClassicDevice, Light):
    """Representation of a Lutron RadioRA Classic light."""

    def __init__(self, radiora, zone, name):
        super().__init__(radiora, zone, name)
        self._brightness = DEFAULT_BRIGHTNESS
        self._is_on = True

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def brightness(self):
        """Return the brightness of the light."""
        if self._is_on:
            # RadioRA doesn't support GETTING current dimmer level;
            # return last set value (or 100 if never set)
            return to_hass_level(self._brightness)
        else:
            return 0

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        # if brightness specified, set the dimmer level
        if ATTR_BRIGHTNESS in kwargs:
            hass_brightness = int((kwargs[ATTR_BRIGHTNESS] / 255.0) * 200.0)
            lutron_brightness = to_lutron_level( hass_brightness )
            await self._radiora.set_dimmer_level(self._zone, lutron_brightness)
            self._brightness = lutron_brightness
            self._is_on = True
        else:
            # if no dimmer level set, just turn on        
            await self._radiora.turn_on(self._zone)
            self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self._radiora.turn_off(self._zone)
        self._is_on = False
        self._brightness = 0

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._is_on

    async def async_update(self):
        """Call when forcing a refresh of the device."""
        self._is_on = (await self._radiora).is_zone_on(self._zone)



class RadioRAClassicBridge(Light):
    """Representation of a Lutron RadioRA Classic bridge."""

    def __init__(self, radiora, name):
        super().__init__()
        self._radiora = radiora
        self._name = name
        self._is_on = True

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def supported_features(self):
        """Flag supported features."""
        #return SUPPORT_TURN_OFF | SUPPORT_TURN_ON
        return

    async def async_added_to_hass(self):
        """Register callbacks."""
    #    self._radiora.add_subscriber(
    #        self.device_id, self.async_schedule_update_ha_state
    #    )
        return

    async def async_turn_on(self, **kwargs):
        """Turn all lights on."""
        await self._radiora.turn_all_on()
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Turn all lights off."""
        await self._radiora.turn_all_off()
        self._is_on = False

    async def async_security_flash_on(self, **kwargs):
        """Turn the security flashing lights on."""
        await self._radiora.turn_flash_on()

    async def async_security_flash_off(self, **kwargs):
        """Turn the security flashing lights off."""
        await self._radiora.turn_flash_off()

    @property
    def is_on(self):
        """Return true if any light controlled by the bridge is on."""
        return self._is_on

    async def async_update(self):
        """Call when forcing a refresh of the device."""

        # we only need ONE of the light switches to update to get data for ALL the zones
        await self._radiora.update()

        # if any light is on, then the Bridge is on
        is_on = False
        for zone in range(1, 31):
            if await self._radiora.is_zone_on(zone):
                is_on = True
                break
        self._is_on = is_on

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {}

    @property
    def should_poll(self):
        """No polling needed."""
        return True

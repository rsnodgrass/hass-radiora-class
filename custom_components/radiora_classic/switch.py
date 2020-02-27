"""Support for Lutron RadioRA Classic switches."""
import logging

from homeassistant.components.switch import DOMAIN, SwitchDevice

from . import LUTRON_RADIORA_CLASSIC_SMARTBRIDGE, RadioRADevice

LOG = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up Lutron switch."""
    devs = []
    bridge = hass.data[LUTRON_RADIORA_CLASSIC_SMARTBRIDGE]
    switch_devices = bridge.get_devices_by_domain(DOMAIN)

    for switch_device in switch_devices:
        dev = RadioRAClassicLight(switch_device, bridge)
        devs.append(dev)

    async_add_entities(devs, True)
    return True


class RadioRAClassicLight(RadioRAClassicDevice, SwitchDevice):
    """Representation of a Lutron RadioRA Classic switch."""

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._smartbridge.turn_on(self.device_id)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._smartbridge.turn_off(self.device_id)

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device["current_state"] > 0

    async def async_update(self):
        """Update when forcing a refresh of the device."""
        self._device = self._smartbridge.get_device_by_id(self.device_id)
        _LOGGER.debug(self._device)

"""
RadioRA Classic Home Assistant sensors

FUTURE:
- support Celsius and Fahrenheit (based on RadioRA Classic's cloud responses)
"""
import logging

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

from . import ( RadioRA ClassicEntity, SENSORPUSH_SERVICE, SENSORPUSH_SAMPLES,
                SENSORPUSH_DOMAIN, CONF_MAXIMUM_AGE,
                CONF_UNIT_SYSTEM, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC, UNIT_SYSTEMS )

LOG = logging.getLogger(__name__)

DEPENDENCIES = ['radiora_classic']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_UNIT_SYSTEM, default=UNIT_SYSTEM_IMPERIAL): cv.string
    }
)

# pylint: disable=unused-argument
async def async_setup_platform(hass, config, async_add_entities_callback, discovery_info=None):
#def setup_platform(hass, config, add_entities_callback, discovery_info=None):
    """Setup the RadioRA Classic sensor"""

    radiora_classic_service = hass.data.get(SENSORPUSH_SERVICE)
    if not radiora_classic_service:
        LOG.info("NOT setting up RadioRA Classic -- missing SENSORPUSH_SERVICE")
        return

#    conf = hass.config[SENSORPUSH_DOMAIN]
    conf = None

    unit_system = UNIT_SYSTEM_IMPERIAL
#    if conf.get(CONF_UNIT_SYSTEM) == UNIT_SYSTEM_METRIC:
#        unit_system = UNIT_SYSTEM_METRIC

    LOG.debug(f"Setting up RadioRA Classic sensors: {radiora_classic_service.sensors}")

    hass_sensors = []
    for sensor_info in radiora_classic_service.sensors.values():
        LOG.info(f"SensorInfo: {sensor_info} -- {type(sensor_info)}")

        if sensor_info.get('active') == 'False': # FIXME
            LOG.warn(f"Ignoring inactive RadioRA Classic sensor '{sensor_info.get('name')}")
            continue

        LOG.info(f"Instantiating RadioRA Classic sensors: {sensor_info}")
        hass_sensors.append( RadioRA ClassicTemperature(hass, conf, sensor_info, unit_system) )
        hass_sensors.append( RadioRA ClassicHumidity(hass, conf, sensor_info, unit_system))

    # execute callback to add new entities
    async_add_entities_callback(hass_sensors, True)

# pylint: disable=too-many-instance-attributes
class RadioRA ClassicHumidity(RadioRA ClassicEntity):
    """Humidity sensor for a RadioRA Classic device"""

    def __init__(self, hass, config, sensor_info, unit_system):
        self._state = ''
        super().__init__(hass, config, 'Humidity', sensor_info, unit_system, 'humidity')

    @property
    def icon(self):
        return 'mdi:water-percent'

    @property
    def unit_of_measurement(self):
        """Relative Humidity (Rh %)"""
        return '%'

# pylint: disable=too-many-instance-attributes
class RadioRA ClassicTemperature(RadioRA ClassicEntity):
    """Temperature sensor for a RadioRA Classic device"""

    def __init__(self, hass, config, sensor_info, unit_system):
        self._state = ''
        super().__init__(hass, config, 'Temperature', sensor_info, unit_system, 'temperature')

    @property
    def unit_of_measurement(self):
        """Temperature (Fahrenheit or Celsius)"""
        return UNIT_SYSTEMS.get(self._unit_system).get('temperature')

"""
SensorPush for Home Assistant
See https://github.com/rsnodgrass/hass-sensorpush
"""
import logging

import time
from datetime import timedelta
import voluptuous as vol
from requests.exceptions import HTTPError, ConnectTimeout

from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.dispatcher import dispatcher_send, async_dispatcher_connect
from homeassistant.helpers.event import track_time_interval
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL

LOG = logging.getLogger(__name__)

SENSORPUSH_DOMAIN = 'sensorpush'

SENSORPUSH_SERVICE = 'sensorpush_service'
SENSORPUSH_SAMPLES = 'sensorpush_samples'
SIGNAL_SENSORPUSH_UPDATED = 'sensorpush_updated'

NOTIFICATION_ID = 'sensorpush_notification'
NOTIFICATION_TITLE = 'SensorPush'

ATTR_BATTERY_VOLTAGE = 'battery_voltage'
ATTR_DEVICE_ID       = 'device_id'
ATTR_OBSERVED_TIME   = 'observed_time'

CONF_UNIT_SYSTEM = 'unit_system'
CONF_MAXIMUM_AGE = 'maximum_age' # maximum age (in minutes) of observations before they expire

UNIT_SYSTEM_IMPERIAL = 'imperial'
UNIT_SYSTEM_METRIC = 'metric'

UNIT_SYSTEMS = {
    UNIT_SYSTEM_IMPERIAL: { 
        'system':      'imperial',
        'temperature': '°F',
        'humidity':    '%' # 'Rh'
    },
    UNIT_SYSTEM_METRIC: { 
        'system':      'metric',
        'temperature': '°C',
        'humidity':    '%' # 'Rh'
    }
}

CONFIG_SCHEMA = vol.Schema({
        SENSORPUSH_DOMAIN: vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Optional(CONF_SCAN_INTERVAL, default=60): cv.positive_int,
            vol.Optional(CONF_UNIT_SYSTEM, default='imperial'): cv.string,
            vol.Optional(CONF_MAXIMUM_AGE, default=30): cv.positive_int
        })
    }, extra=vol.ALLOW_EXTRA
)

def setup(hass, config):
    """Initialize the SensorPush integration"""
    conf = config[SENSORPUSH_DOMAIN]

    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    try:
        from pysensorpush import PySensorPush

        sensorpush_service = PySensorPush(username, password)
        #if not sensorpush_service.is_connected:
        #    return False
        # FIXME: log warning if no sensors found?

        # share reference to the service with other components/platforms running within HASS
        hass.data[SENSORPUSH_SERVICE] = sensorpush_service
        hass.data[SENSORPUSH_SAMPLES] = sensorpush_service.samples

    except (ConnectTimeout, HTTPError) as ex:
        LOG.error("Unable to connect to SensorPush: %s", str(ex))
        hass.components.persistent_notification.create(
            f"Error: {ex}<br />You will need to restart Home Assistant after fixing.",
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID,
        )
        return False

    def refresh_sensorpush_data(event_time):
        """Call SensorPush service to refresh latest data"""
        LOG.debug("Updating data from SensorPush cloud API")

        # TODO: discovering new devices (and auto-configuring HASS sensors) is not supported
        #hass.data[SENSORPUSH_SERVICE].update(update_devices=True)

        # retrieve the latest samples from the SensorPush cloud service
        latest_samples = hass.data[SENSORPUSH_SERVICE].samples
        if latest_samples:
            hass.data[SENSORPUSH_SAMPLES] = latest_samples

            # notify all listeners (sensor entities) that they may have new data
            dispatcher_send(hass, SIGNAL_SENSORPUSH_UPDATED)
        else:
            LOG.warn("Unable to fetch latest samples from SensorPush cloud")

    # subscribe for notifications that an update should be triggered
    hass.services.register(SENSORPUSH_DOMAIN, 'update', refresh_sensorpush_data)

    # automatically update SensorPush data (samples) on the scan interval
    scan_interval = timedelta(seconds = conf.get(CONF_SCAN_INTERVAL))
    track_time_interval(hass, refresh_sensorpush_data, scan_interval)

    return True

class SensorPushEntity(Entity):
    """Base Entity class for SensorPush devices"""

    def __init__(self, hass, config, name_suffix, sensor_info, unit_system, field_name):
        self._hass = hass
        self._sensor_info = sensor_info
        self._unit_system = unit_system
        self._device_id = sensor_info.get('id')
        self._field_name = field_name
        self._attrs = {}
        self._name = f"{sensor_info.get('name')} {name_suffix}"

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def icon(self):
        return 'mdi:gauge'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

    async def async_added_to_hass(self):
        """Register callbacks."""
        # register callback when cached SensorPush data has been updated
        async_dispatcher_connect(self.hass, SIGNAL_SENSORPUSH_UPDATED, self._update_callback)

    @callback
    def _update_callback(self):
        """Call update method."""
        samples = self._hass.data[SENSORPUSH_SAMPLES]
        sensor_results = samples['sensors']
        
        sensor_data = sensor_results[self._device_id]
        latest_result = sensor_data[0]

        # FIXME: check data['observed'] time against config[CONF_MAXIMUM_AGE], ignoring stale entries

        self._state = float(latest_result.get(self._field_name))
        self._attrs.update({
            ATTR_OBSERVED_TIME   : latest_result['observed'],
            ATTR_BATTERY_VOLTAGE : self._sensor_info.get('battery_voltage') # FIXME: not updated except on restarts of Home Assistant
        })

        LOG.debug(f"Updated {self._name} to {self._state} {self.unit_of_measurement} : {latest_result}")

        # let Home Assistant know that SensorPush data for this entity has been updated
        self.async_schedule_update_ha_state()

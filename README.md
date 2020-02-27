# Lutron RadioRA Classic for Home Assistant

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Home Assistant integration for the [Lutron RadioRA Classic] light switches and dimmers.

## Installation

If you have trouble with installation and configuration, visit the [SensorPush Home Assistant community discussion](https://community.home-assistant.io/t/radiora-classic-humidity-and-temperature-sensors/105711).

### Step 1: Install Custom Components

Easiest is by setting up [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) and then adding the "Integration" repository: *rsnodgrass/hass-radiora-classic*. However you can also manually copy all the files in [custom_components/radiora-classic/](https://github.com/rsnodgrass/hass-radiora-classic/custom_components/radiora-classic) directory to `/config/custom_components/radiora-classic` on your Home Assistant installation.

### Step 2: Configure Light Switches

Example configuration.yaml entry:

```yaml
radiora_classic:
  controllers:
    - tty: /dev/ttyUSB0
      name: "Main House"   # defaults to "RadioRA Classic"
```

Note this supports multiple RS232 controllers. For each RadioRA RS232 controller, this will dynamically create 32 switches, plus one sensor/switch for the RS232 controller itself.

Additionally, you can configure naming and switch type for each zone.

```yaml
radiora_classic:
  controllers:
    - tty: /dev/ttyUSB0
      name: "Main House"   # defaults to "RadioRA Classic"
      zones:
        1:
	  name: "Kichen"
	  type: dimmer
        2:
	  name: "Bathroom"
	  type: switch
```


#### Lovelace

## See Also

* [Community support for Lutron RadioRA Classic](https://community.home-assistant.io/t/radiora-classic-humidity-and-temperature-sensors/105711)
*

## Known Issues

* Not working

#### Not Supported

* This will not support Lutron scenes, instead relying on Home Assistant scene specification which are more flexible and can include non-Lutron devices.
* Support for fans is not currently enabled.

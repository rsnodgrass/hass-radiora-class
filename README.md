# Lutron RadioRA Classic for Home Assistant

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Home Assistant integration for the [Lutron RadioRA Classic] light switches and dimmers, using the RadioRA Classic Smart Bridge.

## Installation

If you have trouble with installation and configuration, visit the [SensorPush Home Assistant community discussion](https://community.home-assistant.io/t/radiora-classic-humidity-and-temperature-sensors/105711).

### Step 1: Install Custom Components

Easiest is by setting up [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) and then adding the "Integration" repository: *rsnodgrass/hass-radiora-classic*. However you can also manually copy all the files in [custom_components/radiora-classic/](https://github.com/rsnodgrass/hass-radiora-classic/custom_components/radiora-classic) directory to `/config/custom_components/radiora-classic` on your Home Assistant installation.

### Step 2: Configure Light Switches

Example configuration.yaml entry:

```yaml
sensors:
  - platform: radiora_classic
    host: localhost
    port: 8333
```

You only need to create the sensor for the Lutron RadioRA bridge and Home Assistant will dynamically create all the switches and dimmers based on the Bridge settings.

#### Lovelace

## See Also

* [Community support for Lutron RadioRA Classic](https://community.home-assistant.io/t/radiora-classic-humidity-and-temperature-sensors/105711)
*

## Known Issues

* Not working

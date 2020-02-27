# Lutron RadioRA Classic for Home Assistant

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Home Assistant integration for the [Lutron RadioRA Classic](http://www.lutron.com/TechnicalDocumentLibrary/RadioRA%20Install%20Guide.pdf) light switches and dimmers.

## Installation

If you have trouble with installation and configuration, visit the [Lutron Home Assistant community discussion](https://community.home-assistant.io/t/integrating-lutron-radiora2/130307).

### Step 1: Install Custom Components

Easiest is by setting up [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) and then adding the "Integration" repository: *rsnodgrass/hass-radiora-classic*.

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

* [Lutron Home Assistant community support](https://community.home-assistant.io/t/integrating-lutron-radiora2/130307)

## Known Issues

#### Not Supported

* switches and fans
* scenes/rooms
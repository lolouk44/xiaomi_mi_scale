[![version](https://img.shields.io/github/v/release/lolouk44/xiaomi_mi_scale)](https://github.com/lolouk44/xiaomi_mi_scale/releases)
[![docker_badge](https://img.shields.io/docker/pulls/lolouk44/xiaomi-mi-scale)](https://hub.docker.com/r/lolouk44/xiaomi-mi-scale)
# Xiaomi Mi Scale

Code to read weight measurements from Xiaomi Body Scales.

## BREAKING CHANGE:
Please note that as off 0.2.0, the config is now located in options.json and no longer in the docker-compose / environment
Please read on for for more information.
This change was necessary to allow for unlimited number of users.

## Supported Scales:
Name | Model | Picture
--- | --- | :---:
[Mi Smart Scale 2](https://www.mi.com/global/scale) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | XMTZCO1HM, XMTZC04HM | ![Mi Scale_2](Screenshots/Mi_Smart_Scale_2_Thumb.png)
[Mi Body Composition Scale](https://www.mi.com/global/mi-body-composition-scale/) | XMTZC02HM | ![Mi Scale](Screenshots/Mi_Body_Composition_Scale_Thumb.png)
[Mi Body Composition Scale 2](https://c.mi.com/thread-2289389-1-0.html) | XMTZC05HM | ![Mi Body Composition Scale 2](Screenshots/Mi_Body_Composition_Scale_2_Thumb.png)


## Home Assistant Add-On:
If using Home Assistant (formerly known as hass.io), try instead the [Xiaomi Mi Scale Add-On for Home Assistant](https://github.com/lolouk44/hassio-addons/tree/master/mi-scale) based on this repository.

## Getting the Mac Address of your Scale:

1. Retrieve the scale's MAC Address from the Xiaomi Mi Fit App:

![MAC Address](Screenshots/MAC_Address.png)

## Setup & Configuration:
### Running script with Docker:

1. Supported platforms:
	1. linux/386
	1. linux/amd64
	1. linux/arm32v6
	1. linux/arm32v7
	1. linux/arm64v8
1. Open `docker-compose.yml` (see below) and edit the environment to suit your configuration...
1. Stand up the container - `docker-compose up -d`

### docker-compose:
```yaml
version: '3'
services:

  mi-scale:
    image: lolouk44/xiaomi-mi-scale:latest
    container_name: mi-scale
    restart: always

    network_mode: host
    privileged: true
    volumes:
      - ./data:/data
      - /var/run/dbus/:/var/run/dbus/:ro #needed for bleak
```
### options.json:
All the config needs to be in a file named `options.json`. You can get a copy of one with minimum config [here](./options.json)

List of options

Option | Type | Required | Description
--- | --- | --- | ---
MISCALE_MAC | string | Yes | Mac address of your scale
MQTT_HOST | string | Yes | MQTT Server (defaults to 127.0.0.1)
HCI_DEV | string | No | Bluetooth hci device to use. Defaults to hci0
MQTT_PREFIX | string | No | MQTT Topic Prefix. Defaults to miscale
MQTT_USERNAME | string | No | Username for MQTT server (comment out if not required)
MQTT_PASSWORD | string | No | Password for MQTT (comment out if not required)
MQTT_PORT | int | No | Defaults to 1883
MQTT_DISCOVERY | bool | No | MQTT Discovery for Home Assistant Defaults to true
MQTT_DISCOVERY_PREFIX | string | No | MQTT Discovery Prefix for Home Assistant. Defaults to homeassistant
MQTT_TLS_CACERTS | string | No | MQTT TLS connection: directory with CA certificate(s) that signed MQTT Server's TLS certificate, defaults to None (= no TLS connection)
MQTT_TLS_INSECURE | bool | No | MQTT TLS connection: don't verify hostname in TLS certificate, defaults to None (= always check hostname)
BLUEPY_PASSIVE_SCAN | bool | No | Try to set to true if getting an error like `Bluetooth connection error: Failed to execute management command ‘le on’` on a Raspberry Pi. Defaults to false
TIME_INTERVAL | int | No | Time in sec between each query to the scale, to allow other applications to use the Bluetooth module. Defaults to 30
USERS | List | Yes | List of users to add

Auto-gender selection/config -- This is used to create the calculations such as BMI, Water/Bone Mass etc...
Here is the logic used to assign a measured weight to a user:
- If the weight is within the range of a user's defined values for GT and LT, then it will be assigned (published) to that user.
- If the weight matches two separate user ranges, it will only be assigned to the first user that matched (so don't overlap ranges!)

User Option | Type | Required | Description
--- | --- | --- | ---
GT | int | Yes | Greater Than - Weight must be greater than this value - this will be the lower limit for the weight range of this user
LT | int | Yes | Less Than - Weight must be less than this value - this will be the upper limit for the weight range of this user
SEX | string | Yes | male / female
NAME | string | Yes | Name of the user
HEIGHT | int | Yes | Height (in cm) of the user
DOB | string | Yes | DOB (in yyyy-mm-dd format)

Note: The weight definitions must be in the same unit as the scale (kg, Lbs, jin)

### Running script directly on your host system:

***Note: Python 3.6 or higher is required to run the script manually***

***Note: this is now deprecated. It would still work provided the path to options.json is manually set in the code manually set path at line 39: `with open('/data/options.json') as json_file`***

1. Install python requirements (pip3 install -r requirements.txt)
1. Open `wrapper.sh` and configure your environment variables to suit your setup.
1. Add a cron-tab entry to wrapper like so:

```sh
@reboot bash /path/to/wrapper.sh
```

**NOTE**: Although once started the script runs continuously, it may take a few seconds for the data to be retrieved, computed and sent via mqtt.

## Home-Assistant Setup:
Under the `sensor` block, enter as many blocks as users configured in your environment variables.

```yaml
mqtt:
  sensor:
    - name: "Example Name Weight"
      state_topic: "miscale/USER_NAME/weight"
      value_template: "{{ value_json['weight'] }}"
      unit_of_measurement: "kg"
      json_attributes_topic: "miscale/USER_NAME/weight"
      icon: mdi:scale-bathroom
      # Below lines only needed if long term statistics are required
      state_class: "measurement"

    - name: "Example Name BMI"
      state_topic: "miscale/USER_NAME/weight"
      value_template: "{{ value_json['bmi'] }}"
      icon: mdi:human-pregnant
      unit_of_measurement: "kg/m2"
      # Below lines only needed if long term statistics are required
     state_class: "measurement"
```

![Mi Scale](Screenshots/HA_Lovelace_Card.png)

![Mi Scale](Screenshots/HA_Lovelace_Card_Details.png)

## Acknowledgements:
Thanks to @syssi (https://gist.github.com/syssi/4108a54877406dc231d95514e538bde9) and @prototux (https://github.com/wiecosystem/Bluetooth) for their initial code

Special thanks to [@ned-kelly](https://github.com/ned-kelly) for his help turning a "simple" python script into a fully fledged docker container

Thanks to [@bpaulin](https://github.com/bpaulin), [@AiiR42](https://github.com/AiiR42), [@andreasbrett](https://github.com/andreasbrett) for their PRs and collaboration

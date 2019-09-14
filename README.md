# Xiaomi Mi Scale

Code to read weight measurements from [Mi Body Composition Scale](https://www.mi.com/global/mi-body-composition-scale/) (aka Xiaomi Mi Scale V2)

![Mi Scale](Screenshots/Mi_Scale.png)

Note: Framework is present to also read from Xiaomi Scale V1, although I do not own one to test so code has not been maintained

## Getting the Mac Address of your Scale:

1. Retrieve the scale's MAC Address (you can identify your scale by looking for `MIBCS` entries) using this command:
```
$ sudo hcitool lescan
LE Scan ...
F8:04:33:AF:AB:A2 [TV] UE48JU6580
C4:D3:8C:12:4C:57 MIBCS
[...]
```
1. Note down your `MIBCS` mac address - we will need to use this as part of your configuration...

## Setup & Configuration:
### Running script with Docker:

1. Open `docker-compose.yml` and edit the environment to suit your configuration...
1. Stand up the container - `docker-compose up -d`

### Running script directly on your host system:

1. Install python requirements (pip3 install -r requirements.txt)
1. Open `wrapper.sh` and configure your environment variables to suit your setup.
1. Add a cron-tab entry to wrapper like so:

```sh
*/5 * * * * bash /path/to/wrapper.sh
```

**NOTE**: It's best to schedule via crontab at most, every 5 min (so as not to drain the battery on your scale):
```
*/5 * * * * python3 /path-to-script/Xiaomi_Scale.py
```

## Home-Assistant Setup:
Under the `sensor` block, enter as many blocks as users configured in your environment variables:

```yaml
  - platform: mqtt
    name: "Example Name Weight"
    state_topic: "miScale/USERS_NAME/weight"
    value_template: "{{ value_json['Weight'] }}"
    unit_of_measurement: "kg"
    json_attributes_topic: "miScale/USERS_NAME/weight"
    icon: mdi:scale-bathroom

  - platform: mqtt
    name: "Example Name BMI"
    state_topic: "miScale/USERS_NAME/weight"
    value_template: "{{ value_json['BMI'] }}"
    icon: mdi:human-pregnant

```

![Mi Scale](Screenshots/HA_Lovelace_Card.png)

![Mi Scale](Screenshots/HA_Lovelace_Card_Details.png)

## Acknowledgements: 
Thanks to @syssi (https://gist.github.com/syssi/4108a54877406dc231d95514e538bde9) and @prototux (https://github.com/wiecosystem/Bluetooth) for their initial code

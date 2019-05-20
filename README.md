# Xiaomi Mi Scale

Code to read weight measurements from [Mi Body Composition Scale](https://www.mi.com/global/mi-body-composition-scale/) (aka Xiaomi Mi Scale V2)

![Mi Scale](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/Screenshots/Mi_Scale.png)

Note: Framework is present to also read from Xiaomi Scale V1, although I do not own one to test so code has not been maintained

## Setup:
1. Retrieve the scale's MAC Address (you can identify your scale by looking for `MIBCS` entries) using this command:
```
$ sudo hcitool lescan
LE Scan ...
F8:04:33:AF:AB:A2 [TV] UE48JU6580
C4:D3:8C:12:4C:57 MIBCS
[...]
```
1. Copy all files
1. Open `Xiaomi_Scale.py`
1. Assign Scale's MAC address to variable `MISCALE_MAC`
1. Edit MQTT Credentials
1. Edit user logic/data on lines 117-131

## How to use?
- Must be executed with Python 3 else body measurements are incorrect.
- Must be executed as root, therefore best to schedule via crontab every 5 min (so as not to drain the battery):
```
*/5 * * * * python3 /path-to-script/Xiaomi_Scale.py
```

## Home-Assistant Setup:
Under the `sensor` block, enter as many blocks as users setup on lines 117-131 in `Xiaomi_Scale.py`.
```
  - platform: mqtt
    name: "Lolo Weight"
    state_topic: "lolo/weight"
    value_template: "{{ value_json['Weight'] }}"
    unit_of_measurement: "kg"
    json_attributes_topic: "lolo/weight"
    icon: mdi:scale-bathroom

  - platform: mqtt
    name: "Lolo BMI"
    state_topic: "lolo/weight"
    value_template: "{{ value_json['BMI'] }}"
    icon: mdi:human-pregnant

  ```
![Mi Scale](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/Screenshots/HA_Lovelace_Card.png)
![Mi Scale](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/Screenshots/HA_Lovelace_Card_Details.png)

## Acknowledgements: 
Thanks to @syssi (https://gist.github.com/syssi/4108a54877406dc231d95514e538bde9) and @prototux (https://github.com/wiecosystem/Bluetooth) for their initial code

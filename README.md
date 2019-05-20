# Xiaomi Mi Scale

Code to read weight measurements from [Mi Body Composition Scale](https://www.mi.com/global/mi-body-composition-scale/) (aka Xiaomi Mi Scale V2)

![Mi Scale](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/Mi_Scale.png)

Note: Framework is present to also read from Xiaomi Scale V1, although I do not own one to test so code has not been maintained

## Setup:
1. Copy all files
1. Open `Xiaomi_Scale.py`
1. Edit MQTT Credentials
1. Edit user logic/data on lines 117-131

## How to use?
- Must be executed with Python 3 else body measurements are incorrect.
- Must be executed as root, therefore best to schedule via crontab every 5 min (so as not to drain the battery):
```
*/5 * * * * python3 /path-to-script/Xiaomi_Scale.py
```

## Acknowledgements: 
Thanks to @syssi (https://gist.github.com/syssi/4108a54877406dc231d95514e538bde9) and @prototux (https://github.com/wiecosystem/Bluetooth) for their initial code

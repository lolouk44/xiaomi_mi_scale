## [0.3.5] - 2022-10-10
### Added
- Added extra logging. Logging Level can be set from config file.
- Deprecated options MISCALE_VERSION, TIME_INTERVAL.
### Changed
- Restored HCI Settings

## [0.3.4] - 2022-10-05
### Changed
- Restored MQTT Discovery. ([fixes #65](https://github.com/lolouk44/hassio-addons/issues/65))
- Removed no longer needed MISCALE_VERSION

## [0.3.3] - 2022-10-03
### Changed
- Restoring handling of V1 scales. ([fixes #64](https://github.com/lolouk44/hassio-addons/issues/64))

## [0.3.0] - 2022-10-02
### Changed
- Stopped using deprecated/no longer supported bluepy library and replaced with bleak, requiring major code overhaul. ([fixes #59](https://github.com/lolouk44/hassio-addons/issues/59))
- Updated documentation to reflect MQTT integration (moved out of sensor config)
### Breaking Changes
- `/var/run/dbus/:/var/run/dbus/:ro` is needed in docker volumes for bleak to work
- If using a MiScale V1, make sure you add the MISCALE_VERSION to your options.json file (see doc)

## [0.2.4] - 2022-02-03
### Changed
- Changed time format for datestamp to contain timezone ([fixes #59](https://github.com/lolouk44/hassio-addons/issues/59))

## [0.2.3] - 2022-01-13
### Added
- Added support for Long Term Statistics (HA 2021.9 minimum required)
- Impedance posted to MQTT ([fixes #56](https://github.com/lolouk44/hassio-addons/issues/56))

## [0.2.2] - 2021-06-28
### Changed
- Fixed handling of MQTT_PORT and TIME_INTERVAL

## [0.2.1] - 2021-05-13
### Changed
- Fixed user lookup by non kg weight

## [0.2.0] - 2021-03-23
### Breaking Changes
Please note that as off 0.2.0, the config is now located in options.json and no longer in the docker-compose / environment. Be sure to check the [Doc](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/README.md) for more information. This change was necessary to allow for unlimited number of users.
### Changed
- Unlimited users ! This unfortunately comes with a breaking change. Be sure to check the [Doc](https://github.com/lolouk44/xiaomi_mi_scale/blob/master/README.md) for more information
### Added
- Added BLUEPY_PASSIVE_SCAN Option for Raspberry Pi users experiencing Bluetooth troubles (in case you're not using the [add-on](https://github.com/lolouk44/hassio-addons/tree/master/mi-scale))

## [0.1.16] - 2021-03-16
### Changed
- Fixed MQTT Retain defaults

## [0.1.15] - 2021-03-12
### Changed
- Added MQTT Retain Option ([fixes #44](https://github.com/lolouk44/xiaomi_mi_scale/issues/44))
- Added MQTT TLS Option ([PR 43](https://github.com/lolouk44/xiaomi_mi_scale/pull/43))

## [0.1.14] - 2020-11-26
### Changed
- Reduced docker image size

## [0.1.13] - 2020-11-26
### Changed
- Fixed MQTT Discovery Message

## [0.1.12] - 2020-11-23
### Changed
- Updated workflow to automatically build docker images on new releases with version and latest tags

## [0.1.11] - 2020-11-23
### Changed
- Remove additional logging for Scale V1 that was used for testing
- Changed timestamp to default python format (fixes https://github.com/lolouk44/xiaomi_mi_scale/issues/29)
- Removed hard-coded 'unit_f_measurement' in the MQTT Discovery (fixes https://github.com/lolouk44/hassio-addons/issues/22)
- Fixed hard coded MQTT Discovery Prefix (fixes https://github.com/lolouk44/xiaomi_mi_scale/issues/35)
- Change measures format to be numbers instead of string where applicable (https://github.com/lolouk44/xiaomi_mi_scale/pull/36)
### Added
- Created workflow to automatically build docker images on new releases (Thanks [@AiiR42](https://github.com/AiiR42) for your help)


## [0.1.10] - 2020-09-09
### Changed
- Fixed issue with detection of boolean in MQTT_DISCOVERY (https://github.com/lolouk44/hassio-addons/issues/16 and https://github.com/lolouk44/xiaomi_mi_scale/issues/31)

## [0.1.9] - 2020-09-08
### Changed
- Fixed typo in MQTT message following the **breaking change** to snake_case attributes in 0.1.8

## [0.1.8] - 2020-09-08
### Breaking Changes
- Attributes are now snake_case (fixes https://github.com/lolouk44/xiaomi_mi_scale/issues/24)
### Changed
- Fixed default MQTT Prefix in config.json typo (fixes https://github.com/lolouk44/hassio-addons/issues/6)
- Fixed MQTT Discovery value check to discover
- Changed timestamp to default python format
- Changes the bluetooth reset from reset to down-wait-up (fixes https://github.com/lolouk44/hassio-addons/issues/13)
- Fixed hard coded hci0 to provided hci interface when performing a reset
- Fixed weight in Lbs not detected on Scale V1 (XMTZCO1HM) (fixes https://github.com/lolouk44/xiaomi_mi_scale/issues/28)
- Fixed body calculations for non kg weights
- Updated README
### Added
- Added unit to attributes

## [0.1.7] - 2020-07-06
### Added
- repository.json to make it a real add-on repo (fixes https://github.com/lolouk44/hassio-addons/issues/4)
## Changed
- Now truly handles optional config entries(fixes https://github.com/lolouk44/hassio-addons/issues/3)
- MQTT Discovery set wtih retain flag (fixes https://github.com/lolouk44/hassio-addons/issues/2)
- README updated to use Xiaomi Mi Fit App to retrieve the MAC Address (fixes https://github.com/lolouk44/xiaomi_mi_scale/pull/25)

## [0.1.6] - 2020-07-01
### Added
- Docker Image so install is quicker (no local build required).

## [0.1.5] - 2020-07-01
### Added
- MQTT Discovery Support.

## [0.1.4] - 2020-06-29
### Added
- First release (version in line with non Add-On script for ease of maintenance).

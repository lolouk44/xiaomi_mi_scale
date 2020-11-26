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

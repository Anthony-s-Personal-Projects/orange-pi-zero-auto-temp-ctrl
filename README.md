# Auto Temp Ctrl for Orange Pi Zero

Automatic fan control service for Orange Pi Zero and similar boards.  
This service will automatically turn on and off the fan based on the CPU temperature using GPIO control.

## Features

- Automatically control fan based on configurable temperature thresholds
- Simple installation via prebuilt .deb package
- Automatically install WiringOP (required for GPIO control) during installation if needed
- Easy uninstallation with cleanup

## Installation

Download the latest `.deb` release from the [Releases](https://github.com/Anthony-s-Personal-Projects/orange-pi-zero-auto-temp-ctrl/releases) page.

Then install with:

```bash
sudo dpkg -i auto-temp-ctrl.deb
```

If WiringOP is not installed, the installer will prompt you to install it automatically.

After installation:

```bash
auto-temp-ctrl status
auto-temp-ctrl show
```

## Uninstallation

To uninstall and clean up:

```bash
auto-temp-ctrl uninstall
```

## Configuration

You can edit the config file to change temperature thresholds and GPIO pin:

```
/etc/auto-temp-ctrl.conf
```

## License

MIT License

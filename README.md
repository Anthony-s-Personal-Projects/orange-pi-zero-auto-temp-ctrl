# Auto Temp Ctrl for Orange Pi Zero

Automatic fan control service for Orange Pi Zero and similar boards.  
This service will automatically turn on and off the fan based on the CPU temperature using GPIO control.

## Installation (Recommended - via APT)

You can now install easily from the APT repository with automatic updates:

```bash
wget https://anthony-s-personal-projects.github.io/orange-pi-zero-auto-temp-ctrl/public.key
sudo apt-key add public.key

echo "deb https://anthony-s-personal-projects.github.io/orange-pi-zero-auto-temp-ctrl/ ./" | sudo tee /etc/apt/sources.list.d/auto-temp-ctrl.list

sudo apt update
sudo apt install auto-temp-ctrl
```

## Installation (Alternative - via .deb file)

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

## 3D Printable Case (STEP file and design)

A 3D printable case has been designed for the Orange Pi Zero with the fan mounted on top, ideal for projects using the Auto Temp Ctrl service.

<img src="3d model.JPG" alt="3D Case Model" width="400">

You can find the STEP file inside this repository or download it directly to print your own case for better airflow and protection of your Orange Pi Zero board.

## License

MIT License

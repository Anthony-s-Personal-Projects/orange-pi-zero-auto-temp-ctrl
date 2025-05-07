# Auto Temp Ctrl for Orange Pi Zero 🎉

Welcome to my first open-source project! 🚀  
This is a practice project to help me step into the open-source world, and I’m so excited to share it with you.

This project brings **automatic fan control** to your Orange Pi Zero, making sure your little powerhouse stays cool when needed — and goes silent when it's not.

It’s simple, useful, and I hope, just the beginning of many projects to come.

---

## 🎈 Installation (Recommended - via APT)

I've made it super easy for you to install and keep up to date. No fiddling around, just add my APT repo and you're good to go:

```bash
wget https://anthony-s-personal-projects.github.io/orange-pi-zero-auto-temp-ctrl/public.key
sudo apt-key add public.key

echo "deb https://anthony-s-personal-projects.github.io/orange-pi-zero-auto-temp-ctrl/ ./" | sudo tee /etc/apt/sources.list.d/auto-temp-ctrl.list

sudo apt update
sudo apt install auto-temp-ctrl
```

---

## 📦 Alternative Installation (Manual via .deb)

If you prefer the old school way or don't want to add the APT repo:

[📥 Download .deb file](https://github.com/Anthony-s-Personal-Projects/orange-pi-zero-auto-temp-ctrl/releases/download/v1.0/auto-temp-ctrl.deb)

Then install with:

```bash
sudo dpkg -i auto-temp-ctrl.deb
```

The installer will guide you if WiringOP is missing.

---

## 🚦 Usage

```bash
auto-temp-ctrl status
auto-temp-ctrl show
```

You can also tweak your fan behavior by editing:

```
/etc/auto-temp-ctrl.conf
```

---

## 🔥 Uninstallation

```bash
auto-temp-ctrl uninstall
```

This will clean up everything nicely.

---

## 🧰 3D Printable Case (STEP file and design)

Because keeping cool is not just for the CPU 😎.  
I've also designed a 3D printable case to make your Orange Pi Zero setup cleaner and safer.

<img src="3d model.JPG" alt="3D Case Model" width="400">

[📥 Download STEP File](https://github.com/Anthony-s-Personal-Projects/orange-pi-zero-auto-temp-ctrl/releases/download/v1.0/Orange-Pi-Zero-Case.step)

---

## 📌 Fan Wiring and Circuit Explanation

To safely control the fan using GPIO, a transistor and a flyback diode are used in the circuit.

### 🧠 Why use a Transistor?

GPIO pins can only provide very small currents and can't drive the fan directly.  
A **NPN Transistor** acts like a switch → controlled by GPIO.

- GPIO High → Transistor ON → Fan runs
- GPIO Low → Transistor OFF → Fan stops

The resistor (300Ω~1kΩ) limits the current flowing into the transistor's base → protecting GPIO.

### 🛡️ Why use a Flyback Diode?

When the fan turns OFF, it generates a reverse voltage (back EMF).  
This could damage the transistor or Orange Pi.

A **Flyback Diode** safely diverts this voltage away → protecting your circuit.

### 📊 Full Wiring Diagram

<img src="wiring description.png" alt="Fan Control Wiring Diagram" width="400">

**Pin usage example:**

- VCC-5V (Pin 4) → Fan +
- GND (Pin 6) → Fan GND via transistor
- PG6 (Pin 8) → Transistor control (via resistor)

---

## ❤️ Why this project?

This is my **first open-source project** and my journey to join this amazing community.  
I hope this will not only make your Orange Pi Zero run better but also inspire others (and myself) to keep building and sharing.

Thanks for checking this out — if you have ideas, issues, or want to improve it, pull requests and suggestions are welcome!

---

## 📜 License

MIT License — because open source should be open and free.

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

## 🔥 Uninstallation (if you ever want to remove it)

```bash
auto-temp-ctrl uninstall
```

This will clean up everything nice and tidy.

---

## 🧰 3D Printable Case (STEP file and design)

Because keeping cool is not just for the CPU 😎.  
I've also designed a 3D printable case to make your Orange Pi Zero setup cleaner and safer.

<img src="3d model.JPG" alt="3D Case Model" width="400">

[📥 Download STEP File](https://github.com/Anthony-s-Personal-Projects/orange-pi-zero-auto-temp-ctrl/releases/download/v1.0/Orange-Pi-Zero-Case.step)

You can print your own case for better airflow and protection of your Orange Pi Zero board.

---

## ❤️ Why this project?

This is my **first open-source project** and my journey to join this amazing community.  
I hope this will not only make your Orange Pi Zero run better but also inspire others (and myself) to keep building and sharing.

Thanks for checking this out — if you have ideas, issues, or want to improve it, pull requests and suggestions are welcome!

---

## 📜 License

MIT License — because open source should be open and free.

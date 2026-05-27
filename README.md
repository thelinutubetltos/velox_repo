# 🐧 Velox Repository

> Official package repository for **Velox Linux** — custom tools, wallpapers, and extras built for the Velox ecosystem.

---

## ⚡ Quick Install

Add the following to your `/etc/pacman.conf` **before** `[core]`:

```ini
[velox_repo]
SigLevel = Never
Server = https://thelinutubetltos.github.io/velox_repo/$arch
```

Then sync your package database:

```bash
sudo pacman -Sy
```

---

## 📦 Packages

| Package | Description | Status |
|---|---|---|
| `velox-wallpapers` | Official Velox Linux wallpapers | 🟢 Available |
| `velox-tools` | Velox system utilities and scripts | 🚧 Coming Soon |

---

## 🖼️ Wallpapers

Wallpapers are installed to `/usr/share/wallpapers/velox/` and are automatically available in KDE Plasma's wallpaper picker.

Install with:

```bash
sudo pacman -S velox-wallpapers
```

---

## 🔗 Links

- 🌐 [Velox Linux ISO Repository](https://github.com/thelinutubetltos/velox-iso)
- 📺 [The Linux Tube on YouTube](https://youtube.com/@thelinuxtube)

---

## 📋 For Maintainers

Packages are built with standard Arch Linux `makepkg` and added to the repo with:

```bash
repo-add velox_repo.db.tar.gz *.pkg.tar.zst
```

---

<div align="center">
  <sub>Built with ❤️ by The Linux Tube &nbsp;|&nbsp; Shape It. Race It. Own It.</sub>
</div>

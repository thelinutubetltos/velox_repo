# Velox Repository

> Official package repository for **Velox Linux** — custom packages, wallpapers, kernel, and tools built for the Velox ecosystem.

---

## Repositories

Velox Linux uses two package repositories depending on file size.

### velox_repo — GitHub Pages (small packages)

Add to `/etc/pacman.conf`:

```ini
[velox_repo]
SigLevel = Never
Server = https://thelinutubetltos.github.io/velox_repo/$arch
```

### velox-packages — GitHub Releases (large packages)

Add to `/etc/pacman.conf`:

```ini
[velox-packages]
SigLevel = Never
Server = https://github.com/thelinutubetltos/velox_repo/releases/download/velox-packages
```

Then sync:

```bash
sudo pacman -Sy
```

---

## Packages

### velox_repo (GitHub Pages)

| Package | Description | Status |
|---|---|---|
| `velox-wallpapers` | Official Velox Linux wallpaper pack (Velox-1 through Velox-7) | Available |
| `velox-welcome` | Velox welcome app — first-boot setup, app installer, kernel manager | Available |

### velox-packages (GitHub Releases)

| Package | Description | Status |
|---|---|---|
| `linux-velox` | Custom performance-tuned Velox kernel (CachyOS base) | Available |
| `linux-velox-headers` | Headers for linux-velox | Available |
| `calamares` | Distribution installer framework | Available |

---

## Wallpapers

Wallpapers are installed to `/usr/share/wallpapers/` and automatically appear in KDE Plasma's wallpaper picker.

```bash
sudo pacman -S velox-wallpapers
```

---

## velox-welcome

The Velox welcome app launches on first boot and includes:
- System update shortcut
- One-click app installation (Gaming, Creative, Internet, Browsers)
- Kernel manager
- Snapper + grub-btrfs snapshot setup
- Package search (pacman, Chaotic-AUR, AUR, Flatpak)
- Autostart toggle

```bash
sudo pacman -S velox-welcome
```

---

## linux-velox Kernel

A custom performance-tuned kernel based on the CachyOS kernel patchset, built specifically for Velox Linux. Includes scheduler optimizations and performance tweaks beyond the stock Arch kernel.

```bash
sudo pacman -S linux-velox linux-velox-headers
```

---

## For Maintainers

### Adding packages to velox_repo (GitHub Pages)

```bash
repo-add velox_repo.db.tar.gz package.pkg.tar.zst
# commit and push — GitHub Pages serves automatically
```

### Adding packages to velox-packages (GitHub Releases)

```bash
repo-add velox-packages.db.tar.gz package.pkg.tar.zst
gh release upload velox-packages --repo thelinutubetltos/velox_repo \
  package.pkg.tar.zst velox-packages.db.tar.gz velox-packages.db \
  velox-packages.files.tar.gz velox-packages.files --clobber
```

---

## Links

- [Velox Linux ISO](https://github.com/thelinutubetltos/velox-iso)
- [Download on SourceForge](https://sourceforge.net/projects/velox-linux/)
- [The Linux Tube on YouTube](https://youtube.com/@thelinuxtube)

---

<div align="center">
  <sub>Built by The Linux Tube &nbsp;|&nbsp; Shape It. Race It. Own It.</sub>
</div>

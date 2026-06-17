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
| `velox-pkgcheck` | PKGBUILD supply-chain attack scanner + `aur-install` wrapper | Available |

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

## velox-pkgcheck

A supply-chain attack scanner that inspects AUR PKGBUILDs **before** installation, protecting against attacks like the [Atomic Arch campaign (June 2026)](https://www.privacyguides.org/news/2026/06/12/around-1-500-aur-packages-compromised-with-rootkit-like-malware/) — where 1,500+ AUR packages were poisoned with an eBPF rootkit and credential stealer.

```bash
sudo pacman -S velox-pkgcheck
```

Installs two tools: `velox-pkgcheck` (the scanner) and `aur-install` (a paru/yay wrapper).

### aur-install

A drop-in replacement for `paru` or `yay` that automatically scans PKGBUILDs before installing anything. Auto-detects whichever AUR helper you have installed at runtime — switching helpers later keeps you protected.

```bash
# Use instead of paru/yay for AUR installs
aur-install some-package
aur-install some-package another-package

# All paru/yay flags pass through unchanged
aur-install --noconfirm some-package

# Non-install operations (search, query, remove, upgrade) pass straight through
aur-install -Syu
aur-install -Ss firefox
```

**What happens on install:**

| Result | Action |
|---|---|
| Clean / Info | Proceeds automatically |
| Medium | Prints warning, proceeds |
| High | Prompts "Install anyway? [y/N]" |
| Critical | **Blocked** — known malicious content detected |

Use `--no-check` to bypass the scan if you know what you're doing.

### velox-pkgcheck

The underlying scanner — use it standalone to inspect any PKGBUILD before installing.

```bash
# Scan a specific PKGBUILD
velox-pkgcheck ~/path/to/PKGBUILD

# Scan all PKGBUILDs in your paru/yay cache at once
velox-pkgcheck --scan-aur-cache

# Check installed AUR packages against the Atomic Arch attack window
velox-pkgcheck --scan-installed

# Check if your system is already compromised (eBPF artifacts, npm/bun cache, systemd services)
velox-pkgcheck --check-system
```

**Severity levels:**

| Level | Triggers |
|---|---|
| `CRITICAL` | Known malicious npm/bun packages (`atomic-lockfile`, `js-digest`, etc.) or known attacker AUR accounts |
| `HIGH` | `npm install` in PKGBUILD, `curl \| bash`, `eval "$(…)"`, base64-decoded payloads, temp-dir droppers |
| `MEDIUM` | `pip/gem install`, non-HTTPS source URLs, undeclared network downloads, eBPF ops |
| `INFO` | npm build steps — likely fine, flagged for awareness |

Exit codes map to severity (0 = clean, 4 = critical), so the tool integrates cleanly into scripts and CI.

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

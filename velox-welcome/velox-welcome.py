#!/usr/bin/env python3
import sys
import subprocess
import os
import shutil
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QGridLayout,
    QMessageBox, QTabWidget, QCheckBox, QLineEdit, QListWidget, QListWidgetItem,
    QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

VELOX_GREEN = "#3a5228"
VELOX_GREEN_HI = "#5a8160"
VELOX_RED = "#8a1a1a"
DARK_BG = "#1a1a1a"
DARKER_BG = "#141414"
CARD_BG = "#232323"
TEXT_COLOR = "#d4d4d4"

STYLE = f"""
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_COLOR};
    font-family: 'Noto Sans';
}}
QTabWidget::pane {{
    border: 1px solid {VELOX_GREEN};
    background-color: {DARK_BG};
}}
QTabBar::tab {{
    background-color: {DARKER_BG};
    color: {TEXT_COLOR};
    padding: 10px 20px;
    border: 1px solid #333;
}}
QTabBar::tab:selected {{
    background-color: {VELOX_GREEN};
    color: white;
    font-weight: bold;
}}
QPushButton {{
    background-color: {CARD_BG};
    color: {TEXT_COLOR};
    border: 1px solid {VELOX_GREEN};
    border-radius: 6px;
    padding: 10px;
    font-size: 13px;
    text-align: left;
}}
QPushButton:hover {{
    background-color: {VELOX_GREEN};
    color: white;
}}
QPushButton:pressed {{
    background-color: #2a3d1e;
}}
QPushButton#danger {{
    border-color: {VELOX_RED};
}}
QPushButton#danger:hover {{
    background-color: {VELOX_RED};
}}
QPushButton#install {{
    background-color: {VELOX_GREEN};
    color: white;
    font-weight: bold;
    text-align: center;
}}
QPushButton#install:hover {{
    background-color: {VELOX_GREEN_HI};
}}
QPushButton#install:disabled {{
    background-color: #2a2a2a;
    color: #555;
    border-color: #333;
}}
QScrollArea {{
    border: none;
    background-color: {DARK_BG};
}}
QLabel#header {{
    font-size: 28px;
    font-weight: bold;
    color: white;
}}
QLabel#tagline {{
    font-size: 14px;
    color: {VELOX_GREEN_HI};
}}
QLabel#section {{
    font-size: 16px;
    font-weight: bold;
    color: {VELOX_GREEN_HI};
    padding: 10px 0px 5px 0px;
}}
QFrame#card {{
    background-color: {CARD_BG};
    border-radius: 8px;
    border: 1px solid #333;
}}
QCheckBox {{
    color: {TEXT_COLOR};
    font-size: 13px;
    padding: 6px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {VELOX_GREEN};
    border-radius: 3px;
    background-color: {DARKER_BG};
}}
QCheckBox::indicator:checked {{
    background-color: {VELOX_GREEN};
}}
QLineEdit {{
    background-color: {DARKER_BG};
    color: {TEXT_COLOR};
    border: 1px solid {VELOX_GREEN};
    border-radius: 6px;
    padding: 8px;
    font-size: 13px;
}}
QComboBox {{
    background-color: {DARKER_BG};
    color: {TEXT_COLOR};
    border: 1px solid {VELOX_GREEN};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    min-height: 36px;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background-color: {DARKER_BG};
    color: {TEXT_COLOR};
    border: 1px solid {VELOX_GREEN};
    selection-background-color: {VELOX_GREEN};
}}
QListWidget {{
    background-color: {DARKER_BG};
    color: {TEXT_COLOR};
    border: 1px solid #333;
    border-radius: 6px;
    font-size: 13px;
}}
QListWidget::item {{
    padding: 8px;
    border-bottom: 1px solid #2a2a2a;
}}
QListWidget::item:selected {{
    background-color: {VELOX_GREEN};
    color: white;
}}
QListWidget::item:hover {{
    background-color: #2a3d1e;
}}
"""

def has_cmd(cmd):
    return subprocess.run(["which", cmd], capture_output=True).returncode == 0

def get_aur_helper():
    if has_cmd("paru"):
        return "paru"
    if has_cmd("yay"):
        return "yay"
    return None

class SearchThread(QThread):
    results_ready = pyqtSignal(list)

    def __init__(self, query, source):
        super().__init__()
        self.query = query
        self.source = source  # "pacman", "aur", "flatpak"

    def run(self):
        packages = []
        try:
            if self.source == "flatpak":
                result = subprocess.run(
                    ["flatpak", "search", "--columns=application,name,description", self.query],
                    capture_output=True, text=True, timeout=20
                )
                for line in result.stdout.strip().split('\n')[1:]:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        app_id = parts[0].strip()
                        name = parts[1].strip() if len(parts) > 1 else app_id
                        desc = parts[2].strip() if len(parts) > 2 else ""
                        packages.append((app_id, name, desc, "flatpak"))
            elif self.source == "aur":
                helper = get_aur_helper()
                if helper:
                    result = subprocess.run(
                        [helper, "-Ss", "--aur", self.query],
                        capture_output=True, text=True, timeout=20
                    )
                    packages = self._parse_pacman_output(result.stdout, "aur")
            else:  # pacman + chaotic
                result = subprocess.run(
                    ["pacman", "-Ss", self.query],
                    capture_output=True, text=True, timeout=15
                )
                packages = self._parse_pacman_output(result.stdout, "pacman")
        except Exception:
            pass
        self.results_ready.emit(packages[:60])

    def _parse_pacman_output(self, output, source):
        packages = []
        lines = output.strip().split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            if line and not line.startswith(' ') and not line.startswith('\t'):
                parts = line.split('/')
                if len(parts) >= 2:
                    name_ver = parts[-1].split(' ')[0]
                    desc = lines[i+1].strip() if i+1 < len(lines) else ""
                    repo = parts[0] if len(parts) > 1 else source
                    packages.append((name_ver, name_ver, desc, f"{source}:{repo}"))
            i += 1
        return packages


class WorkerThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            result = subprocess.run(
                self.command, shell=True, capture_output=True, text=True
            )
            self.finished.emit(result.returncode == 0, result.stdout + result.stderr)
        except Exception as e:
            self.finished.emit(False, str(e))


class VeloxWelcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Velox Linux")
        self.setMinimumSize(920, 720)
        self.setStyleSheet(STYLE)
        self.autostart_path = Path.home() / ".config/autostart/velox-welcome.desktop"
        self.search_thread = None
        self.selected_pkg = None
        self.selected_source = None
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setStyleSheet(f"background-color: {DARKER_BG}; border-bottom: 2px solid {VELOX_GREEN};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)

        logo_label = QLabel()
        logo_path = "/usr/share/velox-welcome/velox-logo.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(120, 80, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        title = QLabel("Welcome to Velox Linux")
        title.setObjectName("header")
        tagline = QLabel("Shape It. Race It. Own It.")
        tagline.setObjectName("tagline")
        title_layout.addWidget(title)
        title_layout.addWidget(tagline)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        main_layout.addWidget(header)

        tabs = QTabWidget()
        tabs.setContentsMargins(10, 10, 10, 10)
        tabs.addTab(self.create_firstSteps_tab(), "🚀 First Steps")
        tabs.addTab(self.create_gaming_tab(), "🎮 Gaming")
        tabs.addTab(self.create_creative_tab(), "🎨 Creative")
        tabs.addTab(self.create_internet_tab(), "🌐 Internet")
        tabs.addTab(self.create_kernel_tab(), "⚙ Kernels")
        tabs.addTab(self.create_snapper_tab(), "📸 Snapshots")
        tabs.addTab(self.create_package_tab(), "📦 Packages")
        tabs.addTab(self.create_about_tab(), "ℹ About")
        main_layout.addWidget(tabs)

    def create_scroll_tab(self):
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
        return outer, tab

    def add_section_label(self, layout, text):
        label = QLabel(text)
        label.setObjectName("section")
        layout.addWidget(label)

    def make_button(self, text, callback, danger=False, install=False):
        btn = QPushButton(text)
        if danger:
            btn.setObjectName("danger")
        elif install:
            btn.setObjectName("install")
        btn.clicked.connect(callback)
        btn.setMinimumHeight(45)
        return btn

    def run_terminal_command(self, command, title="Running..."):
        reply = QMessageBox.question(self, title,
            f"Run the following command?\n\n{command}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            subprocess.Popen(["konsole", "-e", "bash", "-c",
                f"{command}; echo; echo 'Done. Press Enter to close...'; read"])

    def install_package(self, package):
        helper = get_aur_helper()
        cmd = f"{helper} -S --needed {package}" if helper else f"sudo pacman -S --needed {package}"
        self.run_terminal_command(cmd, f"Install {package}")

    def toggle_autostart(self, state):
        if state:
            src = Path("/usr/share/applications/velox-welcome.desktop")
            self.autostart_path.parent.mkdir(parents=True, exist_ok=True)
            if src.exists():
                shutil.copy2(src, self.autostart_path)
            else:
                self.autostart_path.write_text(
                    "[Desktop Entry]\nType=Application\nName=Velox Welcome\n"
                    "Exec=velox-welcome\nTerminal=false\nHidden=false\n"
                    "X-KDE-autostart-phase=2\n"
                )
        else:
            if self.autostart_path.exists():
                self.autostart_path.unlink()

    # ── First Steps ──────────────────────────────────────────
    def create_firstSteps_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "⚙ Welcome App")
        autostart_cb = QCheckBox("Launch Welcome on login")
        autostart_cb.setChecked(self.autostart_path.exists())
        autostart_cb.stateChanged.connect(self.toggle_autostart)
        layout.addWidget(autostart_cb)

        self.add_section_label(layout, "🔄 System")
        layout.addWidget(self.make_button("Update System",
            lambda: self.run_terminal_command("sudo pacman -Syu")))
        layout.addWidget(self.make_button("Update AUR Packages",
            lambda: self.run_terminal_command(f"{get_aur_helper() or 'paru'} -Syu")))
        layout.addWidget(self.make_button("Clean Package Cache",
            lambda: self.run_terminal_command("sudo pacman -Sc")))

        self.add_section_label(layout, "🎨 Appearance")
        layout.addWidget(self.make_button("Apply Kvantum Dark Theme",
            lambda: self.run_terminal_command("kvantummanager --set Velox")))
        layout.addWidget(self.make_button("Open Kvantum Manager",
            lambda: subprocess.Popen(["kvantummanager"])))
        layout.addWidget(self.make_button("Open System Settings",
            lambda: subprocess.Popen(["systemsettings"])))

        self.add_section_label(layout, "🖥 Display")
        layout.addWidget(self.make_button("Install NVIDIA Drivers (proprietary)",
            lambda: self.install_package("nvidia-open-dkms nvidia-utils nvidia-settings")))
        layout.addWidget(self.make_button("Install AMD Drivers",
            lambda: self.install_package("mesa vulkan-radeon libva-mesa-driver")))

        self.add_section_label(layout, "🔧 System Tools")
        layout.addWidget(self.make_button("Enable Timeshift (Backups)",
            lambda: self.install_package("timeshift")))
        layout.addWidget(self.make_button("Enable Firewall (UFW)",
            lambda: self.run_terminal_command(
                "sudo pacman -S --needed ufw && sudo ufw enable && sudo systemctl enable ufw")))
        layout.addWidget(self.make_button("Enable Bluetooth",
            lambda: self.run_terminal_command("sudo systemctl enable --now bluetooth")))
        layout.addWidget(self.make_button("Enable Flatpak Support",
            lambda: self.run_terminal_command(
                "sudo pacman -S --needed flatpak && "
                "flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo")))

        layout.addStretch()
        return outer

    # ── Gaming ───────────────────────────────────────────────
    def create_gaming_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "🎮 Game Launchers")
        layout.addWidget(self.make_button("Install Steam",
            lambda: self.install_package("steam")))
        layout.addWidget(self.make_button("Install Lutris",
            lambda: self.install_package("lutris")))
        layout.addWidget(self.make_button("Install Heroic Games Launcher",
            lambda: self.install_package("heroic-games-launcher-bin")))
        layout.addWidget(self.make_button("Install Bottles",
            lambda: self.install_package("bottles")))

        self.add_section_label(layout, "⚡ Performance")
        layout.addWidget(self.make_button("Install GameMode",
            lambda: self.install_package("gamemode lib32-gamemode")))
        layout.addWidget(self.make_button("Install MangoHud",
            lambda: self.install_package("mangohud lib32-mangohud")))
        layout.addWidget(self.make_button("Install ProtonUp-Qt",
            lambda: self.install_package("protonup-qt")))
        layout.addWidget(self.make_button("Install Wine",
            lambda: self.install_package("wine wine-mono wine-gecko")))

        self.add_section_label(layout, "💬 Communication")
        layout.addWidget(self.make_button("Install Discord",
            lambda: self.install_package("discord")))
        layout.addWidget(self.make_button("Install TeamSpeak",
            lambda: self.install_package("teamspeak3")))

        layout.addStretch()
        return outer

    # ── Creative ─────────────────────────────────────────────
    def create_creative_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "🎬 Video")
        layout.addWidget(self.make_button("Install Kdenlive",
            lambda: self.install_package("kdenlive")))
        layout.addWidget(self.make_button("Install OBS Studio",
            lambda: self.install_package("obs-studio")))
        layout.addWidget(self.make_button("Install Handbrake",
            lambda: self.install_package("handbrake")))
        layout.addWidget(self.make_button("Install DaVinci Resolve",
            lambda: self.install_package("davinci-resolve")))

        self.add_section_label(layout, "🖼 Graphics")
        layout.addWidget(self.make_button("Install GIMP",
            lambda: self.install_package("gimp")))
        layout.addWidget(self.make_button("Install Inkscape",
            lambda: self.install_package("inkscape")))
        layout.addWidget(self.make_button("Install Krita",
            lambda: self.install_package("krita")))
        layout.addWidget(self.make_button("Install Blender",
            lambda: self.install_package("blender")))

        self.add_section_label(layout, "🎵 Audio")
        layout.addWidget(self.make_button("Install Audacity",
            lambda: self.install_package("audacity")))
        layout.addWidget(self.make_button("Install Ardour",
            lambda: self.install_package("ardour")))

        layout.addStretch()
        return outer

    # ── Internet ─────────────────────────────────────────────
    def create_internet_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "🌐 Browsers")
        layout.addWidget(self.make_button("Install Google Chrome",
            lambda: self.install_package("google-chrome")))
        layout.addWidget(self.make_button("Install Brave",
            lambda: self.install_package("brave-bin")))
        layout.addWidget(self.make_button("Install Chromium",
            lambda: self.install_package("chromium")))

        self.add_section_label(layout, "💬 Messaging")
        layout.addWidget(self.make_button("Install Telegram",
            lambda: self.install_package("telegram-desktop")))
        layout.addWidget(self.make_button("Install Signal",
            lambda: self.install_package("signal-desktop")))
        layout.addWidget(self.make_button("Install Element (Matrix)",
            lambda: self.install_package("element-desktop")))

        self.add_section_label(layout, "🎵 Media")
        layout.addWidget(self.make_button("Install Spotify",
            lambda: self.install_package("spotify")))
        layout.addWidget(self.make_button("Install Freetube",
            lambda: self.install_package("freetube-bin")))

        self.add_section_label(layout, "☁ Cloud")
        layout.addWidget(self.make_button("Install Nextcloud Client",
            lambda: self.install_package("nextcloud-client")))
        layout.addWidget(self.make_button("Install Dropbox",
            lambda: self.install_package("dropbox")))

        layout.addStretch()
        return outer

    # ── Kernels ──────────────────────────────────────────────
    def create_kernel_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "🐧 Standard Kernels")
        layout.addWidget(self.make_button("Install linux (default)",
            lambda: self.install_package("linux linux-headers")))
        layout.addWidget(self.make_button("Install linux-lts (Long Term Support)",
            lambda: self.install_package("linux-lts linux-lts-headers")))
        layout.addWidget(self.make_button("Install linux-zen (Desktop Optimized)",
            lambda: self.install_package("linux-zen linux-zen-headers")))
        layout.addWidget(self.make_button("Install linux-hardened (Security)",
            lambda: self.install_package("linux-hardened linux-hardened-headers")))

        self.add_section_label(layout, "⚡ Performance Kernels")
        layout.addWidget(self.make_button("Install linux-cachyos (CachyOS Optimized)",
            lambda: self.install_package("linux-cachyos linux-cachyos-headers")))
        layout.addWidget(self.make_button("Install linux-cachyos-bore (BORE Scheduler)",
            lambda: self.install_package("linux-cachyos-bore linux-cachyos-bore-headers")))
        layout.addWidget(self.make_button("Install linux-xanmod (Xanmod Optimized)",
            lambda: self.install_package("linux-xanmod")))

        self.add_section_label(layout, "⚠ After Installing a New Kernel")
        layout.addWidget(self.make_button("Update GRUB",
            lambda: self.run_terminal_command("sudo grub-mkconfig -o /boot/grub/grub.cfg")))

        layout.addStretch()
        return outer

    # ── Snapper ──────────────────────────────────────────────
    def create_snapper_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "📸 Snapper + GRUB Snapshots")
        info = QLabel(
            "Snapper automatically saves Btrfs snapshots before and after system changes.\n"
            "grub-btrfs makes snapshots bootable from the GRUB menu."
        )
        info.setStyleSheet("color: #888; font-size: 13px; padding: 4px 0px 10px 0px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.snapper_status = QLabel()
        self.snapper_status.setStyleSheet("font-size: 12px; padding: 4px 0px;")
        layout.addWidget(self.snapper_status)
        self.refresh_snapper_status()

        self.add_section_label(layout, "⚙ Setup")
        layout.addWidget(self.make_button("📦 Install Snapper + grub-btrfs",
            lambda: self.run_terminal_command(
                "paru -S --needed snapper grub-btrfs inotify-tools")))
        layout.addWidget(self.make_button("🔧 Create Snapper config for root",
            lambda: self.run_terminal_command(
                "sudo snapper -c root create-config / && "
                "sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer")))
        layout.addWidget(self.make_button("🔄 Enable grub-btrfs auto-update",
            lambda: self.run_terminal_command(
                "sudo systemctl enable --now grub-btrfsd && "
                "sudo grub-mkconfig -o /boot/grub/grub.cfg")))

        self.add_section_label(layout, "📷 Manual Snapshots")
        layout.addWidget(self.make_button("Take snapshot now",
            lambda: self.run_terminal_command(
                "sudo snapper -c root create --description 'Manual snapshot'")))
        layout.addWidget(self.make_button("List snapshots",
            lambda: self.run_terminal_command("snapper -c root list")))
        layout.addWidget(self.make_button("Delete old snapshots (keep last 5)",
            lambda: self.run_terminal_command("sudo snapper -c root cleanup number")))

        layout.addStretch()
        return outer

    def refresh_snapper_status(self):
        snapper_ok = has_cmd("snapper")
        config_ok = Path("/etc/snapper/configs/root").exists()
        grub_ok = has_cmd("grub-btrfsd")
        if snapper_ok and config_ok and grub_ok:
            self.snapper_status.setText("✅ Snapper is configured and active")
            self.snapper_status.setStyleSheet("color: #5a8160; font-size: 12px; padding: 4px 0px;")
        elif snapper_ok:
            self.snapper_status.setText("⚠ Snapper installed but not configured — run Setup steps below")
            self.snapper_status.setStyleSheet("color: #cc8800; font-size: 12px; padding: 4px 0px;")
        else:
            self.snapper_status.setText("❌ Snapper not installed — run Setup steps below")
            self.snapper_status.setStyleSheet("color: #8a1a1a; font-size: 12px; padding: 4px 0px;")

    # ── Package Search ───────────────────────────────────────
    def create_package_tab(self):
        outer = QWidget()
        layout = QVBoxLayout(outer)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "📦 Package Search & Install")

        # Backend status bar
        status_row = QHBoxLayout()
        helper = get_aur_helper()
        flatpak_ok = has_cmd("flatpak")
        chaotic_ok = Path("/etc/pacman.d/chaotic-mirrorlist").exists()

        def status_badge(label, ok):
            lbl = QLabel(f"{'✅' if ok else '❌'} {label}")
            lbl.setStyleSheet(f"color: {'#5a8160' if ok else '#8a1a1a'}; font-size: 11px; padding: 2px 8px;")
            return lbl

        status_row.addWidget(status_badge(f"AUR Helper ({helper or 'none'})", helper is not None))
        status_row.addWidget(status_badge("Chaotic-AUR", chaotic_ok))
        status_row.addWidget(status_badge("Flatpak", flatpak_ok))
        status_row.addStretch()
        layout.addLayout(status_row)

        # Source selector + search bar
        search_row = QHBoxLayout()
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Pacman + Chaotic-AUR", "AUR", "Flatpak"])
        self.source_combo.setMaximumWidth(200)
        search_row.addWidget(self.source_combo)

        self.pkg_search_box = QLineEdit()
        self.pkg_search_box.setPlaceholderText("Search packages...")
        self.pkg_search_box.returnPressed.connect(self.search_packages)
        search_row.addWidget(self.pkg_search_box)

        search_btn = QPushButton("🔍 Search")
        search_btn.setMinimumHeight(40)
        search_btn.setMaximumWidth(110)
        search_btn.clicked.connect(self.search_packages)
        search_row.addWidget(search_btn)
        layout.addLayout(search_row)

        # Status label
        self.pkg_status = QLabel("Select a source and enter a search term")
        self.pkg_status.setStyleSheet("color: #666; font-size: 12px; padding: 2px 0px;")
        layout.addWidget(self.pkg_status)

        # Results
        self.pkg_list = QListWidget()
        self.pkg_list.itemSelectionChanged.connect(self.on_package_selected)
        layout.addWidget(self.pkg_list)

        # Description
        self.pkg_desc = QLabel("")
        self.pkg_desc.setStyleSheet("color: #888; font-size: 12px; padding: 4px 0px;")
        self.pkg_desc.setWordWrap(True)
        layout.addWidget(self.pkg_desc)

        # Install button
        self.pkg_install_btn = QPushButton("📦 Select a package to install")
        self.pkg_install_btn.setObjectName("install")
        self.pkg_install_btn.setMinimumHeight(45)
        self.pkg_install_btn.setEnabled(False)
        self.pkg_install_btn.clicked.connect(self.install_selected_package)
        layout.addWidget(self.pkg_install_btn)

        # Setup buttons if tools missing
        if not helper:
            layout.addWidget(self.make_button("⚠ Install paru (AUR helper)",
                lambda: self.run_terminal_command(
                    "sudo pacman -S --needed base-devel && "
                    "git clone https://aur.archlinux.org/paru.git /tmp/paru && "
                    "cd /tmp/paru && makepkg -si")))
        if not flatpak_ok:
            layout.addWidget(self.make_button("⚠ Enable Flatpak",
                lambda: self.run_terminal_command(
                    "sudo pacman -S --needed flatpak && "
                    "flatpak remote-add --if-not-exists flathub "
                    "https://dl.flathub.org/repo/flathub.flatpakrepo")))

        return outer

    def search_packages(self):
        query = self.pkg_search_box.text().strip()
        if not query:
            return
        source_map = {0: "pacman", 1: "aur", 2: "flatpak"}
        source = source_map.get(self.source_combo.currentIndex(), "pacman")
        self.pkg_status.setText(f"Searching '{query}' in {self.source_combo.currentText()}...")
        self.pkg_list.clear()
        self.pkg_desc.setText("")
        self.pkg_install_btn.setEnabled(False)
        self.pkg_install_btn.setText("📦 Select a package to install")
        self.search_thread = SearchThread(query, source)
        self.search_thread.results_ready.connect(self.on_search_results)
        self.search_thread.start()

    def on_search_results(self, packages):
        self.pkg_list.clear()
        if not packages:
            self.pkg_status.setText("No results found.")
            return
        self.pkg_status.setText(f"{len(packages)} results found")
        for pkg_id, name, desc, source in packages:
            item = QListWidgetItem(f"{name}  [{source}]")
            item.setData(Qt.ItemDataRole.UserRole, (pkg_id, desc, source))
            self.pkg_list.addItem(item)

    def on_package_selected(self):
        items = self.pkg_list.selectedItems()
        if items:
            pkg_id, desc, source = items[0].data(Qt.ItemDataRole.UserRole)
            self.selected_pkg = pkg_id
            self.selected_source = source
            self.pkg_desc.setText(desc)
            self.pkg_install_btn.setEnabled(True)
            self.pkg_install_btn.setText(f"📦 Install {pkg_id}")

    def install_selected_package(self):
        if not self.selected_pkg:
            return
        if self.selected_source == "flatpak":
            self.run_terminal_command(
                f"flatpak install flathub {self.selected_pkg}",
                f"Install {self.selected_pkg}")
        else:
            self.install_package(self.selected_pkg)

    # ── About ────────────────────────────────────────────────
    def create_about_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "About Velox Linux")
        about = QLabel(
            "Velox Linux is an Arch-based KDE Plasma distribution focused on\n"
            "performance, customization, and a great out-of-the-box experience.\n\n"
            "Built by The Linux Tube for creators, gamers, and power users."
        )
        about.setStyleSheet("color: #aaaaaa; font-size: 14px; padding: 10px;")
        about.setWordWrap(True)
        layout.addWidget(about)

        self.add_section_label(layout, "🔗 Links")
        layout.addWidget(self.make_button("🐙 GitHub Repository",
            lambda: subprocess.Popen(["xdg-open", "https://github.com/thelinutubetltos/velox-iso"])))
        layout.addWidget(self.make_button("📺 YouTube Channel",
            lambda: subprocess.Popen(["xdg-open", "https://youtube.com/@thelinuxtube"])))
        layout.addWidget(self.make_button("🐛 Report a Bug",
            lambda: subprocess.Popen(["xdg-open", "https://github.com/thelinutubetltos/velox-iso/issues"])))
        layout.addWidget(self.make_button("📦 Velox Repository",
            lambda: subprocess.Popen(["xdg-open", "https://github.com/thelinutubetltos/velox_repo"])))

        layout.addStretch()
        return outer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Velox Welcome")
    window = VeloxWelcome()
    window.show()
    sys.exit(app.exec())

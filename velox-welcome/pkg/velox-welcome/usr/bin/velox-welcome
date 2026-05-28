#!/usr/bin/env python3
import sys
import subprocess
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QGridLayout,
    QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette

VELOX_GREEN = "#5a8160"
VELOX_RED = "#cc3333"
DARK_BG = "#1a1a1a"
DARKER_BG = "#141414"
CARD_BG = "#232323"
TEXT_COLOR = "#ffffff"

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
    background-color: #3d5c40;
}}
QPushButton#danger {{
    border-color: {VELOX_RED};
}}
QPushButton#danger:hover {{
    background-color: {VELOX_RED};
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
    color: {VELOX_GREEN};
}}
QLabel#section {{
    font-size: 16px;
    font-weight: bold;
    color: {VELOX_GREEN};
    padding: 10px 0px 5px 0px;
}}
QFrame#card {{
    background-color: {CARD_BG};
    border-radius: 8px;
    border: 1px solid #333;
}}
"""

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
        self.setMinimumSize(900, 700)
        self.setStyleSheet(STYLE)
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

        # Logo
        logo_label = QLabel()
        logo_path = "/usr/share/velox-welcome/velox-logo.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(120, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        # Title
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

        # Tabs
        tabs = QTabWidget()
        tabs.setContentsMargins(10, 10, 10, 10)
        tabs.addTab(self.create_firstSteps_tab(), "🚀 First Steps")
        tabs.addTab(self.create_gaming_tab(), "🎮 Gaming")
        tabs.addTab(self.create_creative_tab(), "🎨 Creative")
        tabs.addTab(self.create_internet_tab(), "🌐 Internet")
        tabs.addTab(self.create_kernel_tab(), "⚙️ Kernels")
        tabs.addTab(self.create_about_tab(), "ℹ️ About")
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

    def make_button(self, text, callback, danger=False):
        btn = QPushButton(text)
        if danger:
            btn.setObjectName("danger")
        btn.clicked.connect(callback)
        btn.setMinimumHeight(45)
        return btn

    def run_terminal_command(self, command, title="Running..."):
        reply = QMessageBox.question(self, title, 
            f"Run the following command?\n\n{command}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            subprocess.Popen(["konsole", "-e", "bash", "-c", f"{command}; echo 'Press Enter to close...'; read"])

    def install_package(self, package):
        self.run_terminal_command(f"paru -S --needed {package}", f"Install {package}")

    # ── First Steps Tab ──────────────────────────────────────
    def create_firstSteps_tab(self):
        outer, tab = self.create_scroll_tab()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.add_section_label(layout, "🔄 System")
        layout.addWidget(self.make_button("Update System", 
            lambda: self.run_terminal_command("sudo pacman -Syu")))
        layout.addWidget(self.make_button("Update AUR Packages", 
            lambda: self.run_terminal_command("paru -Syu")))
        layout.addWidget(self.make_button("Clean Package Cache", 
            lambda: self.run_terminal_command("sudo pacman -Sc")))

        self.add_section_label(layout, "🎨 Appearance")
        layout.addWidget(self.make_button("Apply Kvantum Dark Theme", 
            lambda: self.run_terminal_command("kvantummanager --set Velox")))
        layout.addWidget(self.make_button("Open Kvantum Manager", 
            lambda: subprocess.Popen(["kvantummanager"])))
        layout.addWidget(self.make_button("Open System Settings", 
            lambda: subprocess.Popen(["systemsettings"])))

        self.add_section_label(layout, "🖥️ Display")
        layout.addWidget(self.make_button("Install NVIDIA Drivers (proprietary)", 
            lambda: self.install_package("nvidia-open-dkms nvidia-utils nvidia-settings")))
        layout.addWidget(self.make_button("Install AMD Drivers", 
            lambda: self.install_package("mesa vulkan-radeon libva-mesa-driver")))

        self.add_section_label(layout, "🔧 System Tools")
        layout.addWidget(self.make_button("Enable Timeshift (Backups)", 
            lambda: self.install_package("timeshift")))
        layout.addWidget(self.make_button("Enable Firewall (UFW)", 
            lambda: self.run_terminal_command("sudo pacman -S --needed ufw && sudo ufw enable && sudo systemctl enable ufw")))
        layout.addWidget(self.make_button("Enable Bluetooth", 
            lambda: self.run_terminal_command("sudo systemctl enable --now bluetooth")))

        layout.addStretch()
        return outer

    # ── Gaming Tab ───────────────────────────────────────────
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

    # ── Creative Tab ─────────────────────────────────────────
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

        self.add_section_label(layout, "🖼️ Graphics")
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

    # ── Internet Tab ─────────────────────────────────────────
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

        self.add_section_label(layout, "☁️ Cloud")
        layout.addWidget(self.make_button("Install Nextcloud Client", 
            lambda: self.install_package("nextcloud-client")))
        layout.addWidget(self.make_button("Install Dropbox", 
            lambda: self.install_package("dropbox")))

        layout.addStretch()
        return outer

    # ── Kernel Tab ───────────────────────────────────────────
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
        layout.addWidget(self.make_button("Install linux-tkg-pds (TKG PDS Scheduler)", 
            lambda: self.install_package("linux-tkg-pds")))
        layout.addWidget(self.make_button("Install linux-xanmod (Xanmod Optimized)", 
            lambda: self.install_package("linux-xanmod")))

        self.add_section_label(layout, "⚠️ After Installing a New Kernel")
        layout.addWidget(self.make_button("Update GRUB", 
            lambda: self.run_terminal_command("sudo grub-mkconfig -o /boot/grub/grub.cfg")))

        layout.addStretch()
        return outer

    # ── About Tab ────────────────────────────────────────────
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

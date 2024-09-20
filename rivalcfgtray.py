import sys
import subprocess
import re
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the current script's directory
ICON_PATH = os.path.join(BASE_DIR, "rivalcfgbatt", "batticons")

def get_battery_status():
    """Run the rivalcfg command and get battery status."""
    try:
        # Run the command and get the output
        result = subprocess.run(['rivalcfg', '--battery-level'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def parse_battery_level(status):
    """Extract battery percentage and charging state from the status."""
    match = re.search(r'(Charging|Discharging)\s+\[.*\]\s+(\d+)\s*%', status)
    if match:
        charging_state = match.group(1) == "Charging"
        battery_level = int(match.group(2))
        return battery_level, charging_state
    return 0, False  # Default if no match found

def get_icon_for_battery_level(battery_level):
    """Return the appropriate icon based on battery level."""
    if battery_level >= 100:
        return QIcon(os.path.join(ICON_PATH, "battery_100.png"))
    elif battery_level >= 75:
        return QIcon(os.path.join(ICON_PATH, "battery_75.png"))
    elif battery_level >= 50:
        return QIcon(os.path.join(ICON_PATH, "battery_50.png"))
    elif battery_level >= 25:
        return QIcon(os.path.join(ICON_PATH, "battery_25.png"))
    else:
        return QIcon(os.path.join(ICON_PATH, "battery_empty.png"))

def update_battery_status(tray_icon):
    """Update the tray icon based on the battery status."""
    status = get_battery_status()
    print("Battery Status:", status)  # print the raw status

    battery_level, charging = parse_battery_level(status)
    print(f"Parsed Level: {battery_level}%, Charging: {'Yes' if charging else 'No'}")  # Debug parsed values

    # Get the appropriate icon based on battery level
    icon = get_icon_for_battery_level(battery_level)
    tray_icon.setIcon(icon)

    # Set tooltip with the mouse icon and battery level
    tooltip_text = f"🖱️ {'Charging' if charging else 'Discharging'}: {battery_level}%"
    tray_icon.setToolTip(tooltip_text)

def create_tray_icon():
    """Create the system tray icon with a menu."""
    app = QApplication(sys.argv)
    tray_icon = QSystemTrayIcon()
    
    # Initial battery status update
    update_battery_status(tray_icon)

    # Create a menu with an exit option
    menu = QMenu()
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)
    
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_battery_status(tray_icon))
    timer.start(600000)  # 10 minutes

    sys.exit(app.exec())

if __name__ == "__main__":
    create_tray_icon()

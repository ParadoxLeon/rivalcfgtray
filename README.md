git clone or download the repo and add it to you're autostart

### Example `rivalcfgtray.desktop`
```
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 10 && python3 /path/to/rivalcfgtray/rivalcfgtray.py"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Rivalcfg Tray
Comment=Run Rivalcfg battery tray application

```

## Required
[rivalcfg](https://github.com/flozz/rivalcfg), python and python-pyqt6

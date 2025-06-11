Hello,

This project is a little side project to learn and play with Python.
If you would like to try my latest update, please download the executable file `VillageDefense.exe` and enjoy!

Thanks,
Nick

## Building the Game

1. Build the game with PyInstaller:
```batch
python build.py
```

2. Compile the installer with Inno Setup:
```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "GameInstaller.iss"
```

The installer will be created in `installer/VillageDefenseSetup.exe`
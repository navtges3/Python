import os
import subprocess

# Define the main script and output file name
main_script = "main.py"  # Replace with the entry point of your game
output_name = "VillageDefense"  # Name of the output executable

# PyInstaller options
options = [
    # Using onedir (default) mode instead of onefile
    "--noconsole",  # Hide the console window (useful for GUI apps)
    "--icon=icon.ico",  # Path to your game icon
    "--noupx",  # Avoid using UPX compression to prevent antivirus false positives
    "--name", output_name,  # Name of the output executable
    "--add-data", "icon.ico;.",  # Include the icon file (adjust as needed)
    "--add-data", "images;images",  # Include images folder (adjust as needed)
    "--add-data", "music;music",  # Include sounds folder (adjust as needed)
]

# Build the command
command = ["pyinstaller"] + options + [main_script]

# Run the command
print("Running PyInstaller...")
subprocess.run(command, check=True)

# Clean up build files
print("Cleaning up temporary files...")
for folder in ["build", "__pycache__"]:
    if os.path.exists(folder):
        os.system(f"rmdir /s /q {folder}")  # Windows-specific command to remove directories
if os.path.exists(f"{output_name}.spec"):
    os.remove(f"{output_name}.spec")

print(f"Build complete! Executable is located in the 'dist' folder as {output_name}.exe")
import os
import platform
import subprocess
import shutil

def check_and_install_ffmpeg():
    ffmpeg_path = "/usr/bin/ffmpeg"
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg is already installed.")
        return
    except FileNotFoundError:
        print("FFmpeg not found. Installing via pacman...")

    # Check if the script is running on Arch Linux
    system = platform.system()
    if system != "Linux":
        raise RuntimeError(f"This script supports only Arch Linux. Your system: {system}")

    # Install FFmpeg using pacman
    try:
        subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "ffmpeg"], check=True)
        print("FFmpeg installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing FFmpeg: {e}")
        raise

if __name__ == "__main__":
    check_and_install_ffmpeg()

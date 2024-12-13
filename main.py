import importlib
import sys
import os
import subprocess

def check_and_activate_venv():
    """
    Kiểm tra nếu đang trong môi trường ảo.
    Nếu không, yêu cầu người dùng kích hoạt môi trường ảo.
    """
    if os.getenv("VIRTUAL_ENV") is None:
        print("Chương trình cần được chạy trong môi trường ảo (virtual environment).\n")
        print("Hãy tạo và kích hoạt môi trường ảo với các lệnh sau:")
        print("python -m venv myenv")
        print("source myenv/bin/activate")
        print("Sau đó chạy lại chương trình.")
        sys.exit(1)

def check_required_modules(required_modules):
    """
    Kiểm tra các module cần thiết đã được cài đặt chưa.
    Nếu chưa, in hướng dẫn cài đặt thủ công.
    """
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("\nCác module sau chưa được cài đặt:")
        for module in missing_modules:
            print(f"- {module}")

        print("\nHãy cài đặt chúng trong môi trường ảo bằng lệnh:")
        print("pip install " + " ".join(missing_modules))
        sys.exit(1)

def install_ffmpeg():
    """
    Tự động cài đặt FFmpeg nếu không có trên hệ thống.
    """
    ffmpeg_path = "/usr/bin/ffmpeg"
    if not os.path.exists(ffmpeg_path):
        print("FFmpeg không được tìm thấy. Đang cài đặt qua pacman...")
        try:
            subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "ffmpeg"], check=True)
            print("FFmpeg đã được cài đặt thành công.")
        except subprocess.CalledProcessError as e:
            print(f"Không thể cài đặt FFmpeg: {e}")
            sys.exit(1)
    else:
        print("FFmpeg đã được cài đặt.")

def main():
    # Kiểm tra và kích hoạt môi trường ảo nếu cần
    check_and_activate_venv()

    # Danh sách các module cần kiểm tra
    required_modules = ["requests", "yt_dlp", "pyperclip", "keyboard"]

    # Kiểm tra và thông báo nếu thiếu module
    check_required_modules(required_modules)

    try:
        # Kiểm tra và cài đặt FFmpeg nếu cần
        print("Kiểm tra và cài đặt FFmpeg...")
        install_ffmpeg()

        # Import các module nội bộ sau khi đảm bảo module bên ngoài đã đầy đủ
        print("Kiểm tra và import modules.youtube...")
        from modules.youtube import monitor_clipboard_and_store_urls

        # Thực hiện logic chính
        print("Chạy monitor_clipboard_and_store_urls...")
        monitor_clipboard_and_store_urls()

    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
import os
import time
import pyperclip
import threading
from yt_dlp import YoutubeDL

# Global variables
youtube_links = []
monitoring = True

def monitor_clipboard():
    """Monitor the clipboard for YouTube links."""
    global youtube_links, monitoring

    print("\nClipboard monitoring started. Press F8 to stop.")
    while monitoring:
        # Get the current clipboard content
        clipboard_content = pyperclip.paste()
        
        # Check if it's a YouTube link and not already in the list
        if "youtube.com" in clipboard_content or "youtu.be" in clipboard_content:
            if clipboard_content not in youtube_links:
                youtube_links.append(clipboard_content)
                print(f"Added: {clipboard_content}")

        time.sleep(1)

def download_videos_as_mp3(links):
    """Download YouTube links as MP3 files."""
    print("\nStarting download...")
    
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': False,
    }

    with YoutubeDL(options) as ydl:
        ydl.download(links)

    print("\nAll downloads complete!")

def stop_monitoring():
    """Stop clipboard monitoring when F8 is pressed."""
    global monitoring
    print("\nStopping clipboard monitoring...")
    monitoring = False

# Main execution
if __name__ == "__main__":
    try:
        # Start the clipboard monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor_clipboard)
        monitor_thread.start()

        # Wait for F8 key press to stop monitoring
        while True:
            key = input("\nPress F8 to stop: ").strip().lower()
            if key == "f8":
                stop_monitoring()
                break

        # Wait for the monitoring thread to finish
        monitor_thread.join()

        # If there are links, download them
        if youtube_links:
            download_videos_as_mp3(youtube_links)
        else:
            print("\nNo YouTube links were detected.")

    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")

    except Exception as e:
        print(f"An error occurred: {e}")

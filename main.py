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

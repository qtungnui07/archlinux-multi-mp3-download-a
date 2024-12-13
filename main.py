import importlib
import sys
import os

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

def main():
    # Kiểm tra và kích hoạt môi trường ảo nếu cần
    check_and_activate_venv()

    # Danh sách các module cần kiểm tra
    required_modules = ["requests", "yt_dlp", "pyperclip", "keyboard"]

    # Kiểm tra và thông báo nếu thiếu module
    check_required_modules(required_modules)

    # Import các module nội bộ sau khi đảm bảo module bên ngoài đã đầy đủ
    from modules.ffmpeg import check_and_install_ffmpeg
    from modules.youtube import monitor_clipboard_and_store_urls

    # Thực hiện logic chính
    check_and_install_ffmpeg()
    monitor_clipboard_and_store_urls()

if __name__ == "__main__":
    main()

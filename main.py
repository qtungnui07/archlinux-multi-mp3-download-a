import importlib
import subprocess
import sys
import os

def create_and_activate_venv(venv_name="myenv"):
    """
    Tạo và kích hoạt môi trường ảo (venv).
    """
    if not os.path.exists(venv_name):
        print(f"Tạo môi trường ảo: {venv_name}")
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])

    # Kích hoạt môi trường ảo bằng cách thêm vào sys.path
    venv_bin = os.path.join(venv_name, "bin")
    if not os.path.exists(venv_bin):
        raise FileNotFoundError(f"Không tìm thấy thư mục: {venv_bin}. Kiểm tra lại việc tạo môi trường ảo.")

    sys.path.insert(0, os.path.abspath(venv_bin))
    os.environ["VIRTUAL_ENV"] = os.path.abspath(venv_name)
    os.environ["PATH"] = f"{os.path.abspath(venv_bin)}:{os.environ.get('PATH', '')}"

    print(f"Đã kích hoạt môi trường ảo: {venv_name}")

def install_and_import(package):
    """
    Kiểm tra nếu module thiếu thì tự động cài đặt
    """
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Module {package} chưa được cài đặt. Đang cài đặt {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)

def main():
    # Tạo và kích hoạt môi trường ảo
    create_and_activate_venv()

    # Danh sách các module cần kiểm tra
    required_modules = ["requests", "yt_dlp", "pyperclip", "keyboard"]
    for module in required_modules:
        install_and_import(module)

    # Import các module nội bộ
    from modules.ffmpeg import check_and_install_ffmpeg
    from modules.youtube import monitor_clipboard_and_store_urls

    # Thực hiện logic chính
    check_and_install_ffmpeg()
    monitor_clipboard_and_store_urls()

if __name__ == "__main__":
    main()

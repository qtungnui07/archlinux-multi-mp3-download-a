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

    print("\nClipboard monitoring started. Type 'done' to stop.")
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
    """Stop clipboard monitoring when 'done' is typed."""
    global monitoring
    print("\nStopping clipboard monitoring...")
    monitoring = False

# Main execution
if __name__ == "__main__":
    try:
        # Start the clipboard monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor_clipboard)
        monitor_thread.start()

        # Wait for 'done' input to stop monitoring
        while True:
            user_input = input("\nType 'done' to stop: ").strip().lower()
            if user_input == "done":
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

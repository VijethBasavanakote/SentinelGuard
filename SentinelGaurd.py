import os
import time
import cv2
import threading
from pushbullet import Pushbullet
from pynput import mouse
import pygetwindow as gw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCHED_WINDOW_TITLE = 'Your Window Title Here'
WATCHED_FOLDER = r"C:\Path\To\Watched\Folder"
PHOTO_FOLDER = r"C:\Path\To\Photo\Folder"
API_KEY = "Your_Pushbullet_API_Key_Here"
LOG_FILE_PATH = r"C:\Path\To\Log\File.txt"
NOTIFICATION_INTERVAL = 60  # seconds for mouse monitoring

# Global variables
window_bounds = None
last_notification_time = 0
access_detected = False

def send_notification(photo_path, message, keylogger_data=None):
    """Send a Pushbullet notification with the photo and details attached."""
    try:
        pb = Pushbullet(API_KEY)
        title = 'Window Event Alert'
        body = message
        if keylogger_data:
            body += f"\n\nKeylogger Data:\n{keylogger_data}"
        with open(photo_path, 'rb') as f:
            file_data = pb.upload_file(f, os.path.basename(photo_path))
            pb.push_file(**file_data, title=title, body=body)
        print("Pushbullet notification sent.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def capture_photo(photo_path):
    """Capture a photo and save it to the specified path."""
    print("Capturing photo...")
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open video device")
        return
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(photo_path, frame)
    camera.release()
    print(f"Photo captured: {photo_path}")

def get_window_bounds():
    """Get the bounds of the folder window."""
    try:
        window = gw.getWindowsWithTitle(WATCHED_WINDOW_TITLE)[0]
        return (window.left, window.top, window.right, window.bottom)
    except IndexError:
        return None

def get_active_window_title():
    """Get the title of the active window."""
    try:
        return gw.getActiveWindow().title
    except AttributeError:
        return "Unknown Window"

def monitor_window():
    """Monitor the window for opening, closing, and reopening."""
    global window_bounds
    previous_state = None
    while True:
        try:
            current_state = 'open' if get_window_bounds() else 'closed'
            if current_state != previous_state:
                if previous_state == 'open' and current_state == 'closed':
                    photo_path = os.path.join(PHOTO_FOLDER, 'intrusion.jpg')
                    capture_photo(photo_path)
                    # Read keylogger data
                    with open(LOG_FILE_PATH, 'r') as log_file:
                        keylogger_data = log_file.read()
                    send_notification(photo_path, "Window closed.", keylogger_data)
                    print("Window closed. Monitoring folder again...")
                elif previous_state == 'closed' and current_state == 'open':
                    photo_path = os.path.join(PHOTO_FOLDER, 'intrusion.jpg')
                    capture_photo(photo_path)
                    send_notification(photo_path, "Window opened.")
                previous_state = current_state
            time.sleep(1)  # Reduced from 5 seconds
        except Exception as e:
            print(f"Error monitoring window: {e}")

class FileEventHandler(FileSystemEventHandler):
    """Handle file system events."""
    def on_any_event(self, event):
        """Log file system events."""
        if event.is_directory:
            event_type = event.event_type
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event.event_type} on {event.src_path}\n")

def monitor_file_system():
    """Monitor file system changes."""
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Reduced from 1 second
    except KeyboardInterrupt:
        observer.stop()
        print("File system monitoring stopped.")
    observer.join()

def on_click(x, y, button, pressed):
    """Log mouse clicks with more descriptive information."""
    if pressed:
        window_title = get_active_window_title()
        # Log the click with window title
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Mouse clicked at ({x}, {y}) with {button} in window '{window_title}'\n")

def monitor_mouse():
    """Start monitoring mouse events."""
    with mouse.Listener(on_click=on_click) as listener:
        try:
            while True:
                time.sleep(NOTIFICATION_INTERVAL)
        except KeyboardInterrupt:
            print("Mouse monitoring stopped.")
            listener.stop()

def main():
    """Start all monitoring components."""
    print("Starting monitoring...")

    # Start threads for each monitoring component
    window_thread = threading.Thread(target=monitor_window)
    file_system_thread = threading.Thread(target=monitor_file_system)
    mouse_thread = threading.Thread(target=monitor_mouse)

    window_thread.start()
    file_system_thread.start()
    mouse_thread.start()

    window_thread.join()
    file_system_thread.join()
    mouse_thread.join()

if __name__ == "__main__":
    main()

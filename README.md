# **SentinelGuard**

**SentinelGuard** is a comprehensive monitoring system designed to observe and log various activities on your computer. It includes features for monitoring window events, file system changes, and mouse clicks, with notifications sent via Pushbullet.

## **Features**

- **Window Monitoring**: Tracks the opening, closing, and reopening of a specified window. Captures a photo when the window state changes and sends notifications.
- **File System Monitoring**: Observes changes in a specified directory and logs events.
- **Mouse Monitoring**: Logs mouse clicks with details about the position and the active window.
- **Pushbullet Notifications**: Sends notifications with attached photos and keylogger data via Pushbullet API.
- **Configurable Settings**: Easily adjustable settings for window title, folder paths, and notification intervals.

## **Installation**

### **Prerequisites**

- Python 3.x
- Required Python packages: `opencv-python`, `pushbullet.py`, `pynput`, `pygetwindow`, `watchdog`

### **Installation Steps**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/VijethBasavanakote/Project.git
   cd Project
   ```

2. **Install Required Packages**

   ```bash
   pip install opencv-python pushbullet.py pynput pygetwindow watchdog
   ```

3. **Configure Settings**

   Edit the script to set the following configuration variables:
   - `WATCHED_WINDOW_TITLE`: The title of the window you want to monitor.
   - `WATCHED_FOLDER`: The path to the folder you want to monitor.
   - `PHOTO_FOLDER`: The path where captured photos will be saved.
   - `API_KEY`: Your Pushbullet API key.
   - `LOG_FILE_PATH`: Path to the keylogger log file.
   - `NOTIFICATION_INTERVAL`: Time interval for mouse monitoring notifications.

## **Usage**

1. **Run the Script**

   ```bash
   python main.py
   ```

   This will start all monitoring components in separate threads:
   - **Window Monitoring**: Monitors the specified window for state changes.
   - **File System Monitoring**: Observes changes in the specified folder.
   - **Mouse Monitoring**: Logs mouse clicks and sends notifications.

2. **Stopping the Script**

   You can stop the script by interrupting the process (e.g., using `Ctrl+C` in the terminal).

## **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the coding guidelines and test your changes thoroughly.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Contact**

For any questions or support, you can contact me via [GitHub Issues](https://github.com/VijethBasavanakote/Project/issues) or [email](mailto:your-email@example.com).

---

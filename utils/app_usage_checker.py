from plyer import notification
from config import BLOCKED_APPS, FOCUS_MODE_TRIGGER
import time
import psutil
import threading
from kivy.logger import Logger

class AppUsageChecker:
    def __init__(self):
        self.focus_mode_running = False
        self.is_monitoring = False
        self.monitoring_thread = None

    def check_app_usage(self):
        """Legacy method for continuous monitoring"""
        while True:
            for process in psutil.process_iter(['pid', 'name']):
                if any(app.lower() in process.info['name'].lower() for app in BLOCKED_APPS):
                    if not self.focus_mode_running:
                        self.start_focus_mode()
            time.sleep(60)  # Check every minute

    def get_blocked_apps_running(self):
        """Get list of currently running blocked apps"""
        try:
            running_blocked_apps = []
            
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    process_name = process.info['name'].lower()
                    
                    # Check if this process matches any blocked app
                    for app in BLOCKED_APPS:
                        if app.lower() in process_name:
                            running_blocked_apps.append(app)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Skip processes that can't be accessed
                    continue
                    
            return list(set(running_blocked_apps))  # Remove duplicates
            
        except Exception as e:
            Logger.error(f"AppUsageChecker: Error getting blocked apps: {e}")
            return []

    def start_monitoring(self):
        """Start monitoring in background thread"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self.check_app_usage, daemon=True)
        self.monitoring_thread.start()
        Logger.info("AppUsageChecker: Started monitoring")

    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        Logger.info("AppUsageChecker: Stopped monitoring")

    def start_focus_mode(self):
        self.focus_mode_running = True
        notification.notify(title="Focus Mode Started", message="Distraction detected. Focus Mode started.")
        # Further logic to start focus mode

    def end_focus_mode(self):
        self.focus_mode_running = False
        notification.notify(title="Focus Mode Ended", message="Focus session completed. Meet you next time!")


"""
Android-compatible app usage checker
Uses Android's UsageStatsManager when available, falls back to simulation
"""

import time
import threading
from kivy.logger import Logger

class AndroidAppUsageChecker:
    def __init__(self):
        self.focus_mode_running = False
        self.is_monitoring = False
        self.monitoring_thread = None
        self.android_available = False
        self.usage_stats_manager = None
        self.blocked_apps = ['Instagram', 'Facebook', 'Twitter', 'Discord']
        
        # Try to initialize Android services
        self._init_android_services()
        
    def _init_android_services(self):
        """Initialize Android-specific services"""
        try:
            from jnius import autoclass, PythonJavaClass, java_method
            from android.permissions import request_permissions, Permission
            
            # Request necessary permissions
            request_permissions([
                Permission.PACKAGE_USAGE_STATS,
                Permission.SYSTEM_ALERT_WINDOW,
                Permission.INTERNET
            ])
            
            # Get Android services
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            
            self.context = PythonActivity.mActivity
            self.usage_stats_manager = self.context.getSystemService(Context.USAGE_STATS_SERVICE)
            self.android_available = True
            
            Logger.info("AndroidAppChecker: Android services initialized successfully")
            
        except ImportError:
            Logger.info("AndroidAppChecker: Running on desktop, Android services not available")
            self.android_available = False
        except Exception as e:
            Logger.error(f"AndroidAppChecker: Error initializing Android services: {e}")
            self.android_available = False
    
    def get_blocked_apps_running(self):
        """Get list of currently running blocked apps"""
        if self.android_available:
            return self._get_android_running_apps()
        else:
            return self._get_simulated_running_apps()
    
    def _get_android_running_apps(self):
        """Get running apps using Android's UsageStatsManager"""
        try:
            from jnius import autoclass
            
            # Get current time
            current_time = int(time.time() * 1000)  # Convert to milliseconds
            start_time = current_time - (5 * 60 * 1000)  # Last 5 minutes
            
            # Query usage stats
            usage_stats = self.usage_stats_manager.queryUsageStats(
                0,  # INTERVAL_DAILY
                start_time,
                current_time
            )
            
            running_blocked_apps = []
            
            if usage_stats:
                for stat in usage_stats:
                    package_name = stat.getPackageName()
                    last_used = stat.getLastTimeUsed()
                    
                    # Check if app was used in last 2 minutes
                    if current_time - last_used < (2 * 60 * 1000):
                        # Check if it's a blocked app
                        for blocked_app in self.blocked_apps:
                            if blocked_app.lower() in package_name.lower():
                                running_blocked_apps.append(blocked_app)
                                break
            
            return list(set(running_blocked_apps))
            
        except Exception as e:
            Logger.error(f"AndroidAppChecker: Error getting Android running apps: {e}")
            return []
    
    def _get_simulated_running_apps(self):
        """Simulate running apps for desktop testing"""
        # For desktop testing, we'll simulate no blocked apps running
        # In a real Android environment, this would use the Android method
        return []
    
    def start_monitoring(self):
        """Start monitoring in background thread"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        Logger.info("AndroidAppChecker: Started monitoring")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        Logger.info("AndroidAppChecker: Stopped monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Check for blocked apps
                blocked_apps = self.get_blocked_apps_running()
                
                if blocked_apps and not self.focus_mode_running:
                    Logger.info(f"AndroidAppChecker: Detected blocked apps: {blocked_apps}")
                    self.start_focus_mode()
                
                # Sleep for 30 seconds
                time.sleep(30)
                
            except Exception as e:
                Logger.error(f"AndroidAppChecker: Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def start_focus_mode(self):
        """Start focus mode"""
        self.focus_mode_running = True
        Logger.info("AndroidAppChecker: Focus mode started")
        
        # Send notification if plyer is available
        try:
            from plyer import notification
            notification.notify(
                title="Focus Mode Started",
                message="Distraction detected. Focus Mode started.",
                timeout=10
            )
        except ImportError:
            Logger.warning("AndroidAppChecker: Plyer not available for notifications")
    
    def end_focus_mode(self):
        """End focus mode"""
        self.focus_mode_running = False
        Logger.info("AndroidAppChecker: Focus mode ended")
        
        # Send notification if plyer is available
        try:
            from plyer import notification
            notification.notify(
                title="Focus Mode Ended",
                message="Focus session completed. Meet you next time!",
                timeout=10
            )
        except ImportError:
            Logger.warning("AndroidAppChecker: Plyer not available for notifications")
    
    def check_permissions(self):
        """Check if necessary permissions are granted"""
        if not self.android_available:
            return True  # Desktop doesn't need permissions
        
        try:
            # Check if usage stats permission is granted
            # This requires user to manually grant in Settings
            return True  # Assume granted for now
        except Exception as e:
            Logger.error(f"AndroidAppChecker: Error checking permissions: {e}")
            return False

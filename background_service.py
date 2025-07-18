#!/usr/bin/env python3
"""
Background Service for Focus Mode App
Handles app usage monitoring and triggers focus mode when needed
"""

import time
import threading
import json
import asyncio
from datetime import datetime, timedelta
from kivy.logger import Logger
from kivy.clock import Clock

# Import configuration and utilities
from config import BLOCKED_APPS, FOCUS_MODE_TRIGGER, SECRET_CODE
from utils.telegram_bot import telegram_bot
from utils.app_usage_checker import AppUsageChecker

class BackgroundService:
    """
    Background service that monitors app usage and triggers focus mode
    """
    
    def __init__(self, app_usage_checker=None, screen_manager=None):
        self.app_usage_checker = app_usage_checker
        self.screen_manager = screen_manager
        self.is_monitoring = False
        self.monitoring_thread = None
        self.focus_mode_active = False
        self.app_usage_data = {}
        self.last_check_time = datetime.now()
        
        # Load blocked apps configuration
        self.load_blocked_apps_config()
        
        Logger.info("BackgroundService: Initialized")
    
    def load_blocked_apps_config(self):
        """
        Load blocked apps configuration from JSON file
        """
        try:
            with open('blocked_apps.json', 'r') as f:
                self.config = json.load(f)
            Logger.info("BackgroundService: Loaded blocked apps configuration")
        except FileNotFoundError:
            Logger.warning("BackgroundService: blocked_apps.json not found, using defaults")
            self.config = {
                "blocked_apps": [
                    {"name": "Instagram", "package_name": "com.instagram.android", "daily_limit": 30},
                    {"name": "Facebook", "package_name": "com.facebook.katana", "daily_limit": 30},
                    {"name": "Twitter", "package_name": "com.twitter.android", "daily_limit": 30},
                    {"name": "Discord", "package_name": "com.discord", "daily_limit": 30}
                ],
                "focus_mode_settings": {
                    "black_screen_duration": 10,
                    "screen_lock_duration": 20,
                    "motivational_messages": [
                        "Your future is bright!",
                        "Stay focused, stay strong!",
                        "Great things await you!"
                    ]
                }
            }
        except Exception as e:
            Logger.error(f"BackgroundService: Error loading config: {e}")
            self.config = {}
    
    def start_monitoring(self):
        """
        Start the background monitoring service
        """
        if self.is_monitoring:
            Logger.warning("BackgroundService: Already monitoring")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        Logger.info("BackgroundService: Started monitoring")
    
    def stop_monitoring(self):
        """
        Stop the background monitoring service
        """
        self.is_monitoring = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        Logger.info("BackgroundService: Stopped monitoring")
    
    def _monitoring_loop(self):
        """
        Main monitoring loop that runs in background thread
        """
        Logger.info("BackgroundService: Monitoring loop started")
        
        while self.is_monitoring:
            try:
                # Check app usage
                self._check_app_usage()
                
                # Check if focus mode should be triggered
                self._check_focus_mode_trigger()
                
                # Update usage statistics
                self._update_usage_statistics()
                
                # Sleep for monitoring interval (60 seconds)
                time.sleep(60)
                
            except Exception as e:
                Logger.error(f"BackgroundService: Error in monitoring loop: {e}")
                time.sleep(30)  # Wait 30 seconds before retrying
    
    def _check_app_usage(self):
        """
        Check current app usage using the app usage checker
        """
        try:
            if self.app_usage_checker:
                # Get current running processes
                blocked_apps_running = self.app_usage_checker.get_blocked_apps_running()
                
                # Update usage tracking
                current_time = datetime.now()
                for app_name in blocked_apps_running:
                    if app_name not in self.app_usage_data:
                        self.app_usage_data[app_name] = {
                            'total_time': 0,
                            'last_seen': current_time,
                            'session_start': current_time
                        }
                    else:
                        # Update total time
                        time_diff = (current_time - self.app_usage_data[app_name]['last_seen']).total_seconds()
                        if time_diff <= 120:  # Only count if seen within last 2 minutes
                            self.app_usage_data[app_name]['total_time'] += time_diff
                        
                        self.app_usage_data[app_name]['last_seen'] = current_time
                
        except Exception as e:
            Logger.error(f"BackgroundService: Error checking app usage: {e}")
    
    def _check_focus_mode_trigger(self):
        """
        Check if focus mode should be triggered based on usage
        """
        try:
            if self.focus_mode_active:
                return  # Already in focus mode
            
            # Check each blocked app
            for app_name, usage_data in self.app_usage_data.items():
                total_minutes = usage_data['total_time'] / 60
                
                # Check if app exceeded the limit (30 minutes)
                if total_minutes >= 30:
                    Logger.info(f"BackgroundService: App {app_name} exceeded limit ({total_minutes:.1f} min)")
                    self._trigger_focus_mode()
                    break
                    
        except Exception as e:
            Logger.error(f"BackgroundService: Error checking focus mode trigger: {e}")
    
    def _trigger_focus_mode(self):
        """
        Trigger focus mode through the main UI thread
        """
        try:
            self.focus_mode_active = True
            
            # Schedule focus mode trigger on main thread
            Clock.schedule_once(self._ui_trigger_focus_mode, 0)
            
            # Send telegram notification
            self._send_telegram_notification("focus_started")
            
            Logger.info("BackgroundService: Focus mode triggered")
            
        except Exception as e:
            Logger.error(f"BackgroundService: Error triggering focus mode: {e}")
    
    def _ui_trigger_focus_mode(self, dt):
        """
        Trigger focus mode on the UI thread
        """
        try:
            if self.screen_manager:
                self.screen_manager.current = 'focus_mode'
                focus_screen = self.screen_manager.get_screen('focus_mode')
                focus_screen.start_focus_session(manual=False)
                
        except Exception as e:
            Logger.error(f"BackgroundService: Error in UI focus mode trigger: {e}")
    
    def _update_usage_statistics(self):
        """
        Update and clean up usage statistics
        """
        try:
            current_time = datetime.now()
            
            # Reset daily statistics at midnight
            if current_time.hour == 0 and current_time.minute == 0:
                self.app_usage_data = {}
                Logger.info("BackgroundService: Reset daily usage statistics")
            
            # Clean up old entries (older than 2 minutes)
            apps_to_remove = []
            for app_name, usage_data in self.app_usage_data.items():
                time_since_seen = (current_time - usage_data['last_seen']).total_seconds()
                if time_since_seen > 120:  # 2 minutes
                    apps_to_remove.append(app_name)
            
            for app_name in apps_to_remove:
                del self.app_usage_data[app_name]
                
        except Exception as e:
            Logger.error(f"BackgroundService: Error updating usage statistics: {e}")
    
    def _send_telegram_notification(self, notification_type):
        """
        Send telegram notification asynchronously
        """
        try:
            def send_notification():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    if notification_type == "focus_started":
                        loop.run_until_complete(telegram_bot.send_focus_mode_started())
                    elif notification_type == "focus_ended":
                        loop.run_until_complete(telegram_bot.send_focus_mode_ended())
                    elif notification_type == "manual_focus":
                        loop.run_until_complete(telegram_bot.send_manual_focus_started())
                    
                    loop.close()
                except Exception as e:
                    Logger.error(f"BackgroundService: Error sending telegram notification: {e}")
            
            # Run in separate thread to avoid blocking
            notification_thread = threading.Thread(target=send_notification, daemon=True)
            notification_thread.start()
            
        except Exception as e:
            Logger.error(f"BackgroundService: Error preparing telegram notification: {e}")
    
    def end_focus_mode(self):
        """
        Called when focus mode ends
        """
        try:
            self.focus_mode_active = False
            
            # Reset usage data for blocked apps
            self.app_usage_data = {}
            
            # Send telegram notification
            self._send_telegram_notification("focus_ended")
            
            Logger.info("BackgroundService: Focus mode ended")
            
        except Exception as e:
            Logger.error(f"BackgroundService: Error ending focus mode: {e}")
    
    def get_usage_statistics(self):
        """
        Get current usage statistics
        """
        try:
            stats = {}
            for app_name, usage_data in self.app_usage_data.items():
                stats[app_name] = {
                    'total_minutes': usage_data['total_time'] / 60,
                    'last_seen': usage_data['last_seen'].strftime('%H:%M:%S')
                }
            return stats
        except Exception as e:
            Logger.error(f"BackgroundService: Error getting usage statistics: {e}")
            return {}
    
    def trigger_manual_focus(self):
        """
        Trigger manual focus mode
        """
        try:
            if self.focus_mode_active:
                Logger.warning("BackgroundService: Focus mode already active")
                return
            
            self.focus_mode_active = True
            
            # Schedule focus mode trigger on main thread
            Clock.schedule_once(lambda dt: self._ui_trigger_manual_focus_mode(dt), 0)
            
            # Send telegram notification
            self._send_telegram_notification("manual_focus")
            
            Logger.info("BackgroundService: Manual focus mode triggered")
            
        except Exception as e:
            Logger.error(f"BackgroundService: Error triggering manual focus mode: {e}")
    
    def _ui_trigger_manual_focus_mode(self, dt):
        """
        Trigger manual focus mode on the UI thread
        """
        try:
            if self.screen_manager:
                self.screen_manager.current = 'focus_mode'
                focus_screen = self.screen_manager.get_screen('focus_mode')
                focus_screen.start_focus_session(manual=True)
                
        except Exception as e:
            Logger.error(f"BackgroundService: Error in UI manual focus mode trigger: {e}")

import time
import threading
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty

class FocusTimer(EventDispatcher):
    remaining_time = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.timer_thread = None
        self.total_time = 0
        
    def start_timer(self, duration_minutes):
        """Start a timer for the specified duration in minutes"""
        if self.is_running:
            return
            
        self.total_time = duration_minutes * 60
        self.remaining_time = self.total_time
        self.is_running = True
        
        self.timer_thread = threading.Thread(target=self._run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
    def _run_timer(self):
        """Internal timer loop"""
        while self.is_running and self.remaining_time > 0:
            time.sleep(1)
            if self.is_running:
                self.remaining_time -= 1
                
        if self.remaining_time <= 0:
            self.dispatch('on_timer_finished')
            
    def stop_timer(self):
        """Stop the timer"""
        self.is_running = False
        
    def reset_timer(self):
        """Reset the timer"""
        self.stop_timer()
        self.remaining_time = 0
        
    def get_formatted_time(self):
        """Get formatted time as MM:SS"""
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def on_timer_finished(self):
        """Called when timer finishes"""
        self.is_running = False
        print("Timer finished!")

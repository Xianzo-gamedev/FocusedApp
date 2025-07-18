from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from utils.timer import FocusTimer
from utils.telegram_bot import telegram_bot
import asyncio
import json
import random
import threading

class FocusModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'focus_mode'
        self.timer = FocusTimer()
        self.timer.bind(on_timer_finished=self.on_timer_finished)
        self.current_phase = 'black_screen'  # 'black_screen' or 'locked_screen'
        self.phase_start_time = 0
        self.build_ui()
        
    def build_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Set background color to black
        with main_layout.canvas.before:
            Color(0, 0, 0, 1)  # Black background
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Motivational message
        self.message_label = Label(
            text='',
            font_size='20sp',
            color=(1, 1, 1, 1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(self.message_label)
        
        # Timer display
        self.timer_label = Label(
            text='',
            font_size='32sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=100
        )
        main_layout.add_widget(self.timer_label)
        
        # Phase label
        self.phase_label = Label(
            text='',
            font_size='16sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(self.phase_label)
        
        self.add_widget(main_layout)
        
        # Update timer display
        Clock.schedule_interval(self.update_timer_display, 1.0)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def start_focus_session(self, manual=False):
        """Start a 30-minute focus session"""
        self.current_phase = 'black_screen'
        self.timer.start_timer(30)  # 30 minutes total
        self.phase_start_time = self.timer.remaining_time
        
        # Load motivational messages
        with open('blocked_apps.json', 'r') as f:
            data = json.load(f)
            messages = data['focus_mode_settings']['motivational_messages']
            
        # Show random motivational message
        message = random.choice(messages)
        self.message_label.text = message
        self.phase_label.text = 'Phase 1: Reflection Time'
        
        # Send telegram notification
        if manual:
            self._send_telegram_notification_async("manual_focus")
        else:
            self._send_telegram_notification_async("focus_started")
            
    def update_timer_display(self, dt):
        """Update timer display"""
        if self.timer.is_running:
            self.timer_label.text = self.timer.get_formatted_time()
            
            # Check if we need to switch phases
            elapsed_time = self.phase_start_time - self.timer.remaining_time
            
            if self.current_phase == 'black_screen' and elapsed_time >= 10 * 60:  # 10 minutes
                self.switch_to_locked_phase()
                
    def switch_to_locked_phase(self):
        """Switch to locked screen phase"""
        self.current_phase = 'locked_screen'
        self.phase_label.text = 'Phase 2: Focus Lock'
        self.message_label.text = 'Stay strong! Your future is being built right now.'
        
        # Change background to dark gray
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(size=self.size, pos=self.pos)
            
    def on_timer_finished(self, timer):
        """Called when focus session ends"""
        self.message_label.text = 'Your future is bright! Meet you next time.'
        self.phase_label.text = 'Session Complete'
        self.timer_label.text = '00:00'
        
        # Send telegram notification
        self._send_telegram_notification_async("focus_ended")
        
        # Schedule return to home screen
        Clock.schedule_once(self.return_to_home, 3.0)
        
    def return_to_home(self, dt):
        """Return to home screen"""
        self.manager.current = 'home'
        
    def emergency_unlock(self):
        """Emergency unlock function"""
        self.timer.stop_timer()
        self.message_label.text = 'Emergency unlock activated'
        Clock.schedule_once(self.return_to_home, 2.0)
    
    def _send_telegram_notification_async(self, notification_type):
        """Send telegram notification asynchronously"""
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
                print(f"Error sending telegram notification: {e}")
        
        # Run in separate thread to avoid blocking
        notification_thread = threading.Thread(target=send_notification, daemon=True)
        notification_thread.start()

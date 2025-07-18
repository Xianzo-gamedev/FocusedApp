from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from utils.telegram_bot import telegram_bot
import asyncio
import threading

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.build_ui()
        
    def build_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Set background color
        with main_layout.canvas.before:
            Color(0.1, 0.1, 0.2, 1)  # Dark blue background
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Title
        title = Label(
            text='Focus Mode App',
            font_size='24sp',
            size_hint_y=None,
            height=80,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='Monitoring your app usage...',
            font_size='16sp',
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Instructions label
        instructions_label = Label(
            text='Emergency unlock: Tap 🔧 (bottom-left) during focus mode',
            font_size='12sp',
            size_hint_y=None,
            height=40,
            color=(0.6, 0.6, 0.6, 1)
        )
        main_layout.add_widget(instructions_label)
        
        # Manual focus button
        focus_button = Button(
            text='Start 30-Min Focus Session',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='18sp'
        )
        focus_button.bind(on_press=self.start_manual_focus)
        main_layout.add_widget(focus_button)
        
        # Settings button
        settings_button = Button(
            text='Settings',
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='16sp'
        )
        main_layout.add_widget(settings_button)
        
        # Emergency unlock button (bottom-left corner)
        unlock_button = Button(
            text='🔧',
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={'x': 0.02, 'y': 0.02},
            background_color=(0.8, 0.5, 0.2, 0.9),
            font_size='18sp',
            color=(1, 1, 1, 1)
        )
        print("Emergency unlock button created at bottom-left corner")
        unlock_button.bind(on_press=self.show_unlock_screen)
        
        # Add to screen
        self.add_widget(main_layout)
        self.add_widget(unlock_button)
        
        # Start monitoring
        Clock.schedule_interval(self.update_status, 1.0)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def start_manual_focus(self, instance):
        """Start manual focus mode"""
        # Send telegram notification in separate thread
        self._send_telegram_notification_async("manual_focus")
        
        # Switch to focus mode
        self.manager.current = 'focus_mode'
        self.manager.get_screen('focus_mode').start_focus_session(manual=True)
    
    def _send_telegram_notification_async(self, notification_type):
        """Send telegram notification asynchronously"""
        def send_notification():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if notification_type == "manual_focus":
                    loop.run_until_complete(telegram_bot.send_manual_focus_started())
                
                loop.close()
            except Exception as e:
                print(f"Error sending telegram notification: {e}")
        
        # Run in separate thread to avoid blocking
        notification_thread = threading.Thread(target=send_notification, daemon=True)
        notification_thread.start()
        
    def show_unlock_screen(self, instance):
        """Show unlock screen"""
        self.manager.current = 'unlock'
        
    def update_status(self, dt):
        """Update status label"""
        # This would typically check app usage and update accordingly
        pass

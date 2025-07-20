<<<<<<< HEAD
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from config import SECRET_CODE

class UnlockInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'unlock'
        self.build_ui()
        
    def build_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Set background color
        with main_layout.canvas.before:
            Color(0.2, 0.2, 0.3, 1)  # Dark background
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Title
        title = Label(
            text='Emergency Unlock',
            font_size='24sp',
            size_hint_y=None,
            height=80,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Instruction
        instruction = Label(
            text='Enter secret code to unlock focus mode:',
            font_size='16sp',
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(instruction)
        
        # Text input
        self.code_input = TextInput(
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        self.code_input.bind(on_text_validate=self.check_code)
        main_layout.add_widget(self.code_input)
        
        # Submit button
        submit_button = Button(
            text='Submit',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='18sp'
        )
        submit_button.bind(on_press=self.check_code)
        main_layout.add_widget(submit_button)
        
        # Back button
        back_button = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=(0.7, 0.2, 0.2, 1),
            font_size='16sp'
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)
        
        # Error message
        self.error_label = Label(
            text='',
            font_size='14sp',
            size_hint_y=None,
            height=40,
            color=(1, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.error_label)
        
        self.add_widget(main_layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def check_code(self, instance):
        """Check if entered code is correct"""
        entered_code = self.code_input.text
        
        if entered_code == SECRET_CODE:
            self.error_label.text = 'Code accepted! Unlocking...'
            self.error_label.color = (0.2, 1, 0.2, 1)
            
            # Check if focus mode is active
            if self.manager.has_screen('focus_mode'):
                focus_screen = self.manager.get_screen('focus_mode')
                if focus_screen.timer.is_running:
                    focus_screen.emergency_unlock()
                    
            # Return to home
            self.manager.current = 'home'
            
        else:
            self.error_label.text = 'Invalid code. Try again.'
            self.error_label.color = (1, 0.2, 0.2, 1)
            self.code_input.text = ''
            
    def go_back(self, instance):
        """Go back to previous screen"""
        # Check if focus mode is active
        if self.manager.has_screen('focus_mode'):
            focus_screen = self.manager.get_screen('focus_mode')
            if focus_screen.timer.is_running:
                self.manager.current = 'focus_mode'
                return
                
        self.manager.current = 'home'
        
    def on_enter(self):
        """Called when screen is entered"""
        self.code_input.text = ''
        self.error_label.text = ''
        self.code_input.focus = True
=======
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from config import SECRET_CODE

class UnlockInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'unlock'
        self.build_ui()
        
    def build_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Set background color
        with main_layout.canvas.before:
            Color(0.2, 0.2, 0.3, 1)  # Dark background
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Title
        title = Label(
            text='Emergency Unlock',
            font_size='24sp',
            size_hint_y=None,
            height=80,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Instruction
        instruction = Label(
            text='Enter secret code to unlock focus mode:',
            font_size='16sp',
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(instruction)
        
        # Text input
        self.code_input = TextInput(
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        self.code_input.bind(on_text_validate=self.check_code)
        main_layout.add_widget(self.code_input)
        
        # Submit button
        submit_button = Button(
            text='Submit',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='18sp'
        )
        submit_button.bind(on_press=self.check_code)
        main_layout.add_widget(submit_button)
        
        # Back button
        back_button = Button(
            text='Back',
            size_hint_y=None,
            height=50,
            background_color=(0.7, 0.2, 0.2, 1),
            font_size='16sp'
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)
        
        # Error message
        self.error_label = Label(
            text='',
            font_size='14sp',
            size_hint_y=None,
            height=40,
            color=(1, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.error_label)
        
        self.add_widget(main_layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def check_code(self, instance):
        """Check if entered code is correct"""
        entered_code = self.code_input.text
        
        if entered_code == SECRET_CODE:
            self.error_label.text = 'Code accepted! Unlocking...'
            self.error_label.color = (0.2, 1, 0.2, 1)
            
            # Check if focus mode is active
            if self.manager.has_screen('focus_mode'):
                focus_screen = self.manager.get_screen('focus_mode')
                if focus_screen.timer.is_running:
                    focus_screen.emergency_unlock()
                    
            # Return to home
            self.manager.current = 'home'
            
        else:
            self.error_label.text = 'Invalid code. Try again.'
            self.error_label.color = (1, 0.2, 0.2, 1)
            self.code_input.text = ''
            
    def go_back(self, instance):
        """Go back to previous screen"""
        # Check if focus mode is active
        if self.manager.has_screen('focus_mode'):
            focus_screen = self.manager.get_screen('focus_mode')
            if focus_screen.timer.is_running:
                self.manager.current = 'focus_mode'
                return
                
        self.manager.current = 'home'
        
    def on_enter(self):
        """Called when screen is entered"""
        self.code_input.text = ''
        self.error_label.text = ''
        self.code_input.focus = True
>>>>>>> 6e51290681d7035ca70ba6893d1c33e0420ad343

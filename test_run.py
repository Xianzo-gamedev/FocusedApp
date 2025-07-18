#!/usr/bin/env python3
"""
Test script to run the Focus App
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Test import all modules
try:
    from main import FocusApp
    from config import SECRET_CODE, BLOCKED_APPS
    from utils.app_usage_checker import AppUsageChecker
    from utils.telegram_bot import TelegramBot
    from utils.timer import FocusTimer
    from background_service import BackgroundService
    from screens.home_screen import HomeScreen
    from screens.focus_mode import FocusModeScreen
    from screens.unlock_input import UnlockInputScreen
    
    print("✅ All imports successful!")
    print(f"Secret code: {SECRET_CODE}")
    print(f"Blocked apps: {BLOCKED_APPS}")
    
    # Try to create the app
    app = FocusApp()
    print("✅ App created successfully!")
    print("Ready to run with: python main.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

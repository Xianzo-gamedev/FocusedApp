# Focus Mode App

A Kivy-based Android app that helps students stay focused by monitoring app usage and triggering focus mode when distracting apps are used for more than 30 minutes.

## Features

1. **App Usage Monitoring**: Monitors Instagram, Facebook, Twitter, Discord usage
2. **Automatic Focus Mode**: Triggers 30-minute focus session when threshold is crossed
3. **Manual Focus Mode**: Start focus session anytime with a button
4. **Emergency Unlock**: Hidden unlock feature with secret code
5. **Telegram Notifications**: Sends notifications when focus mode starts/ends
6. **Two-Phase Focus Mode**:
   - First 10 minutes: Black screen with motivational message
   - Next 20 minutes: Screen lock with timer

## Project Structure

```
FocusedApp/
├── main.py                 # Main application entry point
├── background_service.py   # Background monitoring service
├── config.py              # App configuration
├── blocked_apps.json      # Blocked apps and settings
├── requirements.txt       # Python dependencies
├── screens/
│   ├── home_screen.py     # Main home screen
│   ├── focus_mode.py      # Focus mode screen
│   └── unlock_input.py    # Emergency unlock screen
├── utils/
│   ├── app_usage_checker.py # App usage monitoring
│   ├── telegram_bot.py     # Telegram bot integration
│   └── timer.py           # Focus timer utility
└── assets/               # Assets directory
```

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the app:
   - Edit `config.py` to set your secret code and Telegram API key
   - Update `blocked_apps.json` if needed

3. Run the app:
   ```bash
   python main.py
   ```

## Configuration

### config.py
- `SECRET_CODE`: Emergency unlock code (default: '1234')
- `FOCUS_MODE_TRIGGER`: Time in seconds to trigger focus mode (default: 1800 = 30 minutes)
- `TELEGRAM_API_KEY`: Your Telegram bot API key
- `BLOCKED_APPS`: List of apps to monitor

### blocked_apps.json
Contains blocked apps configuration and focus mode settings including:
- App names and package names
- Daily limits for each app
- Focus mode durations
- Motivational messages

## Usage

1. **Home Screen**: 
   - Shows monitoring status
   - Manual focus button
   - Hidden unlock button (⚙) in bottom-left

2. **Focus Mode**:
   - Phase 1: 10-minute black screen with message
   - Phase 2: 20-minute lock screen with timer
   - Shows remaining time and motivational messages

3. **Emergency Unlock**:
   - Click hidden ⚙ button
   - Enter secret code to unlock

## Telegram Integration

To enable Telegram notifications:
1. Create a Telegram bot via @BotFather
2. Get your bot token
3. Update `TELEGRAM_API_KEY` in config.py
4. Set your chat ID in the bot

## Testing

Run the test script to verify everything works:
```bash
python test_run.py
```

## Android Deployment

For Android deployment, you'll need:
1. Buildozer for APK building
2. Android permissions for app usage monitoring
3. Background service permissions

## License

This project is for educational purposes.

# Emergency Unlock Guide

## Finding the Emergency Unlock Buttons

### 🔧 Home Screen Emergency Button
- **Location**: Bottom-left corner of the screen
- **Icon**: 🔧 (wrench icon)
- **Size**: 50x50 pixels
- **Color**: Brown/orange background
- **Function**: Opens the emergency unlock screen

### 🚨 Focus Mode Emergency Button
- **Location**: Bottom-right corner of the screen
- **Icon**: 🚨 (alarm icon)
- **Size**: 50x50 pixels  
- **Color**: Red background
- **Function**: Opens the emergency unlock screen during focus mode

## How to Use Emergency Unlock

1. **Locate the Emergency Button**:
   - On home screen: Look for 🔧 in bottom-left corner
   - During focus mode: Look for 🚨 in bottom-right corner

2. **Tap the Emergency Button**:
   - The emergency unlock screen will open

3. **Enter Secret Code**:
   - Default code: `1234`
   - You can change this in `config.py`

4. **Unlock**:
   - If correct code is entered, focus mode will be disabled
   - You'll return to the home screen

## If You Can't Find the Buttons

The emergency buttons are designed to be subtle but accessible:
- They are semi-transparent so they don't interfere with the UI
- They are positioned in corners for easy access
- They have distinct colors (brown for home, red for focus mode)
- They use emoji icons for better visibility

## Testing the Emergency Unlock

1. Start the app: `python main.py`
2. Click "Start 30-Min Focus Session"
3. Look for the red 🚨 button in bottom-right corner
4. Tap it to open unlock screen
5. Enter code `1234` to unlock

## Troubleshooting

If the buttons are not visible:
- Check if your screen resolution is very small
- The buttons might be outside the visible area
- Try maximizing the app window
- The buttons should be 50x50 pixels in size

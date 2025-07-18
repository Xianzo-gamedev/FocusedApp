# Android Build and Debug Guide

## Prerequisites

### For Windows Users:
**Note**: Building Android APKs on Windows is complex and often problematic. Consider using WSL2 or a Linux VM.

### Option 1: Using WSL2 (Recommended)
1. Install WSL2 with Ubuntu
2. Install the project in WSL2
3. Follow the Linux build instructions

### Option 2: Using Linux VM
1. Set up a Linux VM (Ubuntu 20.04+ recommended)
2. Copy the project to the VM
3. Follow the Linux build instructions

### Option 3: Using GitHub Actions (Easiest)
1. Push your code to GitHub
2. Use GitHub Actions to build the APK
3. Download the built APK

## Linux Build Process

### Step 1: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-dev -y

# Install build tools
sudo apt install git unzip default-jdk -y

# Install buildozer
pip3 install buildozer
```

### Step 2: Build Debug APK
```bash
# Navigate to project directory
cd FocusedApp

# Build debug APK (first time will take 30-60 minutes)
buildozer android debug
```

### Step 3: Build Release APK
```bash
# Build release APK
buildozer android release

# Sign the APK (optional, for distribution)
# You'll need to create a keystore first
```

## Testing on Android

### Method 1: Physical Device
1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device to computer
4. Install APK: `adb install bin/focusapp-0.1-debug.apk`

### Method 2: Android Emulator
1. Install Android Studio
2. Create an AVD (Android Virtual Device)
3. Start emulator
4. Install APK: `adb install bin/focusapp-0.1-debug.apk`

## Debugging

### View Logs
```bash
# View all logs
adb logcat

# View Python logs only
adb logcat | grep python

# View app-specific logs
adb logcat | grep focusapp
```

### Common Issues and Solutions

#### 1. Build Fails - Missing Dependencies
```bash
# Install missing system dependencies
sudo apt install python3-dev libffi-dev libssl-dev
```

#### 2. Build Fails - Java Issues
```bash
# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/default-java
```

#### 3. App Crashes on Android
- Check logcat for Python errors
- Ensure all permissions are granted
- Test on different Android versions

#### 4. App Usage Monitoring Not Working
- Grant "Usage Access" permission manually in Settings
- Check if `psutil` works on Android (may need alternative)

### Android-Specific Modifications

#### 1. Update app_usage_checker.py for Android
```python
# Add Android-specific app usage monitoring
try:
    from jnius import autoclass
    # Use Android's UsageStatsManager
    UsageStatsManager = autoclass('android.app.usage.UsageStatsManager')
    # Implementation needed
except ImportError:
    # Fall back to psutil for desktop testing
    pass
```

#### 2. Request Permissions at Runtime
```python
# Add to main.py
from android.permissions import request_permissions, Permission

def request_android_permissions():
    request_permissions([
        Permission.PACKAGE_USAGE_STATS,
        Permission.SYSTEM_ALERT_WINDOW,
        Permission.INTERNET
    ])
```

## File Structure After Build
```
FocusedApp/
├── .buildozer/          # Build cache
├── bin/                 # Built APK files
│   ├── focusapp-0.1-debug.apk
│   └── focusapp-0.1-release.apk (if built)
├── buildozer.spec       # Build configuration
└── [project files]
```

## Performance Tips

1. **First Build**: Takes 30-60 minutes (downloads Android SDK/NDK)
2. **Subsequent Builds**: 5-15 minutes
3. **Clean Build**: `buildozer android clean` then rebuild
4. **Faster Builds**: Use `buildozer android debug` instead of release

## Troubleshooting

### Build Errors
1. Check `buildozer.spec` configuration
2. Verify all requirements are spelled correctly
3. Clean build cache: `buildozer android clean`
4. Update buildozer: `pip3 install --upgrade buildozer`

### Runtime Errors
1. Check Android logs: `adb logcat`
2. Test on different Android versions
3. Verify permissions are granted
4. Check if all Python packages work on Android

## Testing Checklist

- [ ] App installs without errors
- [ ] App starts and shows home screen
- [ ] Manual focus mode works
- [ ] Timer counts down properly
- [ ] Emergency unlock works
- [ ] App permissions are requested
- [ ] Background monitoring works (if supported)
- [ ] App doesn't crash on different screens
- [ ] UI scales properly on different devices

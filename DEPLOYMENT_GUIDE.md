# Complete Deployment and Testing Guide

## 📱 Quick Start for Testing

### Desktop Testing (Windows)
```bash
# 1. Clone/navigate to project
cd FocusedApp

# 2. Install dependencies (already done)
pip install -r requirements.txt

# 3. Run the app
python main.py
```

### Testing Features
1. **Home Screen**: Should show Focus Mode App with instructions
2. **Emergency Button**: Look for 🔧 in bottom-left corner
3. **Manual Focus**: Click "Start 30-Min Focus Session"
4. **Focus Mode**: Should show black screen with timer and 🚨 button
5. **Emergency Unlock**: Click 🚨 → enter code `1234`

---

## 🔧 Android Development Setup

### Option 1: WSL2 (Recommended for Windows)
```bash
# Install WSL2 with Ubuntu
wsl --install Ubuntu

# Inside WSL2:
sudo apt update && sudo apt install -y python3 python3-pip python3-dev
sudo apt install -y git unzip default-jdk
pip3 install buildozer

# Copy project to WSL2
cp -r /mnt/c/path/to/FocusedApp ~/
cd ~/FocusedApp

# Build APK
buildozer android debug
```

### Option 2: GitHub Actions (Easiest)
1. Push code to GitHub
2. Go to Actions tab
3. Run "Build Android APK" workflow
4. Download APK from artifacts

### Option 3: Linux VM
1. Create Ubuntu 20.04+ VM
2. Install dependencies
3. Build APK

---

## 📲 APK Installation and Testing

### Install APK on Device
```bash
# Enable Developer Options on Android device
# Enable USB Debugging
# Connect device

# Install APK
adb install bin/focusapp-0.1-debug.apk

# View logs
adb logcat | grep python
```

### Test on Android Emulator
```bash
# Install Android Studio
# Create AVD with API 28+
# Start emulator
adb install bin/focusapp-0.1-debug.apk
```

---

## 🐛 Debugging Guide

### Common Issues and Solutions

#### 1. **Build Fails on Windows**
```bash
# Solution: Use WSL2 or Linux VM
# Windows buildozer is problematic
```

#### 2. **Python Import Errors**
```bash
# Check buildozer.spec requirements
# Ensure all packages are spelled correctly
# Some packages may not work on Android
```

#### 3. **App Crashes on Start**
```bash
# Check logcat for errors
adb logcat | grep -i error

# Common causes:
# - Missing Android permissions
# - Incompatible Python packages
# - File path issues
```

#### 4. **UI Elements Not Visible**
```bash
# Check device screen size
# Emergency buttons may be outside viewport on small screens
# Test on different screen sizes
```

#### 5. **App Usage Monitoring Not Working**
```bash
# Grant "Usage Access" permission manually:
# Settings > Apps > Special Access > Usage Access > Focus Mode App > Allow

# Check if permissions are requested in code
# Verify UsageStatsManager is available
```

### Debug Commands
```bash
# View all logs
adb logcat

# Python-specific logs
adb logcat | grep python

# App-specific logs
adb logcat | grep focusapp

# Clear logs
adb logcat -c

# Install and run immediately
adb install -r bin/focusapp-0.1-debug.apk && adb shell am start -n com.shlok.focusapp/org.kivy.android.PythonActivity
```

---

## 🧪 Testing Checklist

### Desktop Testing
- [ ] App starts without errors
- [ ] Home screen displays correctly
- [ ] Emergency button (🔧) visible in bottom-left
- [ ] Manual focus button works
- [ ] Focus mode starts and shows timer
- [ ] Emergency button (🚨) visible in focus mode
- [ ] Emergency unlock works with code `1234`
- [ ] Timer counts down properly
- [ ] App returns to home after session

### Android Testing
- [ ] APK installs successfully
- [ ] App starts without crashes
- [ ] All permissions are requested
- [ ] UI scales properly on device
- [ ] Touch interactions work
- [ ] Emergency buttons are accessible
- [ ] Focus mode works on device
- [ ] Background monitoring works (if implemented)
- [ ] App handles screen rotation
- [ ] App handles back button properly

### Performance Testing
- [ ] App starts quickly (< 5 seconds)
- [ ] UI responds smoothly
- [ ] Memory usage is reasonable
- [ ] Battery usage is acceptable
- [ ] App doesn't slow down device

---

## 🚀 Deployment Options

### 1. Direct APK Distribution
```bash
# Build release APK
buildozer android release

# Share APK file directly
# Users need to enable "Unknown Sources"
```

### 2. Google Play Store
```bash
# Create developer account ($25 fee)
# Build release APK/AAB
# Upload to Play Console
# Fill store listing
# Submit for review
```

### 3. F-Droid (Open Source)
```bash
# Submit to F-Droid repository
# Must be open source
# Automated builds from source
```

### 4. Side-loading for Testing
```bash
# For development/testing only
# Share APK with beta testers
# No store approval needed
```

---

## ⚙️ Configuration for Production

### 1. Update Config
```python
# config.py - Change for production
SECRET_CODE = 'your-secure-code'  # Change from '1234'
TELEGRAM_API_KEY = 'your-real-api-key'
```

### 2. Update Buildozer Spec
```ini
# buildozer.spec - For production
version = 1.0
android.permissions = ... # Add only needed permissions
```

### 3. Create Release Keystore
```bash
# Generate keystore for signing
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```

---

## 📊 Monitoring and Analytics

### 1. Add Crash Reporting
```python
# Add to main.py
try:
    import firebase_crashlytics
    # Initialize crash reporting
except ImportError:
    pass
```

### 2. Usage Analytics
```python
# Track app usage
# User engagement metrics
# Focus session statistics
```

### 3. Performance Monitoring
```python
# Monitor app performance
# Track memory usage
# Monitor battery consumption
```

---

## 🔒 Security Considerations

### 1. Permissions
- Only request necessary permissions
- Explain why permissions are needed
- Handle permission denials gracefully

### 2. Data Protection
- Store sensitive data securely
- Encrypt local storage if needed
- Don't log sensitive information

### 3. App Integrity
- Sign APK with secure keystore
- Enable ProGuard for obfuscation
- Validate app integrity on start

---

## 📚 Additional Resources

### Documentation
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Kivy Android Documentation](https://kivy.org/doc/stable/guide/android.html)
- [Python for Android](https://python-for-android.readthedocs.io/)

### Community
- [Kivy Discord](https://discord.gg/kivy)
- [Kivy GitHub](https://github.com/kivy/kivy)
- [Python for Android GitHub](https://github.com/kivy/python-for-android)

### Tools
- [Android Studio](https://developer.android.com/studio)
- [ADB Commands](https://developer.android.com/studio/command-line/adb)
- [Logcat](https://developer.android.com/studio/command-line/logcat)

---

## 🎯 Next Steps

1. **Test on Desktop**: Verify all features work
2. **Build APK**: Use WSL2 or GitHub Actions
3. **Test on Android**: Install and test on real device
4. **Fix Issues**: Debug and resolve any problems
5. **Optimize**: Improve performance and user experience
6. **Deploy**: Choose deployment method and publish

Good luck with your Focus Mode App! 🎉

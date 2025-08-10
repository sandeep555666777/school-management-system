# Capacitor Native App Setup (Easiest!)

## Install Capacitor
```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
```

## Initialize Capacitor
```bash
mkdir SchoolCapacitorApp
cd SchoolCapacitorApp
npm init -y
npx cap init "School Management" "com.school.management"
```

## Create capacitor.config.ts
```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.school.management',
  appName: 'School Management System',
  webDir: 'www',
  bundledWebRuntime: false,
  server: {
    url: 'http://your-server.com:5000',
    cleartext: true,
    androidScheme: 'https'
  },
  android: {
    allowMixedContent: true,
    webContentsDebuggingEnabled: true
  },
  plugins: {
    StatusBar: {
      style: 'DARK',
      backgroundColor: '#007bff'
    },
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#007bff',
      showSpinner: true,
      spinnerColor: '#ffffff'
    }
  }
};

export default config;
```

## Create www/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>School Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #007bff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
        }
        .loading {
            text-align: center;
        }
        .spinner {
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="loading">
        <div class="spinner"></div>
        <h3>School Management System</h3>
        <p>Loading...</p>
    </div>
    
    <script>
        // Redirect to Flask app after short delay
        setTimeout(() => {
            window.location.href = 'http://your-server.com:5000';
        }, 1500);
    </script>
</body>
</html>
```

## Add Android Platform
```bash
npx cap add android
```

## Sync and Build
```bash
npx cap sync
npx cap open android
```

**In Android Studio:**
1. Build → Generate Signed Bundle/APK
2. Choose APK
3. Create keystore or use existing
4. Build Release APK

**Result**: Native Android app, 5-10MB, professional finish!

## Quick Commands
```bash
# Development build
npx cap run android

# Production build
npx cap build android

# Live reload during development
npx cap run android --live-reload --external
```

**Advantages:**
- ✅ True native app (no browser)
- ✅ Access to native device features
- ✅ Small app size
- ✅ Easy to maintain
- ✅ Can upload to Google Play Store
# Tauri Native App Setup

## Install Tauri
```bash
# Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
npm install --save-dev @tauri-apps/cli
npm install @tauri-apps/api
```

## Initialize Tauri Project
```bash
mkdir SchoolManagementApp
cd SchoolManagementApp
npm init -y
npx tauri init
```

## Configure tauri.conf.json
```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://127.0.0.1:5000",
    "distDir": "../dist",
    "withGlobalTauri": false
  },
  "package": {
    "productName": "School Management System",
    "version": "1.0.0"
  },
  "tauri": {
    "allowlist": {
      "all": true
    },
    "bundle": {
      "active": true,
      "category": "Education",
      "identifier": "com.school.management",
      "targets": "all"
    },
    "windows": [
      {
        "fullscreen": false,
        "height": 800,
        "resizable": true,
        "title": "School Management System",
        "width": 1200,
        "url": "http://127.0.0.1:5000"
      }
    ]
  }
}
```

## Build Commands
```bash
# Development
npx tauri dev

# Production build
npx tauri build
```

**Result**: Native desktop/mobile app, ~10MB size, no browser elements!
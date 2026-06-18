---
name: export-deploy
description: Export and deploy Godot projects to Windows, Linux, macOS, Android, iOS, and Web platforms. Use this skill when configuring export presets, setting up CI/CD pipelines, preparing release builds, optimizing for target platforms, or distributing games to Steam, itch.io, or mobile stores.
metadata:
  author: godot-dev
  version: "1.0"
---

# Export and Deploy

## Export Presets Setup

### Windows Export

```cfg
[preset.0]
name="Windows"
platform="Windows"
export_path="build/windows/game.exe"

[preset.0.options]
custom_template/debug=""
custom_template/release=""
binary_format/embed_pck=true
texture_format/s3tc=true
texture_format/etc2=false
```

### Linux Export

```cfg
[preset.1]
name="Linux"
platform="Linux"
export_path="build/linux/game.x86_64"
```

### macOS Export

```cfg
[preset.2]
name="macOS"
platform="macOS"
export_path="build/macos/game.app"
```

### Android Export

```cfg
[preset.3]
name="Android"
platform="Android"
export_path="build/android/game.apk"

[preset.3.options]
custom_template/debug=""
custom_template/release=""
gradle_build/use_gradle_build=true
gradle_build/export_format=0
```

### Web Export

```cfg
[preset.4]
name="Web"
platform="Web"
export_path="build/web/game.html"
```

## Export via Command Line

```bash
# Single platform
godot --headless --export-release "Windows" build/windows/game.exe

# All platforms
godot --headless --export-release "Windows" build/windows/game.exe
godot --headless --export-release "Linux" build/linux/game.x86_64
godot --headless --export-release "Web" build/web/game.html
```

## Export Settings

### Quality Settings

```ini
[rendering]
renderer/rendering_method="forward_plus"
renderer/rendering_method.mobile="mobile"
anti_aliasing/quality/msaa_3d=2
```

### Performance Settings

```ini
[rendering]
limits/rendering/max_renderable_elements=10000
limits/rendering/max_lights=32
quality/filters/anisotropic_filter_level=4
```

## Platform-Specific Settings

### Windows

- Embed PCK: Single executable
- Code signing: For distribution
- Console: Hide for release

### Android

- Minimum SDK: 24
- Target SDK: 34
- Permissions: Internet, Vibrate
- Keystore: For signing

### iOS

- Bundle identifier: com.company.game
- Team ID: For signing
- Provisioning profile: Required

### Web

- HTML shell: Custom loading screen
- Canvas resize: Responsive
- Threads: Enable if needed

## Pre-Export Checklist

### Project Settings

- [ ] Set main scene
- [ ] Configure window size
- [ ] Set application name
- [ ] Configure icon

### Performance

- [ ] Enable appropriate renderer
- [ ] Set texture quality
- [ ] Configure shadow quality
- [ ] Optimize meshes

### Assets

- [ ] Compress textures
- [ ] Optimize audio formats
- [ ] Remove unused resources
- [ ] Set import settings

### Build

- [ ] Test export template
- [ ] Verify all scenes included
- [ ] Check resource paths
- [ ] Enable/disable debug features

## CI/CD Pipeline

### GitHub Actions

```yaml
name: Build and Export

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Godot
        uses: chickensoft-games/setup-godot@v1
        with:
          version: 4.3.0

      - name: Export Windows
        run: godot --headless --export-release "Windows" build/windows/game.exe

      - name: Export Linux
        run: godot --headless --export-release "Linux" build/linux/game.x86_64

      - name: Export Web
        run: godot --headless --export-release "Web" build/web/game.html

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: builds
          path: build/
```

## Distribution Platforms

### Steam

- Use Steamworks SDK
- Set up depot configuration
- Configure achievements
- Test with Steamworks

### itch.io

- Upload HTML5 for web
- Upload builds for desktop
- Set up page with screenshots

### Mobile Stores

- Google Play Store (Android)
- Apple App Store (iOS)
- Follow store guidelines

## Debug vs Release

```gdscript
if OS.is_debug_build():
    show_debug_info()
    enable_cheats()

if not OS.is_debug_build():
    disable_debug_logging()
    enable_analytics()
```

## Best Practices

1. **Test exports early**: Don't wait until release
2. **Use export presets**: Consistent builds
3. **Compress assets**: Reduce download size
4. **Platform testing**: Test on target hardware
5. **Version control**: Tag releases
6. **Automate builds**: CI/CD pipeline

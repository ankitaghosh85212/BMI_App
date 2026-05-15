[app]

# App Information
title = BMI Calculator
package.name = bmicalculator
package.domain = org.bmi

# Source files
source.dir = .
source.include_exts = py,png,txt,jpg,kv

# Version
version = 1.0

# Main requirements
requirements = python3,kivy==2.2.0,pillow

# Orientation
orientation = portrait

# Fullscreen app
fullscreen = 1

# Android settings
android.api = 33
android.minapi = 21
android.ndk = 25b

# Architecture
android.archs = arm64-v8a

# Permissions
android.permissions = INTERNET

# Accept SDK license automatically
android.accept_sdk_license = True

# Build stability
log_level = 2
warn_on_root = 0

# Appearance
presplash.color = #FFFFFF

# Exclude unnecessary files
source.exclude_dirs = tests, bin, venv, .git, __pycache__

# Include image files
android.add_assets = *.png

[app]

title = BMI Calculator

package.name = bmicalculator

package.domain = org.bmi

source.dir = .

source.include_exts = py,png,txt

version = 1.0

requirements = python3,kivy==2.3.0,pillow

orientation = portrait

fullscreen = 1

android.permissions = INTERNET

# FIXED SDK VERSION
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# IMPORTANT FIX
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

presplash.color = #FFFFFF

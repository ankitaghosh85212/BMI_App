[app]

title = BMI Calculator

package.name = bmicalculator
package.domain = org.bmi

source.dir = .
source.include_exts = py,png,txt

version = 1.0

requirements = python3,kivy==2.2.1,pillow

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

presplash.color = #FFFFFF

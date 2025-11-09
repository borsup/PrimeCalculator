[app]

# (str) Title of your application
title = Metal Calculator

# (str) Package name
package.name = MetalCalculator

# (str) Package domain (reverse domain style)
package.domain = com.borsup

# (str) Source code where the main.py live
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,kivymd,requests

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (str) Android entry point, default is ok
# entrypoint = org.kivy.android.PythonActivity

[buildozer]

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version
android.sdk = 33

# (int) NDK version
android.ndk = 25b

# (int) Android NDK API
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir (False)
android.private_storage = True

# (bool) Presplash screen
# presplash.filename = %(source.dir)s/data/presplash.png

# (bool) Orientation
# android.orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[app]
title = Finance Tracker
package.name = financetracker
package.domain = org.example

source.dir = .
source.include_exts = py

version = 1.0
requirements = python3,kivy,requests

orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 28
android.minapi = 21
android.accept_sdk_license = True

[app]
title = Kivy Gattlib Demo
package.name = kivygattlibdemo
package.domain = xloem.github.com
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1.7
requirements = kivy,python3,gattlib-py
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 1
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION
android.arch = armeabi-v7a
android.add_src = gattlib/*.java
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0
#p4a.fork = xloem
p4a.branch = develop
p4a.local_recipes = recipes

[buildozer]
log_level = 2
warn_on_root = 1

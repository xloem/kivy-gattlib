[app]
title = App
package.name = test 
package.domain = xloem.github.com
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1.7
requirements = kivy,bitcoin
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 1
android.permissions = CAMERA
android.arch = armeabi-v7a
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0
p4a.fork = xloem
p4a.branch = bitcoin-core

[buildozer]
log_level = 2
warn_on_root = 1

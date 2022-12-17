# Body Vendas / Body Sales (bodysales)
Aplicativo Body Vendas / Body Sales App

## Setup your PC (if you haven't in your pc)
### Node / npm
Install Node 10.16.0 / npm 6.9.0
Recommends using nvm (```brew install nvm``` using brew in Mac OS)
```
nvm install 10.16.0
```
### Yarn
Mac:
```
brew install yarn
```
### Cordova
```
npm install -g cordova
```
### Android Studio
Mac:
```
brew install --cask android-studio
```
After configure Android Studio installation like these: https://developer.android.com/studio/install
### Java JDK
Mac, download in:
https://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot
or:
https://www.oracle.com/java/technologies/downloads/#java8-mac
https://www.oracle.com/java/technologies/downloads/

## Configure Environment Variables
In your terminal configuration file (shell, bash or zsh)
```
export ANDROID_SDK_ROOT = "{$HOME}/Library/Android/sdk" (recommended setting)
export ANDROID_HOME = "{$HOME}/Library/Android/sdk" (DEPRECATED)
export $JAVA_HOME = "/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home"
```
{$HOME} = home path of your PC

## Install dependencies
```bash
yarn
```
### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```
### Build the app for production
```bash
quasar build
```

## Publishing to Store
See [Publishing to Store](https://v0-17.quasar-framework.org/guide/cordova-publishing-to-store.html).
### Android
#### Debug
```bash
quasar build -m android --debug
```
#### Production
```bash
quasar build -m android
```
The unsigned app is generated in project folder:
```
{$HOME}/body-sales/src-cordova/platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk
```
### iOS

### Sign app
With app .keystore file (body.keystore) using alias_name (body):
```
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore body.keystore <path-to-unsigned-apk-file> body
```
**This signs the apk in same place with same name (app-release-unsigned.apk)**. Finally, we need to run the zip align tool to optimize the APK. The zipalign tool can be found in /path/to/Android/sdk/build-tools/VERSION/zipalign. For example, on OS X with Android Studio installed, zipalign is in ~/Library/Android/sdk/build-tools/VERSION/zipalign:
```
./zipalign -v 4 <path-to-same-apk-file> body-signed.apk
```

### Build icons
#### New icons or compile with quasar/icon-genie already installed
Change ```"build_always": false``` to ```build_always: true``` in ```quasar.extensions.json``` to compile icons
https://github.com/quasarframework/app-extension-icon-genie/blob/dev/README.md

### Customize the configuration
See [Configuring quasar.conf.js](https://quasar.dev/quasar-cli/quasar-conf-js).

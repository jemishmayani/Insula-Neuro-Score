#!/usr/bin/env bash
# Builds a signed APK without Gradle using Ubuntu's Android tools:
#   apt-get install android-sdk-platform-23 aapt apksigner zipalign dalvik-exchange openjdk-21-jdk-headless
# Signing: set KEYSTORE, KS_PASS, KEY_ALIAS (defaults to a local debug-style keystore).
set -euo pipefail
cd "$(dirname "$0")"
SDK=$(ls /usr/lib/android-sdk/platforms/*/android.jar | head -1)
KEYSTORE=${KEYSTORE:-../keystore/local.keystore}; KS_PASS=${KS_PASS:-changeit}; KEY_ALIAS=${KEY_ALIAS:-insula}
if [ ! -f "$KEYSTORE" ]; then
  echo "No keystore at $KEYSTORE; generating a local one (keep it private and backed up: updates must be signed with the same key)."
  mkdir -p "$(dirname "$KEYSTORE")"
  keytool -genkeypair -keystore "$KEYSTORE" -alias "$KEY_ALIAS" -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" -dname "CN=Insula Neuro Score" >/dev/null
fi
rm -rf build && mkdir -p build/gen build/classes
aapt package -f -m -J build/gen -M AndroidManifest.xml -S res -I "$SDK"
javac --release 8 -nowarn -Xlint:-options -classpath "$SDK" -d build/classes build/gen/com/insula/neuroscore/R.java src/com/insula/neuroscore/*.java
dalvik-exchange --dex --output=build/classes.dex build/classes
aapt package -f -M AndroidManifest.xml -S res -A assets -I "$SDK" -F build/unsigned.apk
(cd build && aapt add unsigned.apk classes.dex >/dev/null)
zipalign -f -p 4 build/unsigned.apk build/aligned.apk
apksigner sign --ks "$KEYSTORE" --ks-pass "pass:$KS_PASS" --ks-key-alias "$KEY_ALIAS" --out build/InsulaNeuroScore.apk build/aligned.apk
apksigner verify build/InsulaNeuroScore.apk && echo "Built build/InsulaNeuroScore.apk"

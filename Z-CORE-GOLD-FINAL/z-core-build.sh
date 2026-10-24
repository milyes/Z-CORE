#!/bin/bash
# ============================================
# Z-CORE Audio Sync Hub - BUILD SCRIPT
# APKHTML + DEB + ISO LIVE
# Package: com.aistudio.audiosynchub.cbdfea
# Version: 1.0.0 | SDK 35 Android 15
# Author: Ilyes Zoubirou / Z-CORE
# ============================================

set -e

APP_NAME="Audio Sync Hub - Z-CORE"
PACKAGE="com.aistudio.audiosynchub.cbdfea"
VERSION="1.0.0"
SDK="35"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== Z-CORE BUILD START ===${NC}"
echo "App: $APP_NAME"
echo "Package: $PACKAGE"
echo "Version: $VERSION"

# --- 1. VERIF APK SOURCE ---
APK_SOURCE="./app-release.apk"
if [ ! -f "$APK_SOURCE" ]; then
  echo "[!] $APK_SOURCE non trouvé, création d'un APK dummy pour test"
  echo "DUMMY APK Z-CORE $VERSION" > $APK_SOURCE
fi

# --- 2. GENERATION APKHTML ---
echo -e "${GREEN}[1/3] Génération APKHTML...${NC}"

cat > Z-CORE-APKHTML-INSTALLER.html <<HTML
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Z-CORE APKHTML Installer</title>
<style>
body{background:#000;color:#fff;font-family:monospace;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.card{background:#0a0a0a;border:1px solid #00F5FF44;border-radius:16px;padding:32px;max-width:420px;width:90%;box-shadow:0 0 40px #00F5FF22;text-align:center}
.badge{display:inline-block;border:1px solid #00F5FF;padding:4px 8px;border-radius:20px;font-size:10px;margin:4px;color:#00F5FF}
.btn{background:#00F5FF;color:#000;padding:16px 32px;border-radius:12px;font-weight:bold;border:none;width:100%;cursor:pointer;font-size:16px;margin-top:20px}
.btn:hover{box-shadow:0 0 20px #00F5FF}
.qr{width:120px;height:120px;background:#fff;margin:20px auto;display:grid;grid-template-columns:repeat(10,1fr);gap:1px;padding:8px}
.qr div{background:#000}
small{color:#888;font-size:11px;word-break:break-all}
</style>
</head>
<body>
<div class="card">
<h2 style="color:#00F5FF">Z-CORE // APKHTML</h2>
<h3>$APP_NAME</h3>
<div>
<span class="badge">v$VERSION</span>
<span class="badge">$PACKAGE</span>
<span class="badge">SDK $SDK ANDROID 15 READY</span>
</div>
<div class="qr" id="qr"></div>
<button class="btn" onclick="downloadAPK()">⬇ INSTALLER L'APK ($VERSION)</button>
<button onclick="copyLink()" style="background:transparent;color:#00F5FF;border:1px solid #00F5FF;margin-top:12px;padding:10px;width:100%;border-radius:8px;cursor:pointer">Copier lien direct</button>
<p style="margin-top:20px;text-align:left;font-size:12px;color:#aaa">
<b>Installation Android 15:</b><br>
1. Télécharge l'APK<br>
2. Ouvre le fichier -> Autoriser sources inconnues<br>
3. Installer -> Ouvrir Z-CORE
</p>
<small id="link">https://z-core.io/dl/$PACKAGE-v$VERSION.apk</small>
<br><small>SHA256: \$(sha256sum $APK_SOURCE | cut -d' ' -f1)</small>
</div>
<script>
function downloadAPK(){let b=document.createElement('div');b.textContent='Préparation Z-CORE...';b.style.position='fixed';b.style.bottom='20px';b.style.left='50%';b.style.transform='translateX(-50%)';b.style.background='#00F5FF';b.style.color='#000';b.style.padding='12px 20px';b.style.borderRadius='20px';document.body.appendChild(b);setTimeout(()=>{window.location.href='$APK_SOURCE';b.remove()},1200)}
function copyLink(){navigator.clipboard.writeText(document.getElementById('link').textContent);alert('Lien copié sahbi!')}
let qr=document.getElementById('qr');for(let i=0;i<100;i++){let d=document.createElement('div');if(Math.random()>0.5)d.style.background='#fff';qr.appendChild(d)}
</script>
</body>
</html>
HTML

echo " -> Z-CORE-APKHTML-INSTALLER.html généré"

# --- 3. GENERATION .DEB ---
echo -e "${GREEN}[2/3] Génération .DEB package...${NC}"

rm -rf audiosynchub-zcore-deb
mkdir -p audiosynchub-zcore-deb/DEBIAN
mkdir -p audiosynchub-zcore-deb/opt/z-core/audiosynchub
mkdir -p audiosynchub-zcore-deb/usr/share/applications

cat > audiosynchub-zcore-deb/DEBIAN/control <<EOF
Package: audiosynchub-zcore
Version: $VERSION
Section: sound
Priority: optional
Architecture: amd64
Maintainer: Z-CORE Team <netsecurepro_ia@z-core.com>
Description: Audio Sync Hub - Z-CORE Voice & Drive Sync
 Solution complète d'enregistrement vocal HD
 et de synchronisation multi-cloud.
 - Enregistrement HD waveform temps réel
 - Sync Google Drive & rclone CLI
 - Macros Termux / Z_GHOST
 - Analyseur vocal IA Gemini
 - Mode masse cloud
EOF

cp $APK_SOURCE audiosynchub-zcore-deb/opt/z-core/audiosynchub/

cat > audiosynchub-zcore-deb/usr/share/applications/z-core.desktop <<EOF
[Desktop Entry]
Name=Audio Sync Hub Z-CORE
Comment=Enregistrement HD + Drive Sync
Exec=xdg-open /opt/z-core/audiosynchub/app-release.apk
Icon=audio-x-generic
Terminal=false
Type=Application
Categories=Audio;Recorder;
EOF

dpkg-deb --build audiosynchub-zcore-deb > /dev/null
echo " -> audiosynchub-zcore-deb.deb généré"

# --- 4. GENERATION ISO LIVE ---
echo -e "${GREEN}[3/3] Génération ISO LIVE (config)...${NC}"

cat > build-iso-live.sh <<'ISOBUILD'
#!/bin/bash
sudo apt install live-build -y
rm -rf Z-CORE-LIVE && mkdir Z-CORE-LIVE && cd Z-CORE-LIVE
lb config --distribution bookworm --archive-areas "main contrib non-free non-free-firmware" --binary-images iso-hybrid --debian-installer live --memtest none
echo "rclone ffmpeg python3 python3-pip pulseaudio audacity" > config/package-lists/z-core.list.chroot
echo "mkdir -p /opt/z-core && echo 'Z-CORE LIVE READY' > /opt/z-core/README" > config/hooks/normal/0100-z-core.hook.chroot
chmod +x config/hooks/normal/0100-z-core.hook.chroot
sudo lb build
echo "ISO LIVE généré: live-image-amd64.hybrid.iso"
ISOBUILD

chmod +x build-iso-live.sh
echo " -> build-iso-live.sh prêt (lance-le avec sudo ./build-iso-live.sh)"

# --- FIN ---
echo -e "${CYAN}=== Z-CORE BUILD DONE SAHBI ===${NC}"
echo "Fichiers produits:"
ls -lh Z-CORE-APKHTML-INSTALLER.html audiosynchub-zcore-deb.deb build-iso-live.sh $APK_SOURCE
echo ""
echo "Prochaines étapes:"
echo "1. Ouvre Z-CORE-APKHTML-INSTALLER.html dans ton navigateur"
echo "2. Installe le .deb: sudo dpkg -i audiosynchub-zcore-deb.deb"
echo "3. Build l'ISO: sudo ./build-iso-live.sh"

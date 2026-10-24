#!/bin/bash
# ============================================
# Z-CORE - BUILD CAT EOF EDITION
# Package: com.aistudio.audiosynchub.cbdfea
# Version: 1.0.0 SDK 35
# ============================================

set -e

PACKAGE="com.aistudio.audiosynchub.cbdfea"
VERSION="1.0.0"

# 1 - APKHTML
cat <<'HTMLEOF' > Z-CORE-APKHTML.html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Z-CORE APKHTML</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:monospace;min-height:100vh;display:flex;justify-content:center;align-items:center}
.card{background:#0a0a0a;border:1px solid #00F5FF44;border-radius:20px;padding:30px;width:95%;max-width:430px;text-align:center;box-shadow:0 0 50px #00F5FF22}
.badge{border:1px solid #00F5FF;color:#00F5FF;padding:4px 10px;border-radius:20px;font-size:10px;margin:3px;display:inline-block}
.btn{background:#00F5FF;color:#000;padding:18px;width:100%;border:none;border-radius:12px;font-weight:900;font-size:16px;cursor:pointer;margin-top:20px}
.btn2{background:transparent;color:#00F5FF;border:1px solid #00F5FF;padding:12px;width:100%;border-radius:10px;margin-top:10px;cursor:pointer}
.qr{width:130px;height:130px;background:#fff;margin:20px auto;padding:10px;display:grid;grid-template-columns:repeat(10,1fr);gap:2px}
.qr div{background:#000}
.qr div.w{background:#fff}
</style>
</head>
<body>
<div class="card">
<h1 style="color:#00F5FF;letter-spacing:3px">Z-CORE</h1>
<h3>APKHTML INSTALLER</h3>
<p style="color:#888;font-size:12px;margin:10px 0">Audio Sync Hub - Voice & Drive Sync</p>
<div>
<span class="badge">v1.0.0</span>
<span class="badge">com.aistudio.audiosynchub.cbdfea</span>
<span class="badge">SDK 35 ANDROID 15 READY</span>
</div>
<div class="qr" id="qr"></div>
<button class="btn" onclick="install()">⬇ INSTALLER APK Z-CORE</button>
<button class="btn2" onclick="copyL()">📋 COPIER LIEN DIRECT</button>
<div style="text-align:left;margin-top:25px;background:#111;padding:15px;border-radius:10px;font-size:11px;color:#aaa">
<b style="color:#fff">INSTALLATION:</b><br>
1. Télécharge APK<br>
2. Autoriser sources inconnues<br>
3. Installer > Ouvrir<br><br>
<b style="color:#fff">FEATURES:</b><br>
• HD Recording + Waveform<br>
• Drive & rclone Sync<br>
• Termux / Z_GHOST Macros<br>
• Gemini AI Voice Analyzer<br>
• Bulk Cloud Transfer
</div>
<small id="link" style="display:block;margin-top:15px;color:#555;word-break:break-all">https://github.com/netsecurepro_ia/z-core/releases/download/v1.0.0/app-release.apk</small>
</div>
<script>
const q=document.getElementById('qr');
for(let i=0;i<100;i++){let d=document.createElement('div');d.className=Math.random()>0.45?'w':'';q.appendChild(d)}
function install(){
let t=document.createElement('div');
t.textContent='Z-CORE DOWNLOAD...';
Object.assign(t.style,{position:'fixed',bottom:'30px',left:'50%',transform:'translateX(-50%)',background:'#00F5FF',color:'#000',padding:'12px 24px',borderRadius:'30px',fontWeight:'bold'});
document.body.appendChild(t);
setTimeout(()=>{window.location.href=document.getElementById('link').textContent; t.remove()},1000);
}
function copyL(){navigator.clipboard.writeText(document.getElementById('link').textContent); alert('Lien copié sahbi!');}
</script>
</body>
</html>
HTMLEOF

# 2 - CONTROL DEB
cat <<'DEBEOF' > control
Package: audiosynchub-zcore
Version: 1.0.0
Section: sound
Priority: optional
Architecture: amd64
Maintainer: Z-CORE <netsecurepro_ia@z-core.com>
Description: Audio Sync Hub Z-CORE Voice & Drive Sync
 Solution complète d'enregistrement vocal HD
 et de synchronisation multi-cloud pour Android et Debian Live.
  - Enregistrement HD avec visualiseur waveform
  - Synchronisation Google Drive & rclone CLI
  - Gestionnaire macros Termux / Z_GHOST
  - Analyseur vocal IA Gemini
  - Mode sélection masse cloud
 Package: com.aistudio.audiosynchub.cbdfea SDK 35.
DEBEOF

# 3 - DESKTOP FILE
cat <<'DESKTOPEOF' > z-core.desktop
[Desktop Entry]
Name=Audio Sync Hub Z-CORE
Comment=Voice & Drive Sync - SDK 35
Exec=xdg-open /opt/z-core/app.apk
Icon=audio-x-generic
Terminal=false
Type=Application
Categories=AudioVideo;Recorder;
Keywords=audio;recorder;drive;rclone;gemini;
DESKTOPEOF

# 4 - BUILD DEB SCRIPT
cat <<'BUILDEOF' > build-deb.sh
#!/bin/bash
set -e
rm -rf pkg-deb
mkdir -p pkg-deb/DEBIAN
mkdir -p pkg-deb/opt/z-core
mkdir -p pkg-deb/usr/share/applications
cp control pkg-deb/DEBIAN/control
cp z-core.desktop pkg-deb/usr/share/applications/
[ -f app-release.apk ] && cp app-release.apk pkg-deb/opt/z-core/app.apk || echo "dummy apk" > pkg-deb/opt/z-core/app.apk
dpkg-deb --build pkg-deb audiosynchub-zcore_1.0.0_amd64.deb
echo "[OK] DEB généré: audiosynchub-zcore_1.0.0_amd64.deb"
BUILDEOF

# 5 - BUILD ISO LIVE SCRIPT
cat <<'ISOEOF' > build-iso.sh
#!/bin/bash
set -e
sudo apt update && sudo apt install live-build -y
rm -rf Z-CORE-LIVE
mkdir Z-CORE-LIVE && cd Z-CORE-LIVE
lb config --distribution bookworm --archive-areas "main contrib non-free non-free-firmware" --binary-images iso-hybrid --debian-installer live --memtest none --iso-volume "Z-CORE LIVE 1.0.0"
mkdir -p config/package-lists
cat <<'PKGLIST' > config/package-lists/z-core.list.chroot
rclone
ffmpeg
audacity
pulseaudio
python3
python3-pip
calamares
PKGLIST
mkdir -p config/hooks/normal
cat <<'HOOK' > config/hooks/normal/0100-zcore.hook.chroot
#!/bin/bash
mkdir -p /opt/z-core
echo "Z-CORE Audio Sync Hub v1.0.0 - com.aistudio.audiosynchub.cbdfea" > /opt/z-core/VERSION
echo "Build Live OK" > /opt/z-core/README
HOOK
chmod +x config/hooks/normal/0100-zcore.hook.chroot
sudo lb build
echo "[OK] ISO LIVE: live-image-amd64.hybrid.iso"
ISOEOF

chmod +x build-deb.sh build-iso.sh

cat <<'FINALEOF'
============================================
Z-CORE CAT EOF BUILD - DONE SAHBI
============================================
Fichiers créés:
 -> Z-CORE-APKHTML.html (APKHTML installer)
 -> control (DEB control)
 -> z-core.desktop
 -> build-deb.sh (génère .deb)
 -> build-iso.sh (génère ISO LIVE)

Usage:
 ./build-deb.sh        -> produit .deb
 ./build-iso.sh        -> produit ISO (sudo)
 Ouvre Z-CORE-APKHTML.html dans navigateur

Package: com.aistudio.audiosynchub.cbdfea
Version: 1.0.0 SDK 35 Android 15 Ready
============================================
FINALEOF

echo ""
ls -lh Z-CORE-APKHTML.html control z-core.desktop build-deb.sh build-iso.sh
echo ""
echo "SAHBI - Tous les fichiers en CAT EOF sont prêts!"

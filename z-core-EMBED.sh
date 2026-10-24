#!/bin/bash
# Z-CORE EMBED BASE64 EDITION - APK DANS LE HTML
# 100% autonome, CAT EOF, Base64
# Package: com.aistudio.audiosynchub.cbdfea v1.0.0
set -e

APK="app-release.apk"
HTML="Z-CORE-APKHTML-EMBED.html"

[ -f "$APK" ] || echo "Z-CORE DUMMY APK v1.0.0 com.aistudio.audiosynchub.cbdfea" > "$APK"

echo "[Z-CORE] Encodage Base64 de $APK..."
B64=$(base64 -w 0 "$APK")
SHA=$(sha256sum "$APK" | cut -d' ' -f1)
SIZE=$(du -h "$APK" | cut -f1)

echo "[Z-CORE] Génération HTML autonome $SIZE SHA $SHA"

cat <<HTMLHEAD > "$HTML"
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Z-CORE EMBED v1.0.0</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:monospace;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}.card{background:#0a0a0a;border:1px solid #00F5FF66;border-radius:22px;padding:30px;width:100%;max-width:440px;text-align:center;box-shadow:0 0 70px #00F5FF22}.badge{border:1px solid #00F5FF;color:#00F5FF;padding:4px 10px;border-radius:20px;font-size:10px;margin:3px;display:inline-block}.btn{background:#00F5FF;color:#000;padding:18px;width:100%;border:none;border-radius:12px;font-weight:900;font-size:16px;cursor:pointer;margin-top:18px;letter-spacing:1px}.btn2{background:transparent;color:#00F5FF;border:1px solid #00F5FF;padding:11px;width:100%;border-radius:10px;margin-top:10px;cursor:pointer}.progress{width:100%;height:6px;background:#111;border-radius:10px;margin-top:15px;overflow:hidden;display:none}.bar{height:100%;width:0%;background:#00F5FF;transition:width 0.2s}.qr{width:120px;height:120px;background:#fff;margin:18px auto;padding:8px;display:grid;grid-template-columns:repeat(10,1fr);gap:2px}.qr div{background:#000}.qr div.w{background:#fff}</style>
</head><body><div class="card"><h1 style="color:#00F5FF;letter-spacing:5px">Z-CORE</h1><h3>EMBED APKHTML</h3><p style="color:#666;font-size:10px;margin:6px 0">BIN_ISO-LIVE_DEB EDITION - 100% AUTONOME</p><div><span class="badge">v1.0.0</span><span class="badge">com.aistudio.audiosynchub.cbdfea</span><span class="badge">SDK35</span><span class="badge">EMBED BASE64</span></div><div class="qr" id="qr"></div>
<div style="background:#111;padding:10px;border-radius:8px;margin-top:10px;font-size:10px;text-align:left;color:#888">SIZE: SIZE_PLACEHOLDER<br>SHA256: SHA_PLACEHOLDER<br>TYPE: BASE64 EMBEDDED APK</div>
<button class="btn" id="dlBtn" onclick="extractAPK()">⬇ EXTRACT & INSTALL APK</button><div class="progress" id="prog"><div class="bar" id="bar"></div></div><button class="btn2" onclick="copyInfo()">📋 COPIER SHA256</button><div style="text-align:left;margin-top:18px;background:#0e0e0e;padding:12px;border-radius:10px;font-size:11px;color:#777"><b style="color:#fff">Ce HTML contient l'APK dedans:</b><br>• Pas besoin de serveur<br>• Pas de lien Drive<br>• Ouvre ce HTML partout et extrait l'APK<br>• 100% offline après ouverture</div></div>
<script>
const apkBase64 = "
HTMLHEAD

# Inject base64
echo -n "$B64" >> "$HTML"

cat <<'HTMLTAIL' >> "$HTML"
";
const apkName = "AudioSyncHub-Z-CORE-v1.0.0.apk";
const qr=document.getElementById('qr');for(let i=0;i<100;i++){let d=document.createElement('div');d.className=Math.random()>0.48?'w':'';qr.appendChild(d)}
function extractAPK(){
const prog=document.getElementById('prog');const bar=document.getElementById('bar');const btn=document.getElementById('dlBtn');
prog.style.display='block';btn.textContent='⏳ DECODAGE BASE64...';let w=0;
let iv=setInterval(()=>{w+=Math.random()*25;if(w>90)w=90;bar.style.width=w+'%';},120);
try{
const binaryString = atob(apkBase64);
const len = binaryString.length;
const bytes = new Uint8Array(len);
for(let i=0;i<len;i++){bytes[i]=binaryString.charCodeAt(i);}
bar.style.width='100%';clearInterval(iv);
const blob = new Blob([bytes], {type: 'application/vnd.android.package-archive'});
const url = URL.createObjectURL(blob);
const a=document.createElement('a');a.href=url;a.download=apkName;document.body.appendChild(a);a.click();
setTimeout(()=>{URL.revokeObjectURL(url);a.remove();btn.textContent='✅ APK EXTRAIT SAHBI!';prog.style.display='none';},800);
}catch(e){clearInterval(iv);alert('Erreur extract: '+e);btn.textContent='❌ ERREUR';}
}
function copyInfo(){navigator.clipboard.writeText(document.getElementById('lnk')?document.getElementById('lnk').textContent:location.href);alert('Copié sahbi!');}
</script></body></html>
HTMLTAIL

# Remplace placeholders
sed -i "s/SIZE_PLACEHOLDER/$SIZE/g" "$HTML"
sed -i "s/SHA_PLACEHOLDER/$SHA/g" "$HTML"

echo ""
echo "=================================="
echo " Z-CORE EMBED DONE SAHBI"
echo "=================================="
ls -lh "$HTML" "$APK"
echo ""
echo "Ce HTML est 100% autonome:"
echo " - Ouvre $HTML dans Chrome"
echo " - Clique EXTRACT & INSTALL"
echo " - Il te sort l'APK direct depuis le base64"
echo ""
echo "Aucun serveur, aucun lien, BIN_ISO-LIVE_DEB style"

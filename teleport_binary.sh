#!/bin/bash

TARGET_DIR="$HOME/z_core/bin_store"
mkdir -p "$TARGET_DIR"

if [ -n "$1" ]; then
    NOM_BIN=$(basename "$1")
    echo "[*] Téléportation binaire distante vers local..."
    curl -L -# "$1" -o "$TARGET_DIR/$NOM_BIN"
    if [ $? -eq 0 ]; then
        echo "[✓] Confinement validé : $TARGET_DIR/$NOM_BIN"
    else
        echo "[!] Erreur lors du téléchargement."
    fi
else
    echo "[!] Usage : ./teleport_binary.sh <URL_SOURCE>"
fi

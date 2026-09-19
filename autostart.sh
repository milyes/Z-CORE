#!/bin/bash

# Configuration du lancement automatique dans .bashrc si absent
BASHRC="$HOME/.bashrc"
AUTO_CMD="cd $HOME/z_core && ./master_orchestrator.sh"

if ! grep -q "master_orchestrator.sh" "$BASHRC" 2>/dev/null; then
    echo "" >> "$BASHRC"
    echo "# Lancement automatique Z-CORE" >> "$BASHRC"
    echo "# $AUTO_CMD" >> "$BASHRC"
    echo "[✓] Configuration autostart ajoutée dans $BASHRC"
else
    echo "[✓] Autostart déjà configuré dans $BASHRC"
fi

#!/bin/bash
# Ins Verzeichnis dieses Scripts wechseln
cd "$(dirname "$0")"

# Python 3 prüfen
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 nicht gefunden. Bitte unter https://python.org installieren."
    read -p "Enter drücken zum Beenden..."
    exit 1
fi

python3 interactive.py

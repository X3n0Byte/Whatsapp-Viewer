#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import subprocess
from typing import Optional

# ── Plattform erkennen ───────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS   = sys.platform == 'darwin'


# ── ANSI-Farben (Windows: VT100 aktivieren, Fallback: keine Farben) ──────────
def _enable_ansi_windows():
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        return True
    except Exception:
        return False

if IS_WINDOWS:
    _ansi = _enable_ansi_windows()
else:
    _ansi = True

G  = '\033[92m' if _ansi else ''
B  = '\033[94m' if _ansi else ''
Y  = '\033[93m' if _ansi else ''
R  = '\033[91m' if _ansi else ''
W  = '\033[0m'  if _ansi else ''
BD = '\033[1m'  if _ansi else ''

# ── Pfade ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_TXT    = os.path.join(SCRIPT_DIR, 'input_txt')
DIR_MEDIA  = os.path.join(SCRIPT_DIR, 'input_media')
DIR_OUTPUT = os.path.join(SCRIPT_DIR, 'output')


# ── Hilfsfunktionen ──────────────────────────────────────────────────────────

def banner():
    os_label = 'Windows' if IS_WINDOWS else 'macOS'
    print(f"""
{G}╔══════════════════════════════════════════╗
║        WhatsApp Chat Viewer              ║
║        {os_label} Interaktiver Starter       ║
╚══════════════════════════════════════════╝{W}
""")


def ensure_dirs():
    for d in (DIR_TXT, DIR_MEDIA, DIR_OUTPUT):
        os.makedirs(d, exist_ok=True)
    print(f"{BD}Ordnerstruktur:{W}")
    print(f"  {G}input_txt/{W}   → Chat-Datei ablegen (_chat.txt)")
    print(f"  {G}input_media/{W} → Mediendateien ablegen")
    print(f"  {G}output/{W}      → Hier erscheint die fertige chat.html")
    print()


def open_in_browser(path: str):
    """Öffnet eine Datei im Standardbrowser, plattformübergreifend."""
    if IS_WINDOWS:
        os.startfile(path)
    elif IS_MACOS:
        subprocess.run(['open', path])
    else:
        subprocess.run(['xdg-open', path])


def clean_path(raw: str) -> str:
    """
    Bereinigt Drag-&-Drop Pfade aus Terminal/CMD/PowerShell.
    - Entfernt umschließende Anführungszeichen
    - Entfernt macOS-Backslash-Escapes (z.B. Ordner name mit Leerzeichen)
    - Normalisiert Windows-Pfade
    """
    p = raw.strip()
    # Anführungszeichen (einfach oder doppelt) entfernen
    if len(p) >= 2 and p[0] in ('"', "'") and p[-1] == p[0]:
        p = p[1:-1]
    # macOS: Leerzeichen-Escapes auflösen
    if not IS_WINDOWS:
        p = p.replace('\\ ', ' ')
    # Windows: normalisieren
    p = os.path.normpath(p) if IS_WINDOWS else p
    return p


def find_txt_in_dir(directory: str) -> Optional[str]:
    hits = glob.glob(os.path.join(directory, '*.txt'))
    return hits[0] if len(hits) == 1 else None


def copy_chat(src: str) -> str:
    dest = os.path.join(DIR_TXT, os.path.basename(src))
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.copy2(src, dest)
        print(f"  {G}✓ Kopiert nach input_txt/{os.path.basename(src)}{W}\n")
    return dest


def copy_media(src_dir: str) -> str:
    files = [
        f for f in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, f)) and not f.startswith('.')
    ]
    copied = 0
    for f in files:
        dest = os.path.join(DIR_MEDIA, f)
        if os.path.abspath(os.path.join(src_dir, f)) != os.path.abspath(dest):
            shutil.copy2(os.path.join(src_dir, f), dest)
            copied += 1
    if copied:
        print(f"  {G}✓ {copied} Mediendateien kopiert nach input_media/{W}\n")
    else:
        print(f"  {G}✓ Mediendateien bereits in input_media/{W}\n")
    return DIR_MEDIA


# ── Interaktive Schritte ─────────────────────────────────────────────────────

def ask_chat_path() -> str:
    auto = find_txt_in_dir(DIR_TXT)
    if auto:
        print(f"{B}Schritt 1/4 — Chat-Datei{W}")
        print(f"  {G}✓ Automatisch gefunden:{W} {auto}\n")
        return auto

    print(f"{B}Schritt 1/4 — Chat-Datei (_chat.txt){W}")
    print(f"  {Y}Keine .txt Datei in input_txt/ gefunden.{W}")
    if IS_WINDOWS:
        print(f"  Datei per Drag & Drop ins Fenster ziehen oder Pfad eingeben:")
    else:
        print(f"  Datei per Drag & Drop ins Terminal ziehen oder Pfad eingeben:")
    while True:
        path = clean_path(input('  > '))
        if os.path.isfile(path):
            return copy_chat(path)
        print(f"  {R}Datei nicht gefunden: {path}{W}")


def ask_media_path() -> Optional[str]:
    media_files = [
        f for f in os.listdir(DIR_MEDIA)
        if not f.startswith('.') and os.path.isfile(os.path.join(DIR_MEDIA, f))
    ]
    if media_files:
        print(f"{B}Schritt 2/4 — Medienordner{W}")
        print(f"  {G}✓ input_media/ erkannt ({len(media_files)} Dateien){W}\n")
        return DIR_MEDIA

    print(f"{B}Schritt 2/4 — Medienordner{W}")
    print(f"  {Y}input_media/ ist leer.{W}")
    if IS_WINDOWS:
        print(f"  Ordner per Drag & Drop ins Fenster ziehen oder Enter überspringen:")
    else:
        print(f"  Ordner per Drag & Drop ins Terminal ziehen oder Enter überspringen:")
    raw = input('  > ').strip()
    if not raw:
        print(f"  Ohne Medien fortfahren.\n")
        return None
    path = clean_path(raw)
    if os.path.isdir(path):
        return copy_media(path)
    print(f"  {Y}⚠ Ordner nicht gefunden – ohne Medien fortfahren.{W}\n")
    return None


def ask_sender(senders: list) -> str:
    print(f"{B}Schritt 3/4 — Wer bist du? (Nachrichten erscheinen {G}rechts/grün{W}{B}){W}")
    for i, name in enumerate(senders, 1):
        print(f"  {BD}[{i}]{W} {name}")
    print()
    while True:
        raw = input(f"  Nummer eingeben (1-{len(senders)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(senders):
            chosen = senders[int(raw) - 1]
            print(f"  {G}✓ Du bist: {chosen}{W}\n")
            return chosen
        print(f"  {R}Ungültige Eingabe.{W}")


def ask_embed(media_path: str) -> bool:
    total_bytes = sum(
        os.path.getsize(os.path.join(media_path, f))
        for f in os.listdir(media_path)
        if os.path.isfile(os.path.join(media_path, f)) and not f.startswith('.')
    )
    total_mb   = total_bytes / (1024 * 1024)
    est_mb     = total_mb * 1.37

    print(f"{B}Schritt 4/4 — Ausgabemodus{W}")
    print(f"  {BD}[1]{W} {G}Eingebettet{W}  – alle Medien direkt in die HTML (eine einzige Datei)")
    print(f"       → komplett portabel, kein Ordner nötig, ideal als Backup")
    print(f"       → geschätzte Dateigröße: ~{est_mb:.0f} MB")
    if total_mb > 200:
        print(f"  {Y}       ⚠ Sehr viele Medien ({total_mb:.0f} MB) – Browser könnte langsam laden{W}")
    print(f"  {BD}[2]{W} Relativ        – HTML verweist auf input_media/ (Ordner muss erhalten bleiben)")
    print()
    while True:
        raw = input("  Auswahl (1/2): ").strip()
        if raw == '1':
            print(f"  {G}✓ Eingebetteter Modus{W}\n")
            return True
        if raw == '2':
            print(f"  {G}✓ Relativer Modus{W}\n")
            return False
        print(f"  {R}Bitte 1 oder 2 eingeben.{W}")


# ── Hauptprogramm ────────────────────────────────────────────────────────────

def main():
    banner()
    ensure_dirs()

    sys.path.insert(0, SCRIPT_DIR)
    from parse_chat import parse_chat
    from generate_html import generate_html

    chat_path  = ask_chat_path()
    media_path = ask_media_path()

    print(f"{B}Chat analysieren …{W}")
    messages = parse_chat(chat_path)
    senders  = sorted({m['sender'] for m in messages if m['sender'] and not m['is_system']})
    print(f"  {G}✓ {len(messages)} Nachrichten, {len(senders)} Absender: {', '.join(senders)}{W}\n")

    if not senders:
        print(f"{R}Keine Absender gefunden. Bitte Chat-Datei prüfen.{W}")
        input("\nEnter zum Beenden …")
        sys.exit(1)

    me    = ask_sender(senders)
    embed = ask_embed(media_path) if media_path else False

    output_path = os.path.join(DIR_OUTPUT, 'chat.html')
    generate_html(messages=messages, me=me, media_dir=media_path,
                  output_path=output_path, embed=embed)

    print(f"\n{G}Im Browser öffnen …{W}")
    open_in_browser(output_path)

    print(f"\n{BD}Fertig! Drücke Enter zum Beenden.{W}")
    input()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Y}Abgebrochen.{W}\n")

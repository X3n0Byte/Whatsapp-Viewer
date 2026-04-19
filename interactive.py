#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import subprocess

# ── Farben ──────────────────────────────────────────────────────────────────
G  = '\033[92m'
B  = '\033[94m'
Y  = '\033[93m'
R  = '\033[91m'
W  = '\033[0m'
BD = '\033[1m'

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DIR_TXT     = os.path.join(SCRIPT_DIR, 'input_txt')
DIR_MEDIA   = os.path.join(SCRIPT_DIR, 'input_media')
DIR_OUTPUT  = os.path.join(SCRIPT_DIR, 'output')


def banner():
    print(f"""
{G}╔══════════════════════════════════════════╗
║        WhatsApp Chat Viewer              ║
║        macOS Interaktiver Starter        ║
╚══════════════════════════════════════════╝{W}
""")


def ensure_dirs():
    """Erstellt die Ordnerstruktur falls nicht vorhanden."""
    for d in (DIR_TXT, DIR_MEDIA, DIR_OUTPUT):
        os.makedirs(d, exist_ok=True)
    print(f"{BD}Ordnerstruktur:{W}")
    print(f"  {G}input_txt/{W}   → Chat-Datei ablegen (_chat.txt)")
    print(f"  {G}input_media/{W} → Mediendateien ablegen")
    print(f"  {G}output/{W}      → Hier erscheint die fertige chat.html")
    print()


def clean_path(raw: str) -> str:
    p = raw.strip()
    if len(p) >= 2 and p[0] in ('"', "'") and p[-1] == p[0]:
        p = p[1:-1]
    p = p.replace('\\ ', ' ')
    return p


def find_txt_in_dir(directory: str) -> str | None:
    """Sucht automatisch nach einer .txt Datei im Ordner."""
    hits = glob.glob(os.path.join(directory, '*.txt'))
    return hits[0] if len(hits) == 1 else None


def copy_chat(src: str) -> str:
    """Kopiert die Chat-Datei nach input_txt/ und gibt den neuen Pfad zurück."""
    dest = os.path.join(DIR_TXT, os.path.basename(src))
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.copy2(src, dest)
        print(f"  {G}✓ Kopiert nach input_txt/{os.path.basename(src)}{W}\n")
    return dest


def copy_media(src_dir: str) -> str:
    """Kopiert alle Dateien aus src_dir nach input_media/ und gibt input_media/ zurück."""
    files = [f for f in os.listdir(src_dir)
             if os.path.isfile(os.path.join(src_dir, f)) and not f.startswith('.')]
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


def ask_chat_path() -> str:
    auto = find_txt_in_dir(DIR_TXT)
    if auto:
        print(f"{B}Schritt 1/3 — Chat-Datei{W}")
        print(f"  {G}✓ Automatisch gefunden:{W} {auto}\n")
        return auto

    print(f"{B}Schritt 1/3 — Chat-Datei (_chat.txt){W}")
    print(f"  {Y}Keine .txt Datei in input_txt/ gefunden.{W}")
    print(f"  Datei per Drag & Drop ins Fenster ziehen oder Pfad eingeben:")
    while True:
        path = clean_path(input('  > ').strip())
        if os.path.isfile(path):
            return copy_chat(path)
        print(f"  {R}Datei nicht gefunden: {path}{W}")


def ask_media_path() -> str | None:
    media_files = [
        f for f in os.listdir(DIR_MEDIA)
        if not f.startswith('.') and os.path.isfile(os.path.join(DIR_MEDIA, f))
    ]
    if media_files:
        print(f"{B}Schritt 2/3 — Medienordner{W}")
        print(f"  {G}✓ input_media/ erkannt ({len(media_files)} Dateien){W}\n")
        return DIR_MEDIA

    print(f"{B}Schritt 2/3 — Medienordner{W}")
    print(f"  {Y}input_media/ ist leer.{W}")
    print(f"  Ordner per Drag & Drop ins Fenster ziehen oder Enter überspringen:")
    raw = input('  > ').strip()
    if not raw:
        print(f"  Ohne Medien fortfahren.\n")
        return None
    path = clean_path(raw)
    if os.path.isdir(path):
        return copy_media(path)
    print(f"  {Y}⚠ Ordner nicht gefunden – ohne Medien fortfahren.{W}\n")
    return None


def ask_sender(senders: list[str]) -> str:
    print(f"{B}Schritt 3/3 — Wer bist du? (Nachrichten erscheinen {G}rechts/grün{W}{B}){W}")
    for i, name in enumerate(senders, 1):
        print(f"  {BD}[{i}]{W} {name}")
    print()
    while True:
        raw = input(f"  Nummer eingeben (1–{len(senders)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(senders):
            chosen = senders[int(raw) - 1]
            print(f"  {G}✓ Du bist: {chosen}{W}\n")
            return chosen
        print(f"  {R}Ungültige Eingabe.{W}")


def main():
    banner()
    ensure_dirs()

    sys.path.insert(0, SCRIPT_DIR)
    from parse_chat import parse_chat
    from generate_html import generate_html

    # ── 1. Chat-Datei ────────────────────────────────────────────────────────
    chat_path = ask_chat_path()

    # ── 2. Medienordner ──────────────────────────────────────────────────────
    media_path = ask_media_path()

    # ── Chat analysieren ─────────────────────────────────────────────────────
    print(f"{B}Chat analysieren …{W}")
    messages = parse_chat(chat_path)
    senders = sorted({m['sender'] for m in messages if m['sender'] and not m['is_system']})
    print(f"  {G}✓ {len(messages)} Nachrichten, {len(senders)} Absender: {', '.join(senders)}{W}\n")

    if not senders:
        print(f"{R}Keine Absender gefunden. Bitte Chat-Datei prüfen.{W}")
        sys.exit(1)

    # ── 3. Absender wählen ───────────────────────────────────────────────────
    me = ask_sender(senders)

    # ── HTML generieren ──────────────────────────────────────────────────────
    output_path = os.path.join(DIR_OUTPUT, 'chat.html')
    generate_html(messages=messages, me=me, media_dir=media_path, output_path=output_path)

    # ── Im Browser öffnen ────────────────────────────────────────────────────
    print(f"\n{G}Im Browser öffnen …{W}")
    subprocess.run(['open', output_path])

    print(f"\n{BD}Fertig! Drücke Enter zum Beenden.{W}")
    input()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Y}Abgebrochen.{W}\n")

# WhatsApp Chat Viewer

Konvertiert exportierte WhatsApp-Chats (`.txt` + Medien) in eine übersichtliche, offline-fähige HTML-Datei — direkt im Browser, ohne Installation, ohne Internetverbindung.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) ![macOS](https://img.shields.io/badge/macOS-Monterey%2B-black?logo=apple) ![Windows](https://img.shields.io/badge/Windows-11%20x64-blue?logo=windows) ![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)

---

## Features

- **WhatsApp-Design** — grüne Blasen rechts (du), weiße Blasen links (andere)
- **Medienvorschau** — Bilder, Videos und Audios direkt im Browser
- **Bildergalerie** — Klick auf ein Bild öffnet es in einem Lightbox-Overlay
- **Sticky Datums-Trenner** — automatische Tagesgruppen beim Scrollen
- **Interaktiver Starter** — kein Terminal-Wissen nötig, Drag & Drop
- **Zwei Ausgabemodi** — eingebettete HTML (eine einzige Datei) oder relative Pfade (portabler Ordner)
- **Vollständiges Backup** — alle Medien als Base64 direkt in die HTML einbetten, eine Datei genügt
- **Plattformübergreifend** — läuft auf macOS und Windows 11 (x64)
- **Offline & privat** — keine externen Server, keine Abhängigkeiten außer Python
- **Beide Exportformate** — `[DD.MM.YY, HH:MM:SS]` und `DD.MM.YY, HH:MM -`

---

## Voraussetzungen

### macOS (Monterey oder neuer)

- **Python 3.9+** — im Terminal prüfen:
  ```bash
  python3 --version
  ```
  Falls nicht vorhanden: [python.org/downloads](https://www.python.org/downloads/)

### Windows 11 (x64)

- **Python 3.9+** — in der Eingabeaufforderung prüfen:
  ```cmd
  python --version
  ```
  Falls nicht vorhanden: [python.org/downloads](https://www.python.org/downloads/)
  > **Wichtig beim Installieren:** „**Add Python to PATH**" aktivieren!

---

## Chat exportieren (WhatsApp)

1. WhatsApp öffnen → Chat antippen
2. Oben rechts **⋮ → Mehr → Chat exportieren**
3. **„Medien einschließen"** wählen
4. Datei auf den Computer übertragen (AirDrop, USB, iCloud, etc.)
5. ZIP entpacken → enthält `_chat.txt` und alle Mediendateien

---

## Vorbereitung (Best Practice)

Damit alle Bilder, Videos und Audios korrekt verarbeitet werden, sollten die Medien **vor dem Start** in den Projektordner kopiert werden:

1. Das WhatsApp-Backup-ZIP entpacken
2. Den Ordner `input_media/` im Projektverzeichnis öffnen — er ist zunächst **leer**
3. **Alle Mediendateien** aus dem entpackten Backup nach `input_media/` kopieren  
   *(alle Dateien außer `_chat.txt` auswählen und hineinziehen)*

So erkennt der Viewer die Medien beim Start automatisch — kein manuelles Ziehen nötig.

---

## Verwendung

### Variante A — Interaktiver Starter (empfohlen)

#### macOS

1. Repository herunterladen oder klonen

2. **Ausführungsrechte setzen** (einmalig, nach dem Download nötig):
   ```bash
   cd ~/Downloads/whatsapp-viewer
   chmod +x "WhatsappViewerStart.command"
   ```
   > **Fehlermeldung „Zugriff verweigert" / „access privileges"?**  
   > GitHub entfernt beim Download die Ausführungsrechte. Der `chmod`-Befehl oben behebt das dauerhaft.

3. **Doppelklick** auf `WhatsappViewerStart.command`
   > Beim ersten Start fragt macOS nach Erlaubnis → *Systemeinstellungen → Datenschutz & Sicherheit → „Trotzdem öffnen"*

#### Windows 11

1. Repository herunterladen oder klonen (als ZIP oder per `git clone`)
2. **Doppelklick** auf `WhatsappViewerStart.bat`
   > Falls Windows SmartScreen warnt: „Weitere Informationen" → „Trotzdem ausführen"  
   > Das Skript enthält keinen schädlichen Code — der Quellcode ist vollständig einsehbar.

---

#### Ablauf (gleich auf beiden Systemen)

Im sich öffnenden Fenster den 4 Schritten folgen:

**Schritt 1 — Chat-Datei:**
- Wurde `input_txt/` noch nicht befüllt: `_chat.txt` per **Drag & Drop** ins Fenster ziehen → Enter
- Die Datei wird automatisch nach `input_txt/` kopiert und beim nächsten Start automatisch erkannt

**Schritt 2 — Medienordner:**
- Wurden die Medien bereits nach `input_media/` kopiert (siehe Vorbereitung): automatisch erkannt
- Alternativ: den Backup-Ordner per **Drag & Drop** ins Fenster ziehen → Enter → alle Dateien werden kopiert

**Schritt 3 — Absender wählen:**
- Die erkannten Namen aus dem Chat werden angezeigt
- Nummer des eigenen Namens eingeben → Enter

**Schritt 4 — Ausgabemodus wählen:**
```
  [1] Eingebettet  – alle Medien direkt in die HTML (eine einzige Datei)
       → komplett portabel, kein Ordner nötig, ideal als Backup
       → geschätzte Dateigröße: ~85 MB
  [2] Relativ      – HTML verweist auf input_media/ (Ordner muss erhalten bleiben)
```
- **Option 1 (empfohlen für Backup):** Alle Medien werden als Base64 eingebettet. Die fertige Datei ist vollständig selbstständig — ideal zum Archivieren oder Weitergeben.
- **Option 2:** Schneller, kleinere Datei — aber Projektordner muss zusammenbleiben.

> **Hinweis zu eingebetteten Videos:** Sehr große Einzelvideos (>50 MB) können im Browser träge sein, da kein Streaming möglich ist — das ist eine Browser-Limitierung.

Die fertige `chat.html` öffnet sich automatisch im Standardbrowser.

---

### Variante B — Kommandozeile

**macOS:**
```bash
python3 main.py \
  --chat   /Pfad/zur/_chat.txt \
  --media  /Pfad/zum/Medienordner \
  --me     "Dein Name im Chat" \
  --output ausgabe/chat.html \
  --embed
```

**Windows:**
```cmd
python main.py ^
  --chat   C:\Pfad\zur\_chat.txt ^
  --media  C:\Pfad\zum\Medienordner ^
  --me     "Dein Name im Chat" ^
  --output ausgabe\chat.html ^
  --embed
```

| Parameter  | Beschreibung                                              | Standard              |
|------------|-----------------------------------------------------------|-----------------------|
| `--chat`   | Pfad zur `_chat.txt`                                      | `input_txt/_chat.txt` |
| `--media`  | Pfad zum Ordner mit den Mediendateien                     | `input_media/`        |
| `--me`     | Dein Name, wie er im Chat steht                           | –                     |
| `--output` | Ausgabedatei                                              | `output/chat.html`    |
| `--embed`  | Alle Medien als Base64 in die HTML einbetten (eine Datei) | aus                   |

---

## Projektstruktur

```
whatsapp-viewer/
├── main.py                      # CLI-Einstiegspunkt (macOS + Windows)
├── interactive.py               # Interaktiver Starter (macOS + Windows)
├── parse_chat.py                # WhatsApp .txt Parser
├── generate_html.py             # HTML/CSS Generator
├── WhatsappViewerStart.command  # Doppelklick-Launcher macOS
├── WhatsappViewerStart.bat      # Doppelklick-Launcher Windows
│
├── input_txt/                   # ← _chat.txt hier ablegen
│   └── _chat.txt
├── input_media/                 # ← alle Mediendateien hier ablegen
│   ├── 00000001-PHOTO-2024-01-01.jpg
│   └── ...
└── output/                      # ← fertige HTML erscheint hier
    └── chat.html
```

> Die Ordner `input_txt/`, `input_media/` und `output/` werden beim ersten Start **automatisch angelegt**.

> **Modus Relativ:** Die fertige `chat.html` referenziert alle Medien mit relativen Pfaden — der gesamte Projektordner kann kopiert, verschoben oder weitergegeben werden.

> **Modus Eingebettet (`--embed`):** Alle Medien sind als Base64 direkt in der HTML gespeichert — eine einzige Datei genügt als vollständiges Backup.

---

## Unterstützte Medienformate

| Typ    | Formate                       | Eingebettet                         |
|--------|-------------------------------|-------------------------------------|
| Bild   | JPG, JPEG, PNG, GIF, WebP     | ✓ Vollständig                       |
| Video  | MP4, MOV, AVI, MKV            | ✓ (kein Seeking bei großen Dateien) |
| Audio  | MP3, OGG, Opus, M4A, AAC      | ✓ Vollständig                       |
| Datei  | PDF, DOCX                     | ✓ Als Download-Link                 |

---

## Datenschutz

Alle Daten bleiben **lokal auf deinem Computer**. Es werden keine Daten übertragen, keine externen Bibliotheken geladen und keine Verbindungen ins Internet aufgebaut.

---

## Lizenz

MIT — frei verwendbar, veränderbar und weitergegeben werden darf.

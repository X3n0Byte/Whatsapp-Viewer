# WhatsApp Chat Viewer

Konvertiert exportierte WhatsApp-Chats (`.txt` + Medien) in eine übersichtliche, offline-fähige HTML-Datei — direkt im Browser, ohne Installation, ohne Internetverbindung.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) ![macOS](https://img.shields.io/badge/macOS-Monterey%2B-black?logo=apple) ![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)

---

## Features

- **WhatsApp-Design** — grüne Blasen rechts (du), weiße Blasen links (andere)
- **Medienvorschau** — Bilder, Videos und Audios direkt im Browser
- **Bildergalerie** — Klick auf ein Bild öffnet es in einem Lightbox-Overlay
- **Sticky Datums-Trenner** — automatische Tagesgruppen beim Scrollen
- **Interaktiver Starter** — kein Terminal-Wissen nötig, Drag & Drop
- **Portabel** — alle Medien werden ins Projekt kopiert, relative Pfade in der HTML
- **Offline & privat** — keine externen Server, keine Abhängigkeiten außer Python
- **Beide Exportformate** — `[DD.MM.YY, HH:MM:SS]` und `DD.MM.YY, HH:MM -`

---

## Voraussetzungen

- **macOS** (Monterey oder neuer empfohlen)
- **Python 3.9+** — prüfen mit:
  ```bash
  python3 --version
  ```
  Falls nicht vorhanden: [python.org/downloads](https://www.python.org/downloads/)

---

## Chat exportieren (WhatsApp)

1. WhatsApp öffnen → Chat antippen
2. Oben rechts **⋮ → Mehr → Chat exportieren**
3. **„Medien einschließen"** wählen
4. Datei auf den Mac übertragen (AirDrop, iCloud, etc.)
5. ZIP entpacken → enthält `_chat.txt` und alle Mediendateien

---

## Verwendung

### Variante A — Interaktiver Starter (empfohlen)

#### Vorbereitung (Best Practice)

Damit alle Bilder, Videos und Audios in der HTML korrekt angezeigt werden, sollten die Medien **vor dem Start** in den Projektordner kopiert werden:

1. Das WhatsApp-Backup-ZIP entpacken → ein Ordner mit `_chat.txt` und allen Mediendateien entsteht
2. Den Ordner `input_media/` im Projektverzeichnis öffnen — er ist zunächst **leer**
3. **Alle Mediendateien** aus dem entpackten Backup in `input_media/` kopieren
   > Tipp: Alle Dateien im Backup-Ordner auswählen (außer `_chat.txt`) und in `input_media/` ziehen

So liegt beim Start alles bereit und der Viewer erkennt die Medien automatisch — kein manuelles Ziehen im Terminal nötig.

---

#### Starten

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

4. Im sich öffnenden Terminalfenster den 3 Schritten folgen:

   **Schritt 1 — Chat-Datei:**
   - Wurde `input_txt/` noch nicht befüllt: `_chat.txt` per **Drag & Drop** ins Terminalfenster ziehen → Enter
   - Die Datei wird automatisch nach `input_txt/` kopiert
   - Beim nächsten Start wird sie dort automatisch erkannt

   **Schritt 2 — Medienordner:**
   - Wurden die Medien bereits nach `input_media/` kopiert (siehe Vorbereitung): automatisch erkannt, kein Eingriff nötig
   - Alternativ: den Backup-Ordner mit allen Medien per **Drag & Drop** ins Terminalfenster ziehen → Enter
   - Alle Mediendateien werden automatisch nach `input_media/` kopiert

   **Schritt 3 — Absender wählen:**
   - Die Namen aus dem Chat werden angezeigt
   - Nummer des eigenen Namens eingeben → Enter

5. Die fertige `chat.html` öffnet sich automatisch im Browser

---

### Variante B — Kommandozeile

```bash
python3 main.py \
  --chat  /Pfad/zur/_chat.txt \
  --media /Pfad/zum/Medienordner \
  --me    "Dein Name im Chat" \
  --output ausgabe/chat.html
```

| Parameter  | Beschreibung                                        | Standard            |
|------------|-----------------------------------------------------|---------------------|
| `--chat`   | Pfad zur `_chat.txt`                                | `input_txt/_chat.txt` |
| `--media`  | Pfad zum Ordner mit den Mediendateien               | `input_media/`      |
| `--me`     | Dein Name, wie er im Chat steht                     | –                   |
| `--output` | Ausgabedatei                                        | `output/chat.html`  |

---

## Projektstruktur

```
whatsapp-viewer/
├── main.py                          # CLI-Einstiegspunkt
├── interactive.py                   # Interaktiver Starter
├── parse_chat.py                    # WhatsApp .txt Parser
├── generate_html.py                 # HTML/CSS Generator
├── WhatsappViewerStart.command  # Doppelklick-Launcher (macOS)
│
├── input_txt/                       # ← _chat.txt hier ablegen
│   └── _chat.txt
├── input_media/                     # ← alle Mediendateien hier ablegen
│   ├── 00000001-PHOTO-2024-01-01.jpg
│   └── ...
└── output/                          # ← fertige HTML erscheint hier
    └── chat.html
```

> Die Ordner `input_txt/`, `input_media/` und `output/` werden beim ersten Start **automatisch angelegt**.

> Die fertige `chat.html` referenziert alle Medien mit **relativen Pfaden** — der gesamte Projektordner kann kopiert, verschoben oder weitergegeben werden und bleibt vollständig funktionsfähig.

---

## Unterstützte Medienformate

| Typ    | Formate                          |
|--------|----------------------------------|
| Bild   | JPG, JPEG, PNG, GIF, WebP        |
| Video  | MP4, MOV, AVI, MKV               |
| Audio  | MP3, OGG, Opus, M4A, AAC         |
| Datei  | PDF, DOCX (als Download-Link)    |

---

## Datenschutz

Alle Daten bleiben **lokal auf deinem Mac**. Es werden keine Daten übertragen, keine externen Bibliotheken geladen und keine Verbindungen ins Internet aufgebaut.

---

## Lizenz

MIT — frei verwendbar, veränderbar und weitergegeben werden darf.

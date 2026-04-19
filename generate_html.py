import os
import html as _html
from datetime import datetime

_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: #111b21;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.chat-wrapper {
  width: 100%;
  max-width: 900px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #e5ddd5;
}
.chat-header {
  background: #075e54;
  color: #fff;
  padding: 14px 18px;
  font-size: 17px;
  font-weight: 600;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 10;
}
.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px 20px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect width='400' height='400' fill='%23e5ddd5'/%3E%3C/svg%3E");
}
.date-divider {
  display: flex;
  justify-content: center;
  margin: 12px 0 8px;
  position: sticky;
  top: 8px;
  z-index: 5;
}
.date-divider span {
  background: #fff;
  color: #667781;
  font-size: 12.5px;
  padding: 5px 12px;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
}
.system-msg {
  display: flex;
  justify-content: center;
  margin: 4px 0;
}
.system-msg span {
  background: rgba(255,255,255,0.75);
  color: #667781;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 8px;
}
.msg-row {
  display: flex;
  margin: 2px 0;
}
.msg-row.me { justify-content: flex-end; }
.msg-row.other { justify-content: flex-start; }
.bubble {
  max-width: 70%;
  min-width: 80px;
  padding: 6px 8px 4px 9px;
  border-radius: 8px;
  position: relative;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0,0,0,0.13);
}
.msg-row.me .bubble {
  background: #d9fdd3;
  border-top-right-radius: 2px;
}
.msg-row.other .bubble {
  background: #fff;
  border-top-left-radius: 2px;
}
.sender-name {
  font-size: 12.5px;
  font-weight: 600;
  color: #00a884;
  margin-bottom: 2px;
}
.msg-text {
  font-size: 14.2px;
  color: #111b21;
  white-space: pre-wrap;
  line-height: 1.45;
}
.msg-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 3px;
  gap: 4px;
}
.msg-time {
  font-size: 11px;
  color: #667781;
}
.media-wrap { margin: 2px 0 4px; }
.media-wrap img {
  max-width: 100%;
  max-height: 320px;
  border-radius: 6px;
  cursor: zoom-in;
  display: block;
}
.media-wrap video {
  max-width: 100%;
  max-height: 320px;
  border-radius: 6px;
  display: block;
}
.media-wrap audio {
  width: 280px;
  max-width: 100%;
}
.media-wrap .doc-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: #f0f2f5;
  border-radius: 6px;
  color: #111b21;
  text-decoration: none;
  font-size: 13px;
}
.media-omitted {
  color: #8696a0;
  font-style: italic;
  font-size: 13px;
}
.lightbox {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.88);
  z-index: 1000;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
}
.lightbox img {
  max-width: 95vw;
  max-height: 95vh;
  border-radius: 4px;
  object-fit: contain;
}
"""

_JS = """
function openImg(el) {
  var lb = document.getElementById('lightbox');
  document.getElementById('lb-img').src = el.src;
  lb.style.display = 'flex';
}
function closeLightbox() {
  document.getElementById('lightbox').style.display = 'none';
}
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeLightbox();
});
// Scroll to bottom on load
window.addEventListener('load', function() {
  var body = document.querySelector('.chat-body');
  if (body) body.scrollTop = body.scrollHeight;
});
"""


def _fmt_time(ts):
    return ts.strftime('%H:%M') if ts else ''


def _fmt_date(ts):
    if not ts:
        return ''
    DAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    today = datetime.now().date()
    d = ts.date()
    diff = (today - d).days
    if diff == 0:
        return 'Heute'
    if diff == 1:
        return 'Gestern'
    return ts.strftime('%d.%m.%Y')


def _media_tag(media, media_dir, output_path):
    if media is None:
        return ''
    if media['type'] == 'omitted':
        return '<div class="media-wrap"><span class="media-omitted">🔒 Medien weggelassen</span></div>'
    filename = media['filename']
    filepath = os.path.join(media_dir, filename) if media_dir and filename else None
    if not filepath or not os.path.exists(filepath):
        return f'<div class="media-wrap"><span class="media-omitted">📎 {_html.escape(filename or "")}</span></div>'
    # Relativer Pfad von der HTML-Datei zur Mediendatei → portabel
    rel_path = os.path.relpath(filepath, start=os.path.dirname(os.path.abspath(output_path)))
    ext = os.path.splitext(filename)[1].lower()
    escaped_path = _html.escape(rel_path)
    escaped_name = _html.escape(filename)
    if ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return f'<div class="media-wrap"><img src="{escaped_path}" alt="{escaped_name}" loading="lazy" onclick="openImg(this)"></div>'
    if ext in ('.mp4', '.mov', '.avi', '.mkv'):
        return f'<div class="media-wrap"><video controls preload="metadata"><source src="{escaped_path}">{escaped_name}</video></div>'
    if ext in ('.mp3', '.ogg', '.opus', '.m4a', '.aac'):
        return (
            f'<div class="media-wrap">'
            f'<div style="font-size:12px;color:#667781;margin-bottom:3px">🎵 {escaped_name}</div>'
            f'<audio controls preload="none"><source src="{escaped_path}">{escaped_name}</audio>'
            f'</div>'
        )
    return (
        f'<div class="media-wrap">'
        f'<a class="doc-link" href="{escaped_path}">📄 {escaped_name}</a>'
        f'</div>'
    )


def generate_html(messages, me, media_dir, output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    parts = []
    current_date_label = None

    for msg in messages:
        ts = msg['timestamp']
        date_label = _fmt_date(ts)

        if date_label != current_date_label:
            current_date_label = date_label
            if date_label:
                parts.append(
                    f'<div class="date-divider"><span>{_html.escape(date_label)}</span></div>'
                )

        if msg['is_system']:
            parts.append(
                f'<div class="system-msg"><span>{_html.escape(msg["message"])}</span></div>'
            )
            continue

        is_me = msg['sender'] == me
        side = 'me' if is_me else 'other'
        media = msg.get('media')
        media_tag = _media_tag(media, media_dir, output_path)

        # Don't show raw filename as text when it's a media reference
        if media and media['type'] in ('file', 'omitted'):
            text_tag = ''
        else:
            escaped_text = _html.escape(msg['message']).replace('\n', '<br>')
            text_tag = f'<div class="msg-text">{escaped_text}</div>'

        sender_tag = (
            '' if is_me
            else f'<div class="sender-name">{_html.escape(msg["sender"] or "")}</div>'
        )
        time_tag = f'<div class="msg-footer"><span class="msg-time">{_fmt_time(ts)}</span></div>'

        parts.append(
            f'<div class="msg-row {side}">'
            f'<div class="bubble">'
            f'{sender_tag}{media_tag}{text_tag}{time_tag}'
            f'</div></div>'
        )

    body = '\n'.join(parts)

    page = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WhatsApp Chat</title>
<style>{_CSS}</style>
</head>
<body>
<div class="chat-wrapper">
  <div class="chat-header">WhatsApp Chat</div>
  <div class="chat-body">
{body}
  </div>
</div>
<div id="lightbox" class="lightbox" onclick="closeLightbox()">
  <img id="lb-img" src="" alt="">
</div>
<script>{_JS}</script>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(page)

    print(f'✓ HTML gespeichert: {output_path}')
    print(f'  {len(messages)} Nachrichten verarbeitet.')

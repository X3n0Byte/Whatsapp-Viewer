import re
from datetime import datetime

# Format 1: [DD.MM.YY, HH:MM:SS] Sender: Message
_RE_FMT1_MSG = re.compile(
    r'^\[(\d{1,2}\.\d{1,2}\.\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?)\] ([^:]+): (.+)$'
)
_RE_FMT1_SYS = re.compile(
    r'^\[(\d{1,2}\.\d{1,2}\.\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?)\] (.+)$'
)
# Format 2: DD.MM.YY, HH:MM - Sender: Message (both regular hyphen and en-dash)
_RE_FMT2_MSG = re.compile(
    r'^(\d{1,2}\.\d{1,2}\.\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?) [–-] ([^:]+): (.+)$'
)
_RE_FMT2_SYS = re.compile(
    r'^(\d{1,2}\.\d{1,2}\.\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?) [–-] (.+)$'
)

_MEDIA_OMITTED = {'<Medien weggelassen>', '<Media omitted>'}
_MEDIA_ANHANG = re.compile(r'^<Anhang:\s*(.+)>$')  # German: <Anhang: filename.jpg>
_MEDIA_EXT = re.compile(
    r'^(.+\.(jpg|jpeg|png|gif|webp|mp4|mov|avi|mkv|mp3|ogg|opus|m4a|aac|pdf|docx?))\s*(?:\([^)]*\))?$',
    re.IGNORECASE,
)
_LTR_MARK = '\u200e'


def _parse_ts(date_str, time_str):
    combined = f'{date_str} {time_str}'
    for fmt in ('%d.%m.%y %H:%M:%S', '%d.%m.%Y %H:%M:%S', '%d.%m.%y %H:%M', '%d.%m.%Y %H:%M'):
        try:
            return datetime.strptime(combined, fmt)
        except ValueError:
            pass
    return None


def _detect_media(message):
    clean = message.strip().lstrip(_LTR_MARK)
    if clean in _MEDIA_OMITTED:
        return {'type': 'omitted', 'filename': None}
    m = _MEDIA_ANHANG.match(clean)
    if m:
        return {'type': 'file', 'filename': m.group(1).strip()}
    m = _MEDIA_EXT.match(clean)
    if m:
        return {'type': 'file', 'filename': m.group(1).strip()}
    return None


def _try_parse_line(line):
    line = line.lstrip(_LTR_MARK)
    for pattern, has_sender in (
        (_RE_FMT1_MSG, True),
        (_RE_FMT1_SYS, False),
        (_RE_FMT2_MSG, True),
        (_RE_FMT2_SYS, False),
    ):
        m = pattern.match(line)
        if not m:
            continue
        g = m.groups()
        ts = _parse_ts(g[0], g[1])
        if has_sender:
            return ts, g[2].strip(), g[3], False
        return ts, None, g[2], True
    return None


def parse_chat(filepath):
    messages = []
    current = None

    with open(filepath, encoding='utf-8-sig') as f:
        lines = f.readlines()

    for raw in lines:
        line = raw.rstrip('\n\r')
        result = _try_parse_line(line)
        if result:
            if current:
                messages.append(current)
            ts, sender, message, is_system = result
            media = None if is_system else _detect_media(message)
            current = {
                'timestamp': ts,
                'sender': sender,
                'message': message,
                'media': media,
                'is_system': is_system,
            }
        elif current is not None:
            current['message'] += '\n' + line

    if current:
        messages.append(current)

    return messages

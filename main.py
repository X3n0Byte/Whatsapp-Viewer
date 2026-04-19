import argparse
import sys
import os

from parse_chat import parse_chat
from generate_html import generate_html

_BASE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_CHAT   = os.path.join(_BASE, 'input_txt', '_chat.txt')
_DEFAULT_MEDIA  = os.path.join(_BASE, 'input_media')
_DEFAULT_OUTPUT = os.path.join(_BASE, 'output', 'chat.html')


def main():
    parser = argparse.ArgumentParser(
        description='WhatsApp Chat Viewer – konvertiert einen .txt Export in eine HTML-Datei.'
    )
    parser.add_argument('--chat',   default=_DEFAULT_CHAT,   help=f'Pfad zur _chat.txt (Standard: input_txt/_chat.txt)')
    parser.add_argument('--media',  default=_DEFAULT_MEDIA,  help=f'Pfad zum Medienordner (Standard: input_media/)')
    parser.add_argument('--output', default=_DEFAULT_OUTPUT,  help=f'Ausgabedatei (Standard: output/chat.html)')
    parser.add_argument('--me', default='', help='Dein Name im Chat (für rechte Blasen)')
    parser.add_argument('--embed', action='store_true', help='Alle Medien als Base64 in die HTML einbetten (eine einzige portable Datei)')
    args = parser.parse_args()

    if not os.path.isfile(args.chat):
        print(f'Fehler: Chat-Datei nicht gefunden: {args.chat}', file=sys.stderr)
        sys.exit(1)

    if args.media and not os.path.isdir(args.media):
        print(f'Warnung: Medienordner nicht gefunden: {args.media}', file=sys.stderr)
        args.media = None

    print(f'Lese Chat: {args.chat}')
    messages = parse_chat(args.chat)
    print(f'→ {len(messages)} Nachrichten gefunden.')

    generate_html(
        messages=messages,
        me=args.me,
        media_dir=args.media,
        output_path=args.output,
        embed=args.embed,
    )


if __name__ == '__main__':
    main()

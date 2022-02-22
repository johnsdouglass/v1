#!/usr/bin/env python3

# Exports JIRA ticket hyperlinks to clipboard based.

import sys
import argparse
from jaraco import clipboard


# Gets ID numbers from the clipboard, splitting on whitespace.
# Returns empty list if none.
def get_clipboard_ids():
    c = None
    try:
        c = clipboard.paste()
    except:
        # Don't care if nothing's there
        pass
    return [] if c is None else c.split()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Exports JIRA links to clipboard.',
        epilog='If no JIRA IDs are specified, you will be prompted for them.')
    parser.add_argument('id_numbers', metavar='number', type=str, nargs='*',
                        help='One or more JIRA IDs. For example: "ATLAS-1234 ATHENA-1234".')
    parser.add_argument('--endpoint', default='https://infoblox.atlassian.net/browse',
                        help='JIRA endpoint')
    parser.add_argument('--from-clipboard', action='store_true',
                        help='Specify to read IDs from clipboard')
    args = parser.parse_args()
    headers = {}

    if args.from_clipboard:
        id_numbers = get_clipboard_ids()
    elif len(args.id_numbers) > 0:
        id_numbers = args.id_numbers
    else:
        id_numbers = input('Enter one or more id numbers separated by whitespace: ').split()

    print (id_numbers)

    if len(id_numbers) == 0:
        print('No id numbers specified.')
        parser.print_help()
        sys.exit(1)

    html = '<table>'

    for id in id_numbers:
        html += '<tr>'
        html += '<td>' + '<a href="{}/{}">{}</a>'.format(args.endpoint, id, id) + '</td>'
        html += '</tr>\n'

    html += '</table>'

    print (html)

    clipboard.copy_html(html)

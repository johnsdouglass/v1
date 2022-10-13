#!/usr/bin/env python3

# Exports hyperlinks to clipboard based on format string.
# Examples:
# S3:
#   --format-string "https://s3.console.aws.amazon.com/s3/buckets/{}"
# EC2:
#   --format-string "https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#InstanceDetails:instanceId={}"
# Github:
#   --format-string "https://github.com/[repo]/{}"

import sys
import argparse
from jaraco import clipboard


# Gets items from the clipboard, splitting on lines.
# Returns empty list if none.
def get_clipboard_items():
    c = None
    try:
        c = clipboard.paste()
    except:
        # Don't care if nothing's there
        pass
    return [] if c is None else c.splitlines()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Exports links to clipboard.',
        epilog='If no items are specified, you will be prompted for them.')
    parser.add_argument('items', type=str, nargs='*',
                        help='One or more items to use to build the hyperlink; can be tab separated')
    parser.add_argument('--id-column', type=int, default=0,
                        help='0-based number of column to be treated as ID (link text) for hyperlink')
    parser.add_argument('--format-string', required=True,
                        help='Format string with {}, {0}, etc. at place to substitute item')
    parser.add_argument('--from-clipboard', action='store_true',
                        help='Specify to read IDs from clipboard')
    parser.add_argument('--ignore-header', action='store_true',
                        help='Specify if first item is header; it will be ignored')
    args, _ = parser.parse_known_args()

    if args.from_clipboard:
        items = get_clipboard_items()
    elif len(args.items) > 0:
        items = args.items
    else:
        print('Enter one or more items separated by newlines, followed by Ctrl-D: ', end='')
        items = sys.stdin.read().splitlines()

    print(items)

    if len(items) == 0:
        print('No items specified.')
        parser.print_help()
        sys.exit(1)

    html = '<table>'

    if args.ignore_header and len(items) > 0:
        items.pop(0)

    for item in items:
        html += '<tr>'
        html += '<td>'
        if len(item) > 0:
            item_array = item.split('\t')
            url = args.format_string.format(*item_array)
            html += '<a href="{0}">{1}</a>'.format(url, item_array[args.id_column])
        html += '</td>'
        html += '</tr>\n'

    html += '</table>'

    print(html)

    # exit(0)

    clipboard.copy_html(html)

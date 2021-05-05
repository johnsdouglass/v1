#!/usr/bin/env python3

import sys
import os
import argparse
import requests
from jaraco import clipboard


# This script supports the following asset types/prefixes:
# Type          Prefix
# ------------- ------
# Epic            E-
# Story           B-
# Defect          D-
# Goal            G-
# Issue           I-
# Milestone       M-
# Request         R-
# StrategicTheme  ST-
# Task            TK-
# Test            AT-
# Theme           FG-
# Topic           T-
prefix_asset_type = {
    'E-': 'Epic',
    'B-': 'Story',
    'D-': 'Defect',
    'G-': 'Goal',
    'I-': 'Issue',
    'M-': 'Milestone',
    'R-': 'Request',
    'ST-': 'StrategicTheme',
    'TK-': 'Task',
    'AT-': 'Test',
    'FG-': 'Theme',
    'T-': 'Topic',
}


# Returns asset type of the specified asset number (e.g., E-12345 refers to an Epic)
def get_asset_type(number: str):
    for prefix, asset_type in prefix_asset_type.items():
        if number.startswith(prefix):
            return asset_type
    sys.exit("Can't determine asset type of number " + number + ". Supported prefixes are: " +
             ", ".join(prefix_asset_type.keys()) + ".")


# Class representing an asset, including the type, number, object ID, and name
class AssetInfo(object):
    def __init__(self, number: str, oid: str = None, name: str = None):
        self.asset_type = get_asset_type(number)
        self.number = number
        self.oid = oid
        # Sometimes the name has control characters in it
        self.name = name.replace('\t', ' ').replace('\n', '')

    # Returns a formatted HTML hyperlink (<a> element) for this asset.
    # If there is no object id, we assume it's not a valid asset,
    # so just return the number.
    def get_link(self):
        if self.oid is None:
            return self.number
        else:
            return '<a href="{}/{}.mvc/Summary?oidToken={}">{}</a>'.format(
                args.endpoint, self.asset_type, self.oid, self.number)

    # Returns the name of this asset, or empty string if none
    def get_name(self):
        return '' if self.name is None else self.name


# Calls V1 to get the asset information for the specified number.
def get_asset_info(number: str):
    asset_type = get_asset_type(number)
    q = '{{ "from": "{}", "select": [ "Number", "Name" ], "where": {{ "Number": "{}" }} }}'.\
        format(asset_type, number)
    url = args.endpoint + '/query.v1'
    req = requests.post(url, data=q, headers=headers)
    response = req.json()[0]
    if len(response) > 0:
        item = response[0]
        return AssetInfo(item['Number'], item['_oid'], item['Name'])
    else:
        return AssetInfo(number=number)


# Gets asset numbers from the clipboard, splitting on whitespace.
# Returns empty list if none.
def get_clipboard_assets():
    c = None
    try:
        c = clipboard.paste()
    except:
        # Don't care if nothing's there
        pass
    return [] if c is None else c.split()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Exports VersionOne links to clipboard.',
        epilog='If no asset numbers are specified, this script will attempt to pull them from the clipboard.')
    parser.add_argument('asset_numbers', metavar='number', type=str, nargs='*',
                        help='One or more asset numbers. For example: "E-12345 B-22222". The following ' +
                             'asset types are supported: ' + ', '.join(prefix_asset_type.values()))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'),
                        help='V1 endpoint or specify VERSION_ONE_ENDPOINT environment variable')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'),
                        help='V1 access token or specify VERSION_ONE_TOKEN environment variable')
    parser.add_argument('--include-name', action='store_true',
                        help='Specify to include asset names')
    args = parser.parse_args()
    headers = {}

    if args.endpoint is None:
        sys.exit('No endpoint was found. Specify --endpoint or set VERSION_ONE_ENDPOINT.')

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    asset_numbers = get_clipboard_assets() if len(args.asset_numbers) == 0 else args.asset_numbers
    if len(asset_numbers) == 0:
        sys.exit('No asset numbers specified. Specify on command line or copy to clipboard.')

    assets = []
    for asset_number in asset_numbers:
        assets.append(get_asset_info(asset_number))

    html = '<table>'

    for asset in assets:
        html += '<tr>'
        html += '<td>' + asset.get_link() + '</td>'
        if args.include_name:
            html += '<td>' + asset.get_name() + '</td>'
        html += '</tr>'

    html += '</table>'

    clipboard.copy_html(html)

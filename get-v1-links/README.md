# Export VersionOne (V1) links to clipboard

Copies V1 asset links to the clipboard, optionally with names.

Links are copied to the clipboard as an HTML table, suitable for pasting
into Microsoft Office or Google Docs or other HTML-aware applications.

The HTML looks like this:

```html
<table>
<tr><td><a href="[V1 endpoint]/Epic.mvc/Summary?oidToken=Epic:111111">E-12345</a></td></tr>
<tr><td><a href="[V1 endpoint]/Story.mvc/Summary?oidToken=Story:222222">B-54321</a></td></tr>
</table>
```

If `--include-name` is specified, the asset name(s) are included as a second cell
in each row.

This script supports the following asset types/prefixes:

|Asset Type|Prefix|
|---|---|
|Epic|E-|
|Story|B-|
|Defect|D-|
|Goal|G-|
|Issue|I-|
|Milestone|M-|
|Request|R-|
|StrategicTheme|ST-|
|Task|TK-|
|Test|AT-|
|Theme|FG-|
|Topic|T-|

## Installation

This script requires Python 3 and the following packages:
* sys
* os
* argparse
* requests
* jaraco.clipboard

## Usage

```
get_v1_links.py [--endpoint ENDPOINT] [--token TOKEN] [--include-name] [--from-clipboard] [number ...]
```

You may specify asset numbers on the command line,
in the clipboard with the `--include-clipboard` parameter, or if none are included,
the script will prompt you for them.

Other arguments are:
* `--endpoint`: V1 endpoint, i.e., `https://[host]/[path]`.
Can also be specified with the `VERSION_ONE_ENDPOINT` environment variable.
* `--token`: V1 access token. Can also be specified with the `VERSION_ONE_TOKEN` 
environment variable.
* `--include-name`: Include the name of each asset.
* `--from-clipboard`: Read asset numbers from clipboard.

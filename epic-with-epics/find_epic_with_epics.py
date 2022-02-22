#!/usr/bin/env python3

# Gets list of parent items for V1 Epics

import sys
import os
import json
import argparse
import requests


def get_item(number: str):
    q = '{{ "from": "Epic", "select": [ "Scope.Name", "Number", "Name", "Category.Name" ], "where": {{ "Number": "{}" }} }}'. \
        format(number)
    url = args.endpoint + '/query.v1'
    req = requests.post(url, data=q, headers=headers)
    response = req.json()[0]
    if len(response) > 0:
        return response[0]
    else:
        return None


def get_epics(debug=False):
    q = """
{
  "from": "Epic",
  "select": [
    "Scope.Name",
    "Name",
    "Category.Name",
    "AssetState",
    "Status.Name",
    "Number",
    "Super.Number",
  ],
  "where": {
  #"Number": "E-11515"
    #"Scope.Name": "Portunus 5.X",
    #"Custom_TSAStatus2.Name": "%s",
    "Category.Name": "Epic",
  }
}
"""
    url = args.endpoint + '/query.v1'
    req = requests.post(url, data=q, headers=headers)
    response = req.json()[0]
    print("Number", "Name", "Project", "Asset State", "Status", "Parent Number", "Parent Name", "Parent Project", sep="\t")
    for i in range(len(response)):
        epic = response[i]
        if debug:
            print(json.dumps(epic, indent=1))
        project = epic["Scope.Name"]
        if project.endswith(" Backlog") or project.endswith(" Archive"):
            continue
        super_number = epic["Super.Number"]
        if super_number is not None:
            super_item = get_item(super_number)
            if super_item is not None and super_item["Category.Name"] == "Epic":
                print(epic["Number"], epic["Name"], epic["Scope.Name"], epic["AssetState"], epic["Status.Name"],
                      super_item["Number"], super_item["Name"], super_item["Scope.Name"], sep="\t")


# Number, Name, Project, Super Number, Super Name, Super Project


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'),
                        help='V1 endpoint or specify VERSION_ONE_ENDPOINT environment variable')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'),
                        help='V1 access token or specify VERSION_ONE_TOKEN environment variable')
    args = parser.parse_args()
    headers = {}

    if args.endpoint is None:
        sys.exit('No endpoint was found. Specify --endpoint or set VERSION_ONE_ENDPOINT.')

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    get_epics(False)

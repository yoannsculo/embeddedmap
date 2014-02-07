#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from pprint import pprint

# https://github.com/yoannsculo/emploi/blob/master/societes/france.json

fp_template_js = open('js/template.js', 'r')
fp_template_index = open('template.html', 'r')

fp_map = open('js/map.js', 'w')
fp_index = open('index.html', 'w+')

template_js = fp_template_js.read()
template_index = fp_template_index.read()

with open('france.json') as data_file:
    data = json.load(data_file)

result = u"".encode('utf-8')
list = u"".encode('utf-8')
entries = 0

for entry in data["companies"]:
    name = ""
    url = ""

    if 'name' in entry:
        name = entry["name"]
    if 'url' in entry:
        url = entry["url"]
    if 'description' in entry:
        description_full = entry['description']

    if 'locations' not in entry:
        continue

    for location in entry['locations']:
        if len(location['gps_coordinates']) == 0:
            continue

        lat = location['gps_coordinates'].split('/')[0]
        lon = location['gps_coordinates'].split('/')[1]

        name_full = name

        if 'name' in location:
            if len(location['name']) != 0:
                name_full = ur'%s' %(location['name'])

        popup_content = ur'<b><a target=\\"_blank\\" href=\\"%s\\">%s</a></b>' % (url, name_full)

        if 'description' in location:
            description_full = location['description']

        if len(description_full) > 0:
            popup_content += ur' - %s' % (description_full)

        result += (u'L.marker([%s,%s]).addTo(map)' % (lat, lon)).encode('utf-8')
        result += (u'    .bindPopup("%s").openPopup();' % (popup_content)).encode('utf-8')

        list += (u'<li><strong><a target="_blank" href="%s">%s</a></strong> - %s</li>' % (url, name_full, description_full)).encode('utf-8')
        entries += 1

map_content = re.sub('{{content}}', result, template_js)
index_content = re.sub('{{list}}', list, template_index)
index_content = re.sub('{{entries}}', str(entries), index_content)
fp_map.write(map_content)
fp_index.write(index_content)

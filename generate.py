#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import argparse
from pprint import pprint

# https://github.com/yoannsculo/emploi/blob/master/societes/france.json

fp_template_js = open('js/template.js', 'r')
fp_template_index = open('template.html', 'r')

fp_map = open('js/map.js', 'w')
fp_index = open('index.html', 'w+')

template_js = fp_template_js.read()
template_index = fp_template_index.read()

postal_fr_re = re.compile(r".*([0-9]{5}.*)")
postal_be_re = re.compile(r".*([B-]?[0-9]{4}.*)")

postal_res = [postal_fr_re, postal_be_re]

result = u"".encode('utf-8')
list = u"".encode('utf-8')
companies_nb=0
locations_nb=0

DEFAULT_FILE='france.json'

parser = argparse.ArgumentParser(description='Create embedded company map.')
parser.add_argument('files', metavar='file', type=str, nargs='*',
                    default="france.json",
                    help='A JSON file containing company information (default : france.json)')

args = parser.parse_args()
if type(args.files) == str:
    files = [args.files]
else:
    files = args.files

for f in files:
    with open(f) as data_file:
        data = json.load(data_file)

    country_name = data["country"]["name"]
    country_code = data["country"]["iso"]

    print "==> Parsing %s (%s) %s" % (country_name, country_code, f)

    list += (u"<strong>%s</strong><br/>" % (country_name)).encode('utf-8')

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

        locations = 0

        list += (u'<li class="%s"><strong><a target="_blank" href="%s">%s</a></strong>' % (country_code, url, name)).encode('utf-8')
        if 'description' in entry:
            list += (u' - %s</li>' % (description_full)).encode('utf-8')
        else:
            list += u'</li>'.encode('utf-8')

        list += ur'<ul>'.encode('utf-8')

        for location in entry['locations']:
            if len(location['gps_coordinates']) == 0:
                continue

            short_postal_address = full_postal_address = location['postal_address']
            if len(full_postal_address) == 0:
                short_postal_address = full_postal_address = "Postal address not available"
            else:
                for r in postal_res:
                    postal_re_result = r.match(full_postal_address)
                    if not postal_re_result is None:
                        short_postal_address = postal_re_result.group(1)
                        break

            locations += 1

            lat= re.split('/|,',location['gps_coordinates'])[0]
            lon= re.split('/|,',location['gps_coordinates'])[1]

            name_full = name

            if 'name' in location:
                if len(location['name']) != 0:
                    name_full = ur'%s' %(location['name'])

            popup_content = ur'<b><a target=\\"_blank\\" href=\\"%s\\" title=\\"%s\\">%s</a></b>' % (url, full_postal_address, name_full)

            if 'description' in location:
                description_full = location['description']

            if len(description_full) > 0:
                popup_content += ur' - %s' % (description_full)

            result += (u'm=L.marker([%s,%s]); markers.push(m); m.addTo(map); m.on(\'click\', function(e) {cur_marker=this;})' % (lat, lon)).encode('utf-8')
            result += (u'    .bindPopup("%s");' % (popup_content)).encode('utf-8')

            list += (u'<li class="%s"><strong><a target="_blank" href="%s" title="%s">%s</a></strong> - %s <a href="" onclick="return locateCompany(map, %s, %s, %d);"><strong>Locate</strong></a></li>' % (country_code, url, short_postal_address, name_full, description_full, lat, lon, locations_nb)).encode('utf-8')

        list += ur'</ul>'.encode('utf-8')

        if locations > 0:
            locations_nb += locations
            companies_nb += 1

print "Write content to index.html"

map_content = re.sub('{{content}}', result, template_js)
index_content = re.sub('{{list}}', list, template_index)
index_content = re.sub('{{companies_nb}}', str(companies_nb), index_content)
index_content = re.sub('{{locations_nb}}', str(locations_nb), index_content)
fp_map.write(map_content)
fp_index.write(index_content)

print "OK"

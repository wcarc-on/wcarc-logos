#!/usr/bin/env python3

import math
import shapefile
import svgwrite


def mollweide_error(theta, lat):
    return 2*theta + math.sin(2*theta) - math.pi*math.sin(lat)


def mollweide(lat, lon):
    lat, lon = math.radians(lat), math.radians(lon)
    R = 90

    theta = lat
    while abs(mollweide_error(theta, lat)) > 1e-6:
        theta = theta - mollweide_error(theta, lat) / (2 + 2*math.cos(2*theta))

    x = R * 2 * lon * math.cos(theta) / math.pi
    y = R * math.sin(theta)
    return x, y


def plot(dwg, grp, coords, midx=[0], tabs=3):
    path = grp.add(dwg.path())
    last_move = None
    for i, coord in enumerate(coords):
        if coord == last_move:
            path.push('Z')
            continue

        if i in midx:
            letter = 'M'
            last_move = coord
        else:
            letter = 'L'

        x, y = mollweide(coord[1], coord[0])
        path.push(letter, round(x, 3), round(y, 3))


dwg = svgwrite.Drawing(filename='wcc_logo.svg', size=(730, 370))

map = dwg.add(dwg.g())
map.matrix(2, 0, 0, -2, 365, 185)
map.add(dwg.ellipse(center=(0, 0), r=(180, 90), fill='white',
                    stroke='black', stroke_width=2))
for lon in range(30, 180, 30):
    map.add(dwg.ellipse(center=(0, 0), r=(lon, 90), fill='none',
                        stroke='black', stroke_width=1))
map.add(dwg.line(start=(0, -90), end=(0, 90), stroke='black', stroke_width=1))
for lat in range(-60, 90, 30):
    x, y = mollweide(lat, 180)
    map.add(dwg.line(start=(-x, y), end=(x, y),
                     stroke='black', stroke_width=1))

sf = shapefile.Reader('mapdata/ne_110m_land')
for record, shape in zip(sf.records(), sf.shapes()):
    if len(shape.points) > 20:
        plot(dwg, map, shape.points, midx=shape.parts)

text = dwg.add(dwg.g())
text.matrix(2, 0, 0, 2, 365, 185)
text.add(dwg.text('WCARC', insert=(-1, 24), text_anchor='middle',
                  font_size='65px', font_family='Arial Black',
                  fill='red', stroke='black', stroke_width=2))

dwg.save()

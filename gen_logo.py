#!/usr/bin/env python3

import math
import shapefile


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


def plot(coords, midx=[0], tabs=3):
    tag = '  '*tabs+'<path d="'
    last_move = None
    for i, coord in enumerate(coords):
        if coord == last_move:
            tag += 'Z'
            continue

        if i in midx:
            letter = 'M'
            last_move = coord
        else:
            letter = 'L'

        x, y = mollweide(coord[1], coord[0])
        tag += '{}{:.3f},{:.3f} '.format(letter, x, y)
    tag += '"/>'
    print(tag)


def plot_shape(path):
    sf = shapefile.Reader(path)
    for record, shape in zip(sf.records(), sf.shapes()):
        if len(shape.points) > 20:
            plot(shape.points, midx=shape.parts)


print('<svg width="730" height="370">')
print('  <g transform="matrix(2,0,0,-2,365,185)">')
print('    <ellipse cx="0" cy="0" rx="180" ry="90" style="fill:white; stroke:black; stroke-width:2"/>')
for lon in range(30, 180, 30):
    print('    <ellipse cx="0" cy="0" rx="{0}" ry="90" style="fill:none; stroke:black; stroke-width:1"/>'.format(lon))
print('    <line x1="0" y1="-90" x2="0" y2="90" style="stroke:black; stroke-width:1" />')
for lat in range(-60, 90, 30):
    x, y = mollweide(lat, 180)
    print('    <line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:black; stroke-width:1" />'.format(-x, y, x, y))
print('    <g class="land">')
plot_shape('mapdata/ne_110m_land')
print('    </g>')
print('  </g>')
print('  <g transform="matrix(2,0,0,2,365,185)">')
print('    <text text-anchor="middle" x="-1" y="24" style="font-size: 65px; font-family: Arial Black; font-weight: 900; fill: red; stroke:black; stroke-width:2; stroke-linecap:butt; stroke-linejoin:miter;">WCARC</text>')
print('  </g>')
print('</svg>')

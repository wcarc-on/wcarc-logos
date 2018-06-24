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


def generate(filename, width, thumb=False):
    ellipse_width, grid_width, text_stroke = (4, 2, 3) if thumb else (2, 1, 2)
    height = width / 2
    padding = height * ellipse_width / 360
    tot_width, tot_height = width + padding*2, height + padding*2

    dwg = svgwrite.Drawing(filename=filename, size=(tot_width, tot_height))

    map = dwg.add(dwg.g())
    map.matrix(width / 360, 0, 0, -height / 180, tot_width / 2, tot_height / 2)
    map.add(dwg.ellipse(center=(0, 0), r=(180, 90), fill='white',
                        stroke='black', stroke_width=ellipse_width))
    for lon in range(30, 180, 30):
        map.add(dwg.ellipse(center=(0, 0), r=(lon, 90), fill='none',
                            stroke='black', stroke_width=grid_width))
    map.add(dwg.line(start=(0, -90), end=(0, 90),
                     stroke='black', stroke_width=grid_width))
    for lat in range(-60, 90, 30):
        x, y = mollweide(lat, 180)
        map.add(dwg.line(start=(-x, y), end=(x, y),
                         stroke='black', stroke_width=grid_width))

    sf = shapefile.Reader('mapdata/ne_110m_land')
    for record, shape in zip(sf.records(), sf.shapes()):
        if len(shape.points) > 20:
            plot(dwg, map, shape.points, midx=shape.parts)

    text = dwg.add(dwg.g())
    text.matrix(width / 360, 0, 0, height / 180, tot_width / 2, tot_height / 2)
    text.add(dwg.text('WCARC', insert=(2, 28), text_anchor='middle',
                      font_size='80px', font_family='Montserrat Black',
                      fill='red', stroke='black', stroke_width=text_stroke))

    dwg.save(pretty=True)


generate('wcc_logo.svg', width=601)
generate('wcc_logo_thumb.svg', width=100, thumb=True)

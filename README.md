wcarc-logos
===========

## Build instructions

```
sudo apt install inkscape
python3 -m venv venv
source venv/bin/activate
pip3 install pyshp svgwrite
mkdir -p ~/.fonts
cp fonts/Montserrat-Black.ttf ~/.fonts/
make
```

## Source material

1. Land polygons for the world map (in `/mapdata/`): http://www.naturalearthdata.com/downloads/110m-physical-vectors/
2. Montserrat font (in `/fonts/`): https://github.com/google/fonts/tree/master/ofl/montserrat

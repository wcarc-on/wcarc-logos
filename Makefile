SHELL = /bin/bash

SVG = wcc_logo.svg wcc_logo_thumb.svg
PATH_SVG = $(SVG:.svg=_path.svg)
PNG = $(SVG:.svg=.png)
PDF = $(SVG:.svg=.pdf)

GENERATED_FILES = $(SVG) $(PATH_SVG) $(PNG) $(PDF) wcc_logo_icon.png

.PHONY: all
all: $(GENERATED_FILES)

.PHONY: path_svg
path_svg: $(PATH_SVG)

.PHONY: png
png: $(PNG)

.PHONY: pdf
pdf: $(PDF)

wcc_logo.svg: gen_logo.py
	@./gen_logo.py

%_path.svg: %.svg
	@inkscape --export-text-to-path --export-plain-svg=$@ $<

%.png: %.svg
	@inkscape --export-png=$@ $<

wcc_logo_icon.png: wcc_logo_thumb.svg
	@inkscape -w 64 -h 64 --export-png=$@ $<

%.pdf: %.svg
	@inkscape --export-text-to-path --export-pdf=$@ $<

.PHONY: clean
clean:
	@rm -f $(GENERATED_FILES)

SHELL = /bin/bash

SVG = $(wildcard *.svg)
PNG = $(SVG:.svg=.png)
THUMB = $(SVG:.svg=.thumb.png)
PDF = $(SVG:.svg=.pdf)

GENERATED_FILES = $(PNG) $(THUMB) $(PDF)

.PHONY: all
all: $(GENERATED_FILES)

.PHONY: png
png: $(PNG)

.PHONY: thumb
thumb: $(THUMB)

.PHONY: pdf
pdf: $(PDF)

%.png: %.svg
	@inkscape --export-png=$@ $<

%.thumb.png: %.png
	@convert -size 125x125 -resize 125x125 $< $@

%.pdf: %.svg
	@inkscape --export-text-to-path --export-pdf=$@ $<

.PHONY: clean
clean:
	@rm -f $(GENERATED_FILES)

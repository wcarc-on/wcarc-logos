SHELL = /bin/bash

SVG = wcc_logo.svg wcc_logo_thumb.svg
PNG = $(SVG:.svg=.png)
PDF = $(SVG:.svg=.pdf)

GENERATED_FILES = $(SVG) $(PNG) $(PDF)

.PHONY: all
all: $(GENERATED_FILES)

.PHONY: png
png: $(PNG)

.PHONY: pdf
pdf: $(PDF)

wcc_logo.svg: gen_logo.py
	@./gen_logo.py

%.png: %.svg
	@inkscape --export-png=$@ $<

%.pdf: %.svg
	@inkscape --export-text-to-path --export-pdf=$@ $<

.PHONY: clean
clean:
	@rm -f $(GENERATED_FILES)

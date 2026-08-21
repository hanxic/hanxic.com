MAIN=cv
DATA_DIR=../data
GENERATED=generated/data.tex
DATA=$(wildcard $(DATA_DIR)/*.yaml)
SITE_CV=../static/cv/hanxi-chen-cv.pdf

.PHONY: all generate pdf install clean

all: install

generate: $(GENERATED)

$(GENERATED): $(DATA) ../scripts/yaml_to_tex_data.py
	python3 ../scripts/yaml_to_tex_data.py --data-dir $(DATA_DIR) --output $(GENERATED)

pdf: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex refs.bib $(GENERATED)
	latexmk -pdf $(MAIN)

install: $(SITE_CV)

$(SITE_CV): $(MAIN).pdf
	cp $(MAIN).pdf $(SITE_CV)

clean:
	latexmk -C $(MAIN)
	rm -f $(GENERATED)

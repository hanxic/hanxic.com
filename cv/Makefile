MAIN=cv
RESUME=resume
DATA_DIR=../data
GENERATED=generated/data.tex
DATA=$(wildcard $(DATA_DIR)/*.yaml)
BIB=../assets/data/refs.bib
SITE_CV=../static/cv/hanxi-chen-cv.pdf
SITE_RESUME=../static/cv/hanxi-chen-resume.pdf

.PHONY: all generate pdf install resume resume-pdf resume-install clean

all: install

generate: $(GENERATED)

$(GENERATED): $(DATA) ../scripts/yaml_to_tex_data.py
	python3 ../scripts/yaml_to_tex_data.py --data-dir $(DATA_DIR) --output $(GENERATED)

pdf: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex $(BIB) $(GENERATED)
	latexmk -pdf $(MAIN)

install: $(SITE_CV)

$(SITE_CV): $(MAIN).pdf
	cp $(MAIN).pdf $(SITE_CV)

resume: resume-install

resume-pdf: $(RESUME).pdf

$(RESUME).pdf: $(RESUME).tex $(BIB) $(GENERATED)
	latexmk -pdf $(RESUME)

resume-install: $(SITE_RESUME)

$(SITE_RESUME): $(RESUME).pdf
	cp $(RESUME).pdf $(SITE_RESUME)

clean:
	latexmk -C $(MAIN)
	latexmk -C $(RESUME)
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).fdb_latexmk
	rm -f $(MAIN).fls $(MAIN).log $(MAIN).out $(MAIN).pdf $(MAIN).run.xml $(MAIN)-blx.bib
	rm -f $(RESUME).aux $(RESUME).bbl $(RESUME).bcf $(RESUME).blg $(RESUME).fdb_latexmk
	rm -f $(RESUME).fls $(RESUME).log $(RESUME).out $(RESUME).pdf $(RESUME).run.xml $(RESUME)-blx.bib
	rm -rf generated

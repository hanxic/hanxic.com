MAIN=cv
RESUME=resume
DATA_DIR=../data
GENERATED=generated/data.tex
DATA=$(wildcard $(DATA_DIR)/*.yaml)
BIB=../assets/data/refs.bib
SITE_CV=../static/cv/hanxi-chen-cv.pdf
SITE_RESUME=../static/cv/hanxi-chen-resume.pdf

.PHONY: all generate pdf install resume resume-pdf resume-install force force-resume clean

all: install

$(GENERATED): $(DATA) ../scripts/yaml_to_tex_data.py
	python3 ../scripts/yaml_to_tex_data.py --data-dir $(DATA_DIR) --output $(GENERATED)

generate: $(GENERATED)

$(MAIN).pdf: $(MAIN).tex $(GENERATED) $(BIB)
	latexmk -pdf $(MAIN)

pdf: $(MAIN).pdf

$(SITE_CV): $(MAIN).pdf
	mkdir -p $(dir $@)
	cmp -s $< $@ || cp $< $@

install: $(SITE_CV)

resume: resume-install

$(RESUME).pdf: $(RESUME).tex $(GENERATED) $(BIB)
	latexmk -pdf $(RESUME)

resume-pdf: $(RESUME).pdf

$(SITE_RESUME): $(RESUME).pdf
	mkdir -p $(dir $@)
	cmp -s $< $@ || cp $< $@

resume-install: $(SITE_RESUME)

force: $(GENERATED)
	latexmk -pdf -g $(MAIN)
	mkdir -p $(dir $(SITE_CV))
	cp $(MAIN).pdf $(SITE_CV)

force-resume: $(GENERATED)
	latexmk -pdf -g $(RESUME)
	mkdir -p $(dir $(SITE_RESUME))
	cp $(RESUME).pdf $(SITE_RESUME)

clean:
	latexmk -C $(MAIN)
	latexmk -C $(RESUME)
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).fdb_latexmk
	rm -f $(MAIN).fls $(MAIN).log $(MAIN).out $(MAIN).pdf $(MAIN).run.xml $(MAIN)-blx.bib
	rm -f $(RESUME).aux $(RESUME).bbl $(RESUME).bcf $(RESUME).blg $(RESUME).fdb_latexmk
	rm -f $(RESUME).fls $(RESUME).log $(RESUME).out $(RESUME).pdf $(RESUME).run.xml $(RESUME)-blx.bib
	rm -rf generated

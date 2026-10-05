MAIN=cv
RESUME=resume
DATA_DIR=../data
GENERATED=generated/data.tex
# publications.yaml is generated from refs.bib and carries `_tex: skip: true`, so
# it never reaches data.tex. Excluding it keeps a site rebuild from relinking both PDFs.
DATA=$(filter-out $(DATA_DIR)/publications.yaml,$(wildcard $(DATA_DIR)/*.yaml))
BIB=../assets/data/refs.bib
SITE_CV=../static/cv/hanxi-chen-cv.pdf
SITE_RESUME=../static/cv/hanxi-chen-resume.pdf
# A variant is a directory of sparse YAML overlaid on ../data -- one per tailored
# application. `make resume-amazon.pdf` builds data-variants/amazon. Variant PDFs
# stay in cv/ and are never copied to static/: the site publishes the master only.
VARIANT_DIR=../data-variants

.PHONY: all generate pdf install resume resume-pdf resume-install commit force force-resume variants clean

all: pdf resume-pdf

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

resume: resume-pdf

$(RESUME).pdf: $(RESUME).tex $(GENERATED) $(BIB)
	latexmk -pdf $(RESUME)

resume-pdf: $(RESUME).pdf

$(SITE_RESUME): $(RESUME).pdf
	mkdir -p $(dir $@)
	cmp -s $< $@ || cp $< $@

resume-install: $(SITE_RESUME)

commit: install resume-install

force: $(GENERATED)
	latexmk -pdf -g $(MAIN)

force-resume: $(GENERATED)
	latexmk -pdf -g $(RESUME)

# Without this make treats the variant data as an intermediate and deletes it
# after each build, which forces a full regenerate-and-typeset every time.
.PRECIOUS: generated/data-%.tex

generated/data-%.tex: $(DATA) ../scripts/yaml_to_tex_data.py $(wildcard $(VARIANT_DIR)/%/*.yaml)
	python3 ../scripts/yaml_to_tex_data.py --data-dir $(DATA_DIR) \
	  --overlay-dir $(VARIANT_DIR)/$* --output $@

# -jobname keeps each variant's aux/bcf/pdf separate, so biber and latexmk never
# see the master's state. %S is the source file; the \def wins over resume.tex's
# \providecommand and redirects it at the overlaid data.
$(RESUME)-%.pdf: $(RESUME).tex generated/data-%.tex $(BIB)
	latexmk -pdf -jobname=$(RESUME)-$* \
	  -pdflatex='pdflatex %O "\def\CVDataFile{generated/data-$*.tex}\input{%S}"' $(RESUME).tex

variants: $(patsubst $(VARIANT_DIR)/%,$(RESUME)-%.pdf,$(wildcard $(VARIANT_DIR)/*))

clean:
	latexmk -C $(MAIN)
	latexmk -C $(RESUME)
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).bcf $(MAIN).blg $(MAIN).fdb_latexmk
	rm -f $(MAIN).fls $(MAIN).log $(MAIN).out $(MAIN).pdf $(MAIN).run.xml $(MAIN)-blx.bib
	rm -f $(RESUME).aux $(RESUME).bbl $(RESUME).bcf $(RESUME).blg $(RESUME).fdb_latexmk
	rm -f $(RESUME).fls $(RESUME).log $(RESUME).out $(RESUME).pdf $(RESUME).run.xml $(RESUME)-blx.bib
	rm -f *-SAVE-ERROR
	rm -rf generated

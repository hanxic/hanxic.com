HUGO ?= hugo
HUGO_FLAGS ?=
HUGO_SERVER_FLAGS ?= -D
CV_DIR ?= cv
PUBLICATIONS_BIB ?= assets/data/refs.bib
PUBLICATIONS_DATA ?= data/publications.yaml
PUBLICATIONS_SCRIPT ?= scripts/bib_to_publications_yaml.py

.PHONY: all build site serve cv cv-pdf cv-data resume resume-pdf commit commit-cv commit-resume publications-data clean clean-site clean-cv clean-data help

# `cv` and `resume` are separate recursions into cv/, and both build generated/data.tex.
# Under -j they would race on that one file, so the top level stays serial.
.NOTPARALLEL:

all: build

build: publications-data cv resume site

site: publications-data
	$(HUGO) $(HUGO_FLAGS)

serve: publications-data
	$(HUGO) server $(HUGO_SERVER_FLAGS)

cv:
	$(MAKE) -C $(CV_DIR) pdf

cv-pdf: cv

cv-data:
	$(MAKE) -C $(CV_DIR) generate

resume:
	$(MAKE) -C $(CV_DIR) resume-pdf

resume-pdf: resume

commit: commit-cv commit-resume

commit-cv:
	$(MAKE) -C $(CV_DIR) install

commit-resume:
	$(MAKE) -C $(CV_DIR) resume-install

publications-data: $(PUBLICATIONS_DATA)

$(PUBLICATIONS_DATA): $(PUBLICATIONS_BIB) $(PUBLICATIONS_SCRIPT)
	python3 $(PUBLICATIONS_SCRIPT) --input $(PUBLICATIONS_BIB) --output $(PUBLICATIONS_DATA)

clean: clean-cv clean-site clean-data

clean-site:
	rm -rf public

clean-data:
	rm -f $(PUBLICATIONS_DATA)

clean-cv:
	$(MAKE) -C $(CV_DIR) clean

help:
	@echo "Targets:"
	@echo "  make          Regenerate publication data, compile the CV/resume PDFs as"
	@echo "               needed, then build the Hugo site without committing the PDFs"
	@echo "  make build    Same as make"
	@echo "  make site     Build the Hugo site only"
	@echo "  make serve    Start the Hugo development server with drafts"
	@echo "  make cv       Build cv/cv.pdf without copying it into static/cv"
	@echo "  make cv-pdf   Same as make cv"
	@echo "  make cv-data  Regenerate cv/generated/data.tex from data/*.yaml"
	@echo "  make resume   Build cv/resume.pdf without copying it into static/cv"
	@echo "  make resume-pdf  Same as make resume"
	@echo "  make commit   Commit both compiled PDFs to static/cv"
	@echo "  make commit-cv"
	@echo "               Build and commit only the CV PDF to static/cv"
	@echo "  make commit-resume"
	@echo "               Build and commit only the resume PDF to static/cv"
	@echo "  make publications-data"
	@echo "               Regenerate data/publications.yaml from assets/data/refs.bib"
	@echo "  make clean    Remove generated CV files, publication data, and Hugo output"

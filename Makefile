HUGO ?= hugo
HUGO_FLAGS ?=
HUGO_SERVER_FLAGS ?= -D
CV_DIR ?= cv
PUBLICATIONS_BIB ?= assets/data/refs.bib
PUBLICATIONS_DATA ?= data/publications.yaml
PUBLICATIONS_SCRIPT ?= scripts/bib_to_publications_yaml.py

.PHONY: all build site serve cv cv-pdf cv-data resume resume-pdf publications-data clean clean-site clean-cv help

all: build

build: cv site

site: publications-data
	$(HUGO) $(HUGO_FLAGS)

serve: publications-data
	$(HUGO) server $(HUGO_SERVER_FLAGS)

cv:
	$(MAKE) -C $(CV_DIR) install

cv-pdf:
	$(MAKE) -C $(CV_DIR) pdf

cv-data:
	$(MAKE) -C $(CV_DIR) generate

resume:
	$(MAKE) -C $(CV_DIR) resume-install

resume-pdf:
	$(MAKE) -C $(CV_DIR) resume-pdf

publications-data: $(PUBLICATIONS_DATA)

$(PUBLICATIONS_DATA): $(PUBLICATIONS_BIB) $(PUBLICATIONS_SCRIPT)
	python3 $(PUBLICATIONS_SCRIPT) --input $(PUBLICATIONS_BIB) --output $(PUBLICATIONS_DATA)

clean: clean-cv clean-site

clean-site:
	rm -rf public

clean-cv:
	$(MAKE) -C $(CV_DIR) clean

help:
	@echo "Targets:"
	@echo "  make          Refresh the CV PDF and build the Hugo site"
	@echo "  make build    Same as make"
	@echo "  make site     Build the Hugo site only"
	@echo "  make serve    Start the Hugo development server with drafts"
	@echo "  make cv       Generate CV data, build the PDF, and install it into static/cv"
	@echo "  make cv-pdf   Build cv/cv.pdf without copying it into static/cv"
	@echo "  make cv-data  Regenerate cv/generated/data.tex from data/*.yaml"
	@echo "  make resume   Generate and install the one-page resume PDF into static/cv"
	@echo "  make resume-pdf"
	@echo "               Build cv/resume.pdf without copying it into static/cv"
	@echo "  make publications-data"
	@echo "               Regenerate data/publications.yaml from assets/data/refs.bib"
	@echo "  make clean    Remove generated CV files and Hugo public output"

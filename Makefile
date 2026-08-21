HUGO ?= hugo
HUGO_FLAGS ?=
HUGO_SERVER_FLAGS ?= -D
CV_DIR ?= cv

.PHONY: all build site serve cv cv-pdf cv-data clean clean-site clean-cv help

all: build

build: cv site

site:
	$(HUGO) $(HUGO_FLAGS)

serve:
	$(HUGO) server $(HUGO_SERVER_FLAGS)

cv:
	$(MAKE) -C $(CV_DIR) install

cv-pdf:
	$(MAKE) -C $(CV_DIR) pdf

cv-data:
	$(MAKE) -C $(CV_DIR) generate

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
	@echo "  make clean    Remove generated CV files and Hugo public output"

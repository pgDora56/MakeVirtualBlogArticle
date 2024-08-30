.PHONY: all 
all: scrape run

.PHONY: scrape
scrape:
	@echo "Scraping blog..."
	@python3 scrape.py

.PHONY: run
run:
	@echo "Creating blog..."
	@python3 -m http.server
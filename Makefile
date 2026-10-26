IMAGE ?= de-workspace
RUN = docker run --rm --memory=4g --cpus=4 -v "$(CURDIR)":/workspace -v de-ivy-cache:/root/.ivy2

.PHONY: build test test-solutions lint data

build:
	docker build -t $(IMAGE) .

test:
	$(RUN) $(IMAGE) pytest

test-solutions:
	$(RUN) -e USE_SOLUTIONS=1 $(IMAGE) pytest

lint:
	$(RUN) $(IMAGE) ruff check .

data:
	python data/generate_data.py --rows-per-month 50000

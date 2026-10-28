IMAGE ?= de-workspace
RUN = docker run --rm --memory=4g --cpus=4 -v "$(CURDIR)":/workspace -v de-ivy-cache:/root/.ivy2

.PHONY: build test test-one test-solutions lint data

build:
	docker build -t $(IMAGE) .

test:
	$(RUN) $(IMAGE) pytest

# Usage: make test-one T="tests/test_w01_pyspark_core.py -k large_baskets"
test-one:
	$(RUN) $(IMAGE) pytest $(T) -q -p no:cacheprovider

test-solutions:
	$(RUN) -e USE_SOLUTIONS=1 $(IMAGE) pytest

lint:
	$(RUN) $(IMAGE) ruff check .

data:
	python data/generate_data.py --rows-per-month 50000

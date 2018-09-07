IMAGE_NAME = mocksi
VERSION = latest
IMAGE = $(IMAGE_NAME):$(VERSION)

.PHONY: all

all:
	$(MAKE) test
	$(MAKE) build
	$(MAKE) run

test:
	python -m unittest discover tests/unit/ -v
	python -m unittest discover tests/integration/ -v

build:
	docker build -t $(IMAGE) --force-rm .

run:
	docker run -v /var/run/docker.sock:/var/run/docker.sock -p 9090:9090 $(IMAGE)

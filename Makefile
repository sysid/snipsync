# You can set these variables from the command line, and also from the environment for the first two.
SOURCEDIR     = source
BUILDDIR      = build
MAKE          = make
VERSION       = $(shell cat snipsync/__init__.py | grep __version__ | sed "s/__version__ = //" | sed "s/'//g")

.DEFAULT_GOAL := help

app_root = .
pkg_src =  $(app_root)/snipsync
tests_src = $(app_root)/tests

# pipx installed globals
isort = isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 $(pkg_src) $(tests_src)
black = black $(pkg_src) $(tests_src)
tox = tox
mypy = mypy $(pkg_src)
pipenv = pipenv
#mypy = mypy --config-file $(app_root)/mypy.ini $(pkg_src)

.PHONY: all
all: build upload tag  ## Build all
	@echo "--------------------------------------------------------------------------------"
	@echo "-M- building and distributing"
	@echo "--------------------------------------------------------------------------------"

.PHONY: test
test:  ## run tests
	#./scripts/test
	python -m pytest -ra

.PHONY: tox
tox:   ## Run tox
	$(tox)

.PHONY: coverage
coverage:  ## Run tests with coverage
	python -m coverage erase
	python -m coverage run --include=$(pkg_src)/* -m pytest -ra
	#python -m coverage report -m
	python -m coverage html
	open htmlcov/index.html  # work on macOS

.PHONY: clean
clean:  ## clean dist
	@echo "Cleaning up..."
	#git clean -Xdf
	rm -rf dist

.PHONY: build
build: clean black isort  ## build and lint
	@echo "building"
	#python setup.py sdist
	python -m build

.PHONY: upload
upload:  ## upload
	@echo "upload"
	twine upload --verbose dist/*

.PHONY: tag
tag:  ## tag
	@echo "tagging $(VERSION)"
	git tag -a $(VERSION) -m "version $(VERSION)"
	git push --tags

.PHONY: mypy
mypy:  ## type check
	$(mypy)

.PHONY: black
black:  ## format with black
	$(black)

.PHONY: isort
isort:  ## isort
	$(isort)

.PHONY: bump-minor
bump-minor:  ## bump-minor
	bumpversion --verbose minor

.PHONY: bump-patch
bump-patch:  ## bump-patch
	bumpversion --verbose patch

.PHONY: dist-test
dist-test: dist  ## test a wheel distribution package
	@cd dist && ../tests/test-dist.bash ./snipsync-*-py3-none-any.whl

.PHONY: help
help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done

VERSION_FILE := VERSION
CURRENT_VERSION := $(shell cat $(VERSION_FILE))

# Logika podbijania wersji (X.Y.Z -> X.Y.Z+1)
# Użyłem awk, który obsłuży format semver (np. 0.1.0 -> 0.1.1)
NEXT_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. '{print $$1"."$$2"."$$3+1}')

.PHONY: build bump git-tag release ruff

build:
	@echo "Building dedu-py version $(CURRENT_VERSION)..."
	uv build

# Podbicie wersji w pliku
bump:
	@echo "Bumping version: $(CURRENT_VERSION) -> $(NEXT_VERSION)"
	@echo $(NEXT_VERSION) > $(VERSION_FILE)

# Git commit i tagowanie (identycznie jak w Twoim przykładzie)
git-tag:
	git add $(VERSION_FILE)
	@echo "CURRENT_VERSION: $(NEXT_VERSION)"
	git commit -m "chore: bump version to $(NEXT_VERSION)"
	git tag -a "v$(NEXT_VERSION)" -m "Release v$(NEXT_VERSION)"
	git push origin main --tags

# Pełny cykl: podbijasz wersję -> budujesz paczkę -> tagujesz w git
release: bump build git-tag
	@echo "Release $(NEXT_VERSION) finished. Ready for PyPI or GitHub Release."

ruff:
	@echo "running lint and format using ruff"
	ruff check --fix ./
	ruff format ./

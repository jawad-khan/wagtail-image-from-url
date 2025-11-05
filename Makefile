.PHONY: help clean install build check publish-test publish dev-setup

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean:  ## Remove build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

install:  ## Install package in editable mode
	pip install -e .

install-build-tools:  ## Install tools needed for building and publishing
	pip install --upgrade pip build "setuptools>=61.0,<70.0" wheel twine

build: clean install-build-tools  ## Build distribution packages
	python -m build
	@echo "\nBuild complete! Packages created in dist/"
	@ls -lh dist/

check: build  ## Build and check package with twine
	python -m twine check dist/*
	@echo "\nPackage validation successful!"

publish-test: check  ## Publish to TestPyPI
	@echo "Publishing to TestPyPI..."
	python -m twine upload --repository testpypi dist/*

publish: check  ## Publish to PyPI (use with caution!)
	@echo "⚠️  Publishing to PyPI..."
	@read -p "Are you sure you want to publish to PyPI? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python -m twine upload dist/*; \
	else \
		echo "Cancelled."; \
	fi

dev-setup: install-build-tools install  ## Complete development environment setup
	@echo "Development environment setup complete!"
	@echo "Note: Install testing/linting tools separately if needed (pytest, black, flake8, etc.)"


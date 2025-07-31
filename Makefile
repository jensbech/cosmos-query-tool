.PHONY: help install install-dev clean dist binary format lint typecheck

help:
	@echo ""
	@echo "  install     - Install the package"
	@echo "  install-dev - Install in development mode with dev dependencies"
	@echo "  clean       - Clean build artifacts"
	@echo "  dist        - Build standalone binary executable (runs lint and typecheck first)"
	@echo "  format      - Format code with black"
	@echo "  lint        - Run linting with flake8"
	@echo "  typecheck   - Run type checking with mypy"
	@echo ""

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/cosmos_query/__pycache__/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

dist: install format clean lint typecheck
	@echo "Building standalone binary..."
	./scripts/build_binary.sh

format:
	black src/cosmos_query/

lint:
	flake8 src/cosmos_query/ --max-line-length=88 --exclude=build,dist,*.egg-info

typecheck:
	mypy src/cosmos_query/

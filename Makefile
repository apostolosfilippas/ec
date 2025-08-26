# RAGbench Development Makefile
# - Common commands for RAGbench development workflow
.PHONY: help install clean format lint docs
# - Add common poetry installation paths to PATH
export PATH := $(HOME)/.local/bin:$(PATH)

###############
##@⭐ Utils
###############
help: ## Show this helpful message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "   \033[33m%-25s\033[0m %s\n", $$1, $$2} /^##@/ {printf "\n\033[0;32m%s\033[0m\n", substr($$0, 4)} ' $(MAKEFILE_LIST)

###############
##@💻 Local Development
###############
check-venv-not-active: ## Check if venv is not active
	@echo "Checking whether the venv is not active..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "❗ Your virtual environment is active. Please deactivate it."; \
		exit 1; \
	fi

clean-venv: ## Clean Python venv
	@echo "Cleaning Python venv..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Your Python virtual environment is active. Please deactivate it."; \
		exit 1; \
	fi
	@[ ! -d .venv ] || rm -rf .venv

clean-temp: ## Clean temporary files and caches
	@echo "🧹 Cleaning temp files..."
	@rm -rf temp/*.pdf
	@rm -rf temp/*.csv
	@echo "Cleanup complete!"

install: ## Install all project deps and create a .venv
	@make clean-venv
	@echo "Creating a venv from pyproject.toml and installing deps using poetry..."
	poetry install --with dev
	@echo "Installing pre-commit hooks..."
	poetry run pre-commit install
	@echo "All deps installed and venv created."
	@echo "Use 'eval $$(poetry env activate)' to activate the venv."

###############
##@🔧 Code Quality
###############
format: ## Run black on all Python files
	@echo "Running black on all Python files..."
	@poetry run black --line-length 100 ragbench/
	@poetry run black --line-length 100 scripts/

pre-commit-run: ## Run pre-commit on all files
	@echo "Running pre-commit on all files..."
	@poetry run pre-commit run --all-files

###############
##@🚀 Testing
###############

# Run all scripts in the scripts/ folder
run-scripts: ## Run all Python scripts from clean slate, stop on any error
	@make clean-temp
	@echo "🐍 Running all Python scripts in order with error checking..."
	@set -e; \
	for script in scripts/1.introduction.py \
	              scripts/2.dataframes.py \
	              scripts/3.visualization.py \
	              scripts/4.combining.py \
	              scripts/5.inflation.py \
	              scripts/6.pricing.py \
	              scripts/7.randomization.py \
	              scripts/8.experiments.py \
	              scripts/9.experiments-advanced.py; do \
		echo ""; \
		echo "🚀 Running $$script..."; \
		python $$script || { echo "❌ Error in $$script - stopping execution"; exit 1; }; \
		echo "✅ $$script completed successfully"; \
	done
	@echo ""
	@echo "🎉 All scripts completed successfully!"
	@echo "📊 Check the temp/ folder for generated visualizations"
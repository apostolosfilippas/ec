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

export: ## Export current venv packages to requirements.txt
	@echo "📦 Exporting packages from .venv to requirements.txt..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		pip freeze > requirements.txt; \
		echo "✅ requirements.txt created successfully with $$(wc -l < requirements.txt) packages"; \
	else \
		echo "❗ Virtual environment is not active. Please activate your .venv first."; \
		exit 1; \
	fi

install-requirements: ## Install packages from requirements.txt (requires active venv)
	@echo "📦 Installing packages from requirements.txt..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		if [ -f requirements.txt ]; then \
			pip install -r requirements.txt; \
			echo "✅ All packages from requirements.txt installed successfully"; \
		else \
			echo "❗ requirements.txt not found. Run 'make export' first to create it."; \
			exit 1; \
		fi; \
	else \
		echo "❗ Virtual environment is not active. Please activate your .venv first."; \
		exit 1; \
	fi

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
##@🚀 User
###############
pdfs: ## Convert all Jupyter notebooks in the scripts/ folder to PDF and save in temp/
	@echo "📓 Converting all Jupyter notebooks to PDF..."
	@make clean-temp
	@set -e; \
	for notebook in scripts/*.ipynb; do \
		if [ -f "$$notebook" ]; then \
			notebook_name=$$(basename "$$notebook" .ipynb); \
			echo "🔄 Converting $$notebook_name.ipynb to PDF..."; \
			jupyter nbconvert --to webpdf --allow-chromium-download "$$notebook" --output-dir temp/ || { echo "❌ Error converting $$notebook"; exit 1; }; \
			echo "✅ $$notebook_name.pdf created successfully"; \
		fi; \
	done
	@echo ""
	@echo "🎉 All notebooks converted to PDF!"
	@echo "📂 PDFs saved in temp/ directory"

# Run all scripts in the scripts/ folder
run-scripts: ## Run all Python scripts from clean slate, stop on any error
	@make clean-temp
	@echo "🐍 Running all Python scripts in order with error checking..."
	@set -e; \
	for script in scripts/0.simple.py \
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

# Run all notebooks in the scripts/ folder
run-notebooks: ## Run all Jupyter notebooks from clean slate, stop on any error
	@make clean-temp
	@echo "📓 Running all Jupyter notebooks in order with error checking..."
	@set -e; \
	for notebook in scripts/1.introduction.ipynb \
	              scripts/2.dataframes.ipynb \
	              scripts/3.visualization.ipynb \
	              scripts/4.combining.ipynb \
	              scripts/5.inflation.ipynb \
	              scripts/6.pricing.ipynb \
	              scripts/7.randomization.ipynb \
	              scripts/8.experiments.ipynb \
	              scripts/9.experiments-advanced.ipynb; do \
		echo ""; \
		echo "🚀 Running $$notebook..."; \
		jupyter nbconvert --to notebook --execute --inplace "$$notebook" || { echo "❌ Error in $$notebook - stopping execution"; exit 1; }; \
		echo "✅ $$notebook completed successfully"; \
	done
	@echo ""
	@echo "🎉 All notebooks completed successfully!"
	@echo "📊 Check the temp/ folder for generated visualizations"
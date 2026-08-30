# Marketplaces

## Description
This is the hands-on portion of our Marketplaces class
- We will be using Python 3.13
- We use **uv** for Python version management and package management
- We will cover topics from basic data manipulation to advanced experimental design.

My sole hope is that this will help you get your hands dirty with Python.


## Prerequisites

### 1. Install uv (Python Package Manager)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal and verify:
```bash
uv --version
```

### 2. Clone this repository
```bash
git clone https://github.com/apostolosfilippas/ma.git
cd ma
```

### 3. Install Python and dependencies
```bash
make install
```

This will:
- Install Python 3.13 (if not already installed)
- Create a virtual environment
- Install all required packages
- Install pre-commit hooks
- Register the Jupyter kernel


## Roadmap

| Class | Topic | Script | Key Concepts |
|-------|-------|--------|--------------|
| 0 | **Getting Started** | `0.simple.ipynb` | Variables, data types, basic operations |
| 1 | **Python Fundamentals** | `1.introduction.ipynb` | Variables, data types, basic operations |
| 2 | **DataFrames & Analysis** | `2.dataframes.ipynb` | pandas, data manipulation, method chaining |
| 3 | **Data Visualization** | `3.visualization.ipynb` | matplotlib, seaborn, statistical plots |
| 4 | **Combining Data** | `4.combining.ipynb` | Merging, joining, concatenating datasets |
| 5 | **Time Series Analysis** | `5.inflation.ipynb` | Reputation inflation, trend analysis |
| 6 | **Pricing Behavior** | `6.pricing.ipynb` | Market dynamics, pricing patterns |
| 7 | **Randomized Assignment** | `7.randomization.ipynb` | A/B testing, balance tests |
| 8 | **Experiment Analysis** | `8.experiments.ipynb` | Treatment effects, statistical significance |
| 9 | **Statistical Foundations** | `9.experiments-advanced.ipynb` | Law of Large Numbers, Central Limit Theorem |


## Quick Reference

### Common Commands

```bash
# Install everything
make install

# Uninstall (remove venv and hooks)
make uninstall

# Add a new package
make add PKG=package-name

# Remove a package
make remove PKG=package-name

# Run a Python script
make run SCRIPT=scripts/0.simple.py

# Start Jupyter notebook
make jupyter

# See all available commands
make help
```

### Running Python with uv

```bash
# Run a script
uv run python scripts/0.simple.py

# Open Python REPL
uv run python

# Install a package
uv add package-name
```

.PHONY: help clean reaclean rar-build \
setup mypy-setup mypy-setup \
freshen git-freshen uv-check

REPO_URL := https://github.com/tycarac/trades.git
BACKUP_PATH="${HOME}/pCloudDrive"
DEST_PATH="${BACKUP_PATH}/git"

freshen: git-freshen uv-setup
	uv lock --upgrade
	uv sync


setup: mypy-setup update


help:
	@echo "Make targets:"
	@echo "  setup"
	@echo "  freshen"
	@echo "  clean"
	@echo "  reaclean"
	@echo "  duckdb-setup"
	@echo "  uv-setup"
	@echo "  git-freshen"
	@echo "  rar-build"
	@echo "  help"


uv-setup:
	@export PATH="$$HOME/.local/bin:$$PATH";
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl --proto '=https' --tlsv1.2 -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "Updating uv..."; \
		uv self update; \
	fi


clean:
	@echo "Removing Python build artifacts and cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.bak" -delete
	find . -type f -name "*.bak.*" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	@echo "Cleanup complete."


realclean: clean
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +


rar-build:
	@echo "Creating rar archive..."
	rar u -as -x*.rar trades.rar .
	@if mountpoint -q "${BACKUP_PATH}" && [ -d "${DEST_PATH}" ]; then \
		echo "Copying archive to ${DEST_PATH}"; \
		rsync -u *.rar "${DEST_PATH}/"; \
	fi


git-freshen:
	@if [ ! -d "./.git" ]; then \
		echo "Cloning repository: $(REPO_URL)"; \
		git clone "$(REPO_URL)"; \
	else \
		echo "Updating repository: $(REPO_URL)"; \
		git pull --ff-only --prune; \
	fi


mypy-setup:
	sudo apt update & apt install -y mypy
	mypy --install-types

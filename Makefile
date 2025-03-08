// Lint target for Mojo code integration
lint:
	@echo "Running Mojo lint in anthropic_client_mojo directory..."
	cd anthropic_client_mojo && mojo-lint *.mojo 
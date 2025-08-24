format:
	uv run ruff format .
	uv run ruff check --fix .

serve:
	uv run -m app.main
start:
	poetry run python main.py

localization:
	poetry run pybabel compile -d src/localization

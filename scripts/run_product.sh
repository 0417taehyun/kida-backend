poetry run gunicorn -c src/core/gunicorn_config.py src.main:app

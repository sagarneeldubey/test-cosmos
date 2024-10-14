FROM python:3.11-slim@sha256:17ec9dc2367aa748559d0212f34665ec4df801129de32db705ea34654b5bc77a

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This disables virtual env creation
ENV POETRY_VIRTUALENVS_CREATE 0

RUN apt-get -y update \
    && apt-get install -y locales locales-all gnupg sudo curl wget vim \
    unzip rsyslog gettext patch gcc g++ build-essential \
    pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl xpdf \
    && apt-get dist-upgrade -y \
    && rm -rf /var/lib/apt/lists


RUN pip install --upgrade pip poetry Cython~=3.0 gitignore_parser~=0.1

WORKDIR /app

# makes sure that dependencies are pulled from cache if no changes to toml or lock file
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-cache && rm -rf /root/.cache/

COPY . .

RUN poetry install --only-root

EXPOSE 2432

CMD uvicorn app.main:app --host=0.0.0.0 --port=2432
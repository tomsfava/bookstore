FROM python:3.13.3-slim AS python-base

# Configurações de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PATH="/opt/poetry/bin:/opt/pysetup/.venv/bin:$PATH"

# Instala dependências do sistema
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Define o diretório de trabalho para instalar as dependências
WORKDIR $PYSETUP_PATH

# Copia os arquivos de dependências
COPY poetry.lock pyproject.toml ./

# Instala as dependências sem os devs (caso deseje em produção)
RUN poetry install --no-root --only main

# Define diretório do projeto
WORKDIR /app

# Copia o restante do código da aplicação
COPY ./app .

# Expõe a porta usada pelo Django
EXPOSE 8000

# Comando padrão para iniciar o servidor
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.8.6-slim

RUN pip3 install poetry

WORKDIR /osol_app
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev

COPY osol osol
RUN poetry install --no-dev

EXPOSE 8501
CMD [ "poetry", "run", "streamlit", "run", "--server.address", "0.0.0.0", "--server.port", "8501", "osol/extremum/app/optimizer.py" ]

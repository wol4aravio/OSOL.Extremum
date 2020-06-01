FROM python:3.7.7-slim

LABEL Author="wol4aravio <panovskiy.v@yandex.ru>"
LABEL Description="Demo App for OSOL.Extremum"

RUN pip3 install poetry

WORKDIR /osol_app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY osol osol

EXPOSE 8501
CMD poetry run streamlit run --server.headless=true --server.address=0.0.0.0 --browser.gatherUsageStats=false osol/demo/dummy.py

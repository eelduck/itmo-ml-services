FROM python:3.10.11-slim

ENV WORKDIR=/app
WORKDIR ${WORKDIR}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/
COPY src/test.db ./db/

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/src"

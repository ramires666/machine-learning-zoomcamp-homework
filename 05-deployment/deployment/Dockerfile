FROM agrigorev/zoomcamp-model:2025

WORKDIR /"app"
COPY pyproject.toml .
COPY server.py .
RUN pip install --no-cache-dir .
COPY ./pipeline_v1.bin .
EXPOSE 9999
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9999"]
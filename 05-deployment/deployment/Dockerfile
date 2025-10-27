FROM agrigorev/zoomcamp-model:2025

WORKDIR /code
COPY pyproject.toml .
COPY server2.py .
RUN pip install --no-cache-dir .
EXPOSE 9999
CMD ["uvicorn", "server2:app", "--host", "0.0.0.0", "--port", "9999"]
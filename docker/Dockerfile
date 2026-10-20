FROM python:3.12-slim
WORKDIR /app
COPY python/etl.py /app/python/etl.py
COPY datasets /app/datasets
RUN mkdir /app/output && chown -R 10001:10001 /app
USER 10001:10001
CMD ["python", "python/etl.py"]

FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./personas.json .
COPY ./mcp_config.json .
COPY ./knowledge_base.yaml .

COPY ./lib ./lib
COPY ./migrate.py .
COPY ./settings.py .
COPY ./main.py .

EXPOSE 3000

CMD ["python", "main.py"]

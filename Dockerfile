FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8503

HEALTHCHECK CMD curl --fail http://localhost:8503/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "src/ui/app.py", "--server.port=8503", "--server.address=0.0.0.0"]

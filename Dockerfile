FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN useradd -m appuser
USER appuser

COPY --chown=appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser . .

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "interview.py", "--server.address=0.0.0.0"]

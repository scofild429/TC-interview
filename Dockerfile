FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies as root to ensure they are globally accessible
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser

# Copy application code with correct ownership
COPY --chown=appuser . .

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "interview.py", "--server.address=0.0.0.0"]
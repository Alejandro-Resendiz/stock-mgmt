# Builder Stage
FROM python:3.12-slim AS builder

# Working directory
RUN mkdir /app
WORKDIR /app

# Env variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Python dependencies
RUN pip install --upgrade pip 
COPY ./backend/requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

# Production Stage 
FROM python:3.12-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Source code
WORKDIR /app
COPY --chown=appuser:appuser ./backend .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
USER appuser
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "inventorymgmt.wsgi:application"]
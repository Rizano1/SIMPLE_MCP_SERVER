FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DB path bisa diubah via ENV kalau perlu
ENV DB_PATH=/app/whoa.db
ENV PORT=8000

EXPOSE 8000
CMD ["python", "server.py"]

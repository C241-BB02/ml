FROM python:3.12.0-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ENV FLASK_ENV=production
CMD ["python", "app.py"]

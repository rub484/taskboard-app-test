# --- Stage 1: build Tailwind CSS ---
FROM node:22-alpine AS css
WORKDIR /app
COPY package.json ./
RUN npm install
COPY static/src ./static/src
COPY templates ./templates
RUN npm run build:css

# --- Stage 2: Django app ---
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=css /app/static/css/app.css ./static/css/app.css
RUN DJANGO_SECRET_KEY=build python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]

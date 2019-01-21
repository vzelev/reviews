FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

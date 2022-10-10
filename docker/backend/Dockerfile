FROM python:3.10
WORKDIR /app
# COPY ./backend/ .
COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

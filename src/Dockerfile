FROM alpine:3.24

RUN apk add python3

COPY requirements.txt /app/requirements.txt
RUN python3 -m venv /venv && /venv/bin/pip install -r /app/requirements.txt

COPY ./ /app/src/

WORKDIR /app/src
VOLUME /app/src/db.sqlite3
EXPOSE 8000

CMD ["/bin/sh", "-c", "/venv/bin/python manage.py migrate --noinput && /venv/bin/python manage.py collectstatic --noinput && /venv/bin/python manage.py runserver 0.0.0.0:8000"]

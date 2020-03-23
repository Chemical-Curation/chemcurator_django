FROM python:3.8-buster

COPY requirements.txt /requirements.txt
RUN pip --no-cache-dir install -r /requirements.txt \
 && rm /requirements.txt

COPY . /app/.
WORKDIR /app
RUN python manage.py collectstatic

CMD gunicorn config.wsgi -c config/gunicorn.py

EXPOSE 8000
VOLUME /app/collected_static

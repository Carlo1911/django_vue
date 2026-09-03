FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1
ENV C_FORCE_ROOT=true
ENV TZ=America/Lima
RUN mkdir -p /backend /static /media \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /backend

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD ./backend /backend
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.pip
CMD python manage.py collectstatic --no-input && python manage.py migrate && gunicorn config.wsgi -b 0.0.0.0:8000 --reload

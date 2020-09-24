FROM python:3.6.9-stretch
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /{backend, static, media}
ENV TZ=America/Lima
RUN ln -snf /user/share/zoneinfo/$TZ etc/localtime && echo $TZ > /etc/timezone
WORKDIR /backend

ADD ./backend /backend
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.pip
CMD python manage.py collectstatic --no-input;python manage.py migrate; gunicorn config.wsgi -b 0.0.0.0:8000 --reload & celery worker -A config.celery_worker

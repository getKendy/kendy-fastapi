FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update 
    # dependencies for building Python packages
# RUN apt-get install -y build-essential 
    # psycopg2 dependencies
RUN apt-get install -y libpq-dev 
    # Additional dependencies
RUN apt-get install -y telnet netcat 
    # cleaning up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false 
RUN rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/local/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/fastapi/celery/worker1/start /start-celeryworker1
RUN sed -i 's/\r$//g' /start-celeryworker1
RUN chmod +x /start-celeryworker1

COPY ./compose/local/fastapi/celery/worker2/start /start-celeryworker2
RUN sed -i 's/\r$//g' /start-celeryworker2
RUN chmod +x /start-celeryworker2

COPY ./compose/local/fastapi/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/fastapi/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

# ENTRYPOINT ["/entrypoint"]
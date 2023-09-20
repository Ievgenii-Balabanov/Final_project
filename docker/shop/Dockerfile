FROM python:3.11-slim as python-base

RUN apt-get update --fix-missing && apt-get upgrade -qy

RUN apt update && apt install curl -y

FROM python-base as python-compile

#COPY ../.././shop/requirements.txt .
COPY ./shop/requirements.txt .

RUN pip install --no-cache-dir -t /python -r requirements.txt

FROM python-base as shop_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=python-compile /python /home/appuser/python
ENV PYTHONPATH=/home/appuser/python
ENV PATH="${PYTHONPATH}/bin:${PATH}"

#COPY . /home/appuser/app
#COPY ./docker /home/appuser/app/docker
#
#WORKDIR /home/appuser/app;

COPY ./shop /home/appuser/app
COPY ./docker/shop /home/appuser/app/docker
WORKDIR /home/appuser/app

#RUN chmod +x docker/runserver.sh docker/wait-for-command.sh docker/docker-entrypoint.sh
#RUN chmod --help docker/runserver.sh docker/wait-for-command.sh docker/docker-entrypoint.sh
RUN chmod --help docker/runserver.sh docker/wait-for-command.sh

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/home/appuser/app/docker/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver"]
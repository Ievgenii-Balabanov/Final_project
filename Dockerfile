FROM python:3.10 as python-base

RUN apt-get update --fix-missing && apt-get upgrade -qy

RUN apt update && apt install curl -y

FROM python-base as python-compile

RUN apt-get install -y --no-install-recommends build-essential gcc libpq-dev libcurl4-openssl-dev libssl-dev git

COPY ./shop/requirements.txt .

RUN pip install --no-cache-dir -t /python -r requirements.txt && find /python \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM python-base as final_project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN addgroup --gid 1001 appuser && adduser --uid 1001 --gid 1001 --shell /bin/bash --disabled-password appuser

#COPY --from=python-compile /python /home/appuser/python
#ENV PYTHONPATH=/home/appuser/python
#ENV PATH="${PYTHONPATH}/bin:${PATH}"
#
#COPY . /home/appuser/app
#WORKDIR /home/appuser/app
#
#RUN chmod +x docker/runserver.sh docker/wait-for-command.sh docker/docker-entrypoint.sh create_admin.py
#USER appuser

EXPOSE 80

#ENTRYPOINT ["/bin/bash", "/home/appuser/app/docker/docker-entrypoint.sh"]
CMD ["./", "manage.py"]
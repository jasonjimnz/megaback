FROM ubuntu:19.04

RUN apt-get update
RUN apt-get install -y git wget python3 python3-pip



EXPOSE 8000

ENV DJANGO_DATABASE_ENGINE=""
ENV DJANGO_DATABASE_NAME = "megaback"
ENV DJANGO_DATABASE_USER = "django"
ENV DJANGO_DATABASE_PASSWORD = "django_pass"
ENV DJANGO_DATABASE_HOST = "databasehost"
ENV DJANGO_DATABASE_PORT = 0

RUN git clone https://github.com/jasonjimnz/megaback.git
RUN pip3 install -r megaback/requirements.txt

CMD [ "/megaback/start_server.sh"]
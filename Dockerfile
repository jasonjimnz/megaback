FROM ubuntu:19.04

RUN apt-get update
RUN apt-get install -y git wget python3 python3-pip



EXPOSE 8000

# If the engine is not SQLITE use the Django names
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
ENV DJANGO_DATABASE_ENGINE "sqlite"
# Database name
ENV DJANGO_DATABASE_NAME "megaback"
# Database user
ENV DJANGO_DATABASE_USER "django"
# Database password
ENV DJANGO_DATABASE_PASSWORD "django_pass"
# Database host
ENV DJANGO_DATABASE_HOST "databasehost"
# Database port
ENV DJANGO_DATABASE_PORT "0"
# The url of your monitor service
# docker run -p 5000:5000 palacios3mw/monitor
ENV MONITOR_SERVICE "http://192.168.1.11:5000"

RUN git clone https://github.com/jasonjimnz/megaback.git
RUN pip3 install -r megaback/requirements.txt

CMD [ "/megaback/start_server.sh"]
FROM ubuntu:16.04

EXPOSE 8000

COPY dailyp_site dailyp_site

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN wget -O- http://packages.couchbase.com/ubuntu/couchbase.key | apt-key add -
RUN wget -O/etc/apt/sources.list.d/couchbase.list http://packages.couchbase.com/ubuntu/couchbase-ubuntu1204.list
RUN apt-get update
RUN apt-get install -y libcouchbase2-libevent libcouchbase-dev
RUN pip install django
RUN pip install djangorestframework
RUN pip install couchbase
RUN pip install pytz

CMD ["python","/dailyp_site/manage.py","runserver", "0:80"]
